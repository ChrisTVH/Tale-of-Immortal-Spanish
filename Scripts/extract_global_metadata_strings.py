#!/usr/bin/env python3
"""
Extract text records from a Unity IL2CPP global-metadata.dat file.

The string-literal ID is the zero-based index in the metadata string-literal
table. It is an IL2CPP metadata ID, not a game localization/configuration ID.
The metadata string table is exported separately because its IDs use a
different namespace and mostly contain identifiers rather than translatable
text.

The extractor streams JSON records to disk so a large metadata file does not
need to be loaded into a Python list.
"""

import argparse
import json
import mmap
import os
import struct
import sys
import tempfile
from pathlib import Path

METADATA_MAGIC = 0xFAB11BAF
METADATA_HEADER_SIZE = 0x100
STRING_LITERAL_TABLE_HEADER_OFFSET = 0x08
STRING_LITERAL_DATA_HEADER_OFFSET = 0x10
METADATA_STRING_TABLE_HEADER_OFFSET = 0x18
STRING_LITERAL_RECORD_SIZE = 0x08
DEFAULT_OUTPUT_NAMES = {
    "literal": "global-metadata-string-literals.json",
    "metadata": "global-metadata-table-strings.json",
    "manifest": "global-metadata-manifest.json",
}


def default_metadata_path():
    """Return the known local game metadata path used by this workspace."""
    return (
        Path.home()
        / ".local/share/Steam/steamapps/common/guigubahuang"
        / "guigubahuang_Data/il2cpp_data/Metadata/global-metadata.dat"
    )


def read_header_pair(metadata, header_offset):
    """Read an offset/count pair from the fixed IL2CPP metadata header."""
    return struct.unpack_from("<II", metadata, header_offset)


def validate_region(region_name, offset, size, file_size):
    """Validate that a metadata region is contained in the input file."""
    if offset > file_size or size > file_size - offset:
        raise ValueError(
            f"{region_name} exceeds the metadata file: "
            f"offset=0x{offset:x}, size=0x{size:x}, file_size=0x{file_size:x}"
        )


def decode_text(raw_text, invalid_counter):
    """Decode a metadata byte sequence and count malformed UTF-8 records."""
    try:
        return raw_text.decode("utf-8")
    except UnicodeDecodeError:
        invalid_counter[0] += 1
        return raw_text.decode("utf-8", errors="replace")


def write_json_records(output_path, records):
    """Write an iterable of records as a UTF-8 JSON array atomically."""
    temporary_path = None
    written_count = 0
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write("[\n")
            for index, record in enumerate(records):
                written_count += 1
                if index:
                    temporary_file.write(",\n")
                serialized_record = json.dumps(
                    record,
                    ensure_ascii=False,
                    indent=2,
                )
                temporary_file.write("  ")
                temporary_file.write(serialized_record.replace("\n", "\n  "))
            temporary_file.write("\n]\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        if output_path.exists():
            temporary_path.chmod(output_path.stat().st_mode)
        else:
            temporary_path.chmod(0o644)
        os.replace(temporary_path, output_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    if written_count == 0:
        raise RuntimeError(f"No records were written to {output_path}")
    return written_count


def iter_string_literals(metadata, table_offset, table_size, data_offset, data_size):
    """Yield every IL2CPP string-literal record without deduplicating text."""
    invalid_counter = [0]
    record_count = table_size // STRING_LITERAL_RECORD_SIZE

    for literal_id in range(record_count):
        record_offset = table_offset + literal_id * STRING_LITERAL_RECORD_SIZE
        length, data_index = struct.unpack_from("<II", metadata, record_offset)
        if data_index > data_size or length > data_size - data_index:
            raise ValueError(
                f"String literal {literal_id} exceeds the literal data region: "
                f"index=0x{data_index:x}, length=0x{length:x}"
            )
        raw_text = metadata[
            data_offset + data_index : data_offset + data_index + length
        ]
        yield {
            "id": str(literal_id),
            "text": decode_text(raw_text, invalid_counter),
            "length": length,
            "data_offset": data_index,
            "file_offset": data_offset + data_index,
        }


def iter_metadata_strings(metadata, table_offset, table_size):
    """Yield every null-terminated string from the metadata string table."""
    invalid_counter = [0]
    table_end = table_offset + table_size
    cursor = table_offset
    string_id = 0

    while cursor < table_end:
        terminator = metadata.find(b"\x00", cursor, table_end)
        if terminator < 0:
            terminator = table_end
            next_cursor = table_end
        else:
            next_cursor = terminator + 1

        raw_text = metadata[cursor:terminator]
        yield {
            "id": str(string_id),
            "text": decode_text(raw_text, invalid_counter),
            "length": len(raw_text),
            "data_offset": cursor - table_offset,
            "file_offset": cursor,
        }
        string_id += 1
        cursor = next_cursor


def extract(metadata_path, output_dir, include_metadata_strings=True):
    """Extract metadata records and return a manifest dictionary."""
    metadata_path = metadata_path.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    with metadata_path.open("rb") as metadata_file:
        file_size = metadata_path.stat().st_size
        if file_size < METADATA_HEADER_SIZE:
            raise ValueError("The metadata file is smaller than the IL2CPP header")

        with mmap.mmap(metadata_file.fileno(), 0, access=mmap.ACCESS_READ) as metadata:
            magic, version = struct.unpack_from("<II", metadata, 0)
            if magic != METADATA_MAGIC:
                raise ValueError(
                    f"Unexpected metadata magic: 0x{magic:08x} "
                    f"(expected 0x{METADATA_MAGIC:08x})"
                )

            literal_table_offset, literal_table_size = read_header_pair(
                metadata, STRING_LITERAL_TABLE_HEADER_OFFSET
            )
            literal_data_offset, literal_data_size = read_header_pair(
                metadata, STRING_LITERAL_DATA_HEADER_OFFSET
            )
            metadata_table_offset, metadata_table_size = read_header_pair(
                metadata, METADATA_STRING_TABLE_HEADER_OFFSET
            )

            if literal_table_size % STRING_LITERAL_RECORD_SIZE:
                raise ValueError(
                    "The string-literal table size is not a multiple of 8 bytes"
                )

            validate_region(
                "string-literal table",
                literal_table_offset,
                literal_table_size,
                file_size,
            )
            validate_region(
                "string-literal data",
                literal_data_offset,
                literal_data_size,
                file_size,
            )
            validate_region(
                "metadata string table",
                metadata_table_offset,
                metadata_table_size,
                file_size,
            )

            literal_count = literal_table_size // STRING_LITERAL_RECORD_SIZE
            literal_output = output_dir / DEFAULT_OUTPUT_NAMES["literal"]
            print(
                f"Extracting {literal_count:,} string literals from {metadata_path}",
                file=sys.stderr,
            )
            write_json_records(
                literal_output,
                iter_string_literals(
                    metadata,
                    literal_table_offset,
                    literal_table_size,
                    literal_data_offset,
                    literal_data_size,
                ),
            )

            metadata_count = 0
            metadata_output = output_dir / DEFAULT_OUTPUT_NAMES["metadata"]
            if include_metadata_strings:
                metadata_records = iter_metadata_strings(
                    metadata,
                    metadata_table_offset,
                    metadata_table_size,
                )

                metadata_count = write_json_records(
                    metadata_output,
                    metadata_records,
                )
            elif metadata_output.exists():
                metadata_output.unlink()

            manifest = {
                "source": str(metadata_path),
                "file_size": file_size,
                "metadata_magic": f"0x{magic:08x}",
                "metadata_version": version,
                "string_literals": {
                    "file": literal_output.name,
                    "count": literal_count,
                    "table_offset": literal_table_offset,
                    "table_size": literal_table_size,
                    "data_offset": literal_data_offset,
                    "data_size": literal_data_size,
                    "id_namespace": "zero-based string-literal table index",
                },
                "metadata_strings": {
                    "file": metadata_output.name,
                    "count": metadata_count,
                    "table_offset": metadata_table_offset,
                    "table_size": metadata_table_size,
                    "id_namespace": "zero-based null-terminated metadata string index",
                    "included": include_metadata_strings,
                },
            }

    manifest_output = output_dir / DEFAULT_OUTPUT_NAMES["manifest"]
    write_json_records(manifest_output, (manifest,))
    return manifest


def parse_args(argv=None):
    """Parse command-line arguments."""
    scripts_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Extract Unity IL2CPP strings from global-metadata.dat."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=default_metadata_path(),
        help="Path to global-metadata.dat",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=scripts_dir / "Raw",
        help="Directory for raw JSON output",
    )
    parser.add_argument(
        "--literal-only",
        action="store_true",
        help="Skip the separate metadata identifier-string table",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Run the extractor and report the generated files."""
    args = parse_args(argv)
    if not args.input.is_file():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 1

    try:
        manifest = extract(
            args.input,
            args.output_dir,
            include_metadata_strings=not args.literal_only,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: output directory: {args.output_dir.resolve()}")
    print(f"OK: string literals: {manifest['string_literals']['count']:,}")
    print(f"OK: metadata strings: {manifest['metadata_strings']['count']:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
