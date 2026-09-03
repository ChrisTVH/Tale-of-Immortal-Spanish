#!/usr/bin/env python3
"""Build the editable Spanish catalog for unreferenced IL2CPP string literals."""

import argparse
import sys
from collections import Counter
from pathlib import Path

from classify_global_metadata_strings import TOKEN_RE, JsonArrayWriter, iter_json_array


SOURCE_NAMESPACE = "string_literal"
CHINESE_LANGUAGE_BUCKETS = {"zh-Hans", "zh-Hant", "zh-ambiguous"}


def parse_args(argv=None):
    """Parse command-line options."""
    scripts_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=(
            "Genera GlobalMetadata.json desde literales Han elegibles sin "
            "referencias a la configuración de localización."
        )
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=scripts_dir
        / "Output"
        / "Metadata"
        / "classified-string-literals.json",
        help="Archivo clasificado de literales IL2CPP",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            scripts_dir.parent
            / "ModProject"
            / "ModCode"
            / "ModMain"
            / "Localization"
            / "Spanish"
            / "GlobalMetadata.json"
        ),
        help="Catálogo español de metadata global",
    )
    parser.add_argument(
        "--runtime-output",
        type=Path,
        default=(
            scripts_dir.parent
            / "ModProject"
            / "ModCode"
            / "ModMain"
            / "Localization"
            / "Spanish"
            / "GlobalMetadata.runtime.json"
        ),
        help="Recurso runtime filtrado a entradas ya traducidas",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="informa los cambios sin escribir el catálogo",
    )
    return parser.parse_args(argv)


def validate_entry(item, path, index):
    """Validate one editable global-metadata entry and return its key."""
    if not isinstance(item, dict):
        raise ValueError(f"{path}: la entrada {index} debe ser un objeto JSON")

    source_namespace = item.get("source_namespace")
    entry_id = item.get("id")
    text = item.get("text")
    translation = item.get("es")
    if source_namespace != SOURCE_NAMESPACE:
        raise ValueError(
            f"{path}: la entrada {index} debe usar "
            f"source_namespace={SOURCE_NAMESPACE!r}"
        )
    if not isinstance(entry_id, str) or not entry_id.isdigit():
        raise ValueError(f"{path}: la entrada {index} tiene un id no numérico")
    if not isinstance(text, str) or not text:
        raise ValueError(f"{path}: la entrada {index} no contiene texto fuente")
    if not isinstance(translation, str):
        raise ValueError(f"{path}: la entrada {index} tiene un campo es no textual")
    if translation and Counter(TOKEN_RE.findall(text)) != Counter(TOKEN_RE.findall(translation)):
        raise ValueError(
            f"{path}: la entrada {index} no conserva los tokens del texto fuente"
        )
    return source_namespace, entry_id


def load_existing_entries(path):
    """Load editable entries while retaining translations from prior runs."""
    if not path.exists():
        return {}

    entries = {}
    for index, item in enumerate(iter_json_array(path)):
        key = validate_entry(item, path, index)
        if key in entries:
            raise ValueError(f"{path}: ID duplicado {key[1]!r}")
        entries[key] = item
    return entries


def is_global_metadata_candidate(record):
    """Return whether a classified record is safe for the editable catalog."""
    return (
        isinstance(record, dict)
        and record.get("source_namespace") == SOURCE_NAMESPACE
        and record.get("translation_eligible") is True
        and record.get("language_bucket") in CHINESE_LANGUAGE_BUCKETS
        and "Han" in record.get("script", ())
        and not record.get("config_refs")
        and record.get("config_ref_count", 0) == 0
        and isinstance(record.get("id"), str)
        and record["id"].isdigit()
        and isinstance(record.get("text"), str)
        and bool(record["text"])
    )


def collect_candidates(path):
    """Collect current unreferenced Han string-literal candidates by ID."""
    candidates = {}
    for record in iter_json_array(path):
        if not is_global_metadata_candidate(record):
            continue
        key = (SOURCE_NAMESPACE, record["id"])
        if key in candidates:
            raise ValueError(f"{path}: ID de metadata duplicado {record['id']!r}")
        candidates[key] = record["text"]
    return candidates


def build_entries(candidates, existing_entries):
    """Merge current candidates with previous translations without overwriting them."""
    entries = {
        key: existing_entries[key]
        for key in candidates
        if key in existing_entries
    }
    added = 0
    retained = 0

    for key, text in candidates.items():
        existing = entries.get(key)
        if existing is None:
            entries[key] = {
                "source_namespace": SOURCE_NAMESPACE,
                "id": key[1],
                "text": text,
                "es": "",
            }
            added += 1
            continue
        if existing["text"] != text:
            raise ValueError(
                "La metadata cambió el texto del id "
                f"{key[1]!r}; revisa la entrada antes de actualizarla"
            )
        retained += 1

    stale = len(existing_entries) - len(entries)
    ordered = sorted(entries.values(), key=lambda item: int(item["id"]))
    return ordered, added, retained, stale


def build_runtime_entries(entries):
    """Return translated entries after rejecting conflicting source-text mappings."""
    by_text = {}
    runtime_entries = []
    for entry in entries:
        translation = entry["es"]
        if not translation:
            continue
        existing = by_text.get(entry["text"])
        if existing is not None and existing != translation:
            raise ValueError(
                "Existen traducciones distintas para el mismo texto fuente "
                f"en GlobalMetadata: {entry['text']!r}"
            )
        by_text[entry["text"]] = translation
        runtime_entries.append(entry)
    return runtime_entries


def write_entries(path, entries):
    """Write the catalog atomically using the project JSON-array writer."""
    with JsonArrayWriter(path) as writer:
        for entry in entries:
            writer.write(entry)


def main(argv=None):
    """Create or update the GlobalMetadata candidate catalog."""
    args = parse_args(argv)
    if not args.metadata.is_file():
        print(f"ERROR: no existe el archivo de metadata: {args.metadata}", file=sys.stderr)
        return 1

    try:
        existing_entries = load_existing_entries(args.output)
        candidates = collect_candidates(args.metadata)
        entries, added, retained, stale = build_entries(candidates, existing_entries)
        runtime_entries = build_runtime_entries(entries)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Candidatos actuales: {len(candidates)}")
    print(f"Entradas conservadas: {retained}")
    print(f"Entradas nuevas: {added}")
    print(f"Entradas retiradas: {stale}")
    print(f"Total del catálogo: {len(entries)}")
    print(f"Entradas runtime traducidas: {len(runtime_entries)}")
    if args.dry_run:
        print("DRY-RUN: no se escribieron los archivos de salida")
        return 0

    try:
        write_entries(args.output, entries)
        write_entries(args.runtime_output, runtime_entries)
    except OSError as error:
        print(f"ERROR: no se pudo escribir el catálogo: {error}", file=sys.stderr)
        return 1
    print(f"OK: catálogo escrito en {args.output}")
    print(f"OK: recurso runtime escrito en {args.runtime_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
