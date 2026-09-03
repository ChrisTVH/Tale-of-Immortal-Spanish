#!/usr/bin/env python3
"""Classify extracted IL2CPP strings without changing the raw extraction.

The raw files remain the immutable evidence layer. This script creates a
derived, reviewable layer with language classification, exclusion reasons and
references to known localization records from Scripts/Default/.

The IDs in the output are still metadata IDs. Configuration references are
added only when the exact text matches a localization table in source_specs.
"""

import argparse
import json
import re
import sqlite3
import sys
import tempfile
import unicodedata
from contextlib import ExitStack
from pathlib import Path


SCRIPT_NAMES = {
    "han": "Han",
    "hangul": "Hangul",
    "hiragana": "Hiragana",
    "katakana": "Katakana",
    "latin": "Latin",
    "cyrillic": "Cyrillic",
    "arabic": "Arabic",
    "thai": "Thai",
    "greek": "Greek",
    "hebrew": "Hebrew",
    "devanagari": "Devanagari",
}

LANGUAGE_BUCKETS = (
    "zh-Hans",
    "zh-Hant",
    "zh-ambiguous",
    "en",
    "es",
    "ko",
    "ja",
    "mixed",
    "other",
    "unknown",
)

ENGLISH_HINTS = {
    "a", "about", "after", "all", "and", "are", "as", "at", "back", "be",
    "carefully", "can", "cannot", "choose", "confirm", "continue", "death",
    "do", "down", "for", "from", "has", "have", "here", "if", "in", "into",
    "is", "it", "just", "leave", "let", "live", "maybe", "more", "my", "no",
    "not", "of", "on", "or", "right", "saw", "should", "take", "the", "their",
    "there", "these", "this", "to", "up", "was", "what", "where", "with", "wrong",
    "yes", "you", "your",
}

SPANISH_HINTS = {
    "a", "al", "algo", "aquí", "atención", "con", "confirmar", "cuidadosamente",
    "de", "del", "dónde", "en", "es", "esta", "este", "hay", "la", "las", "lo",
    "los", "más", "me", "mi", "no", "o", "para", "por", "puede", "qué", "que",
    "salir", "si", "sin", "sobre", "son", "tus", "un", "una", "y", "ya",
}

SIMPLIFIED_MARKERS = set("这过后发国会学门气体问说为见来经开长关电画风网鱼鸟")
TRADITIONAL_MARKERS = set("這過後發國會學門氣體問說為見來經開長關電畫風網魚鳥")

PATH_OR_FORMAT_RE = re.compile(
    r"(?:^|[\\/])(?:assets?|resources?|streamingassets?|managed|plugins?)(?:[\\/]|$)"
    r"|\.(?:dll|json|png|jpg|jpeg|asset|prefab|bytes|resS|bundle)$"
    r"|^[0-9a-f]{8,}$",
    re.IGNORECASE,
)
TECHNICAL_RE = re.compile(
    r"^(?:System|UnityEngine|Il2Cpp|Mono|Conf|UI|Data|GameTool|ModData)[.\\/]"
    r"|^(?:get_|set_|b__|cctor|ctor|op_)[A-Za-z0-9_`.<>,]*$"
    r"|(?:\.ctor|::|`[0-9]+$)",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")
TOKEN_RE = re.compile(
    r"\{[^{}]*\}|&[^&]*&|\$[^$]*\$|"
    r"</?(?:r|g|b|o|y|p|w|color|size|align|indent|link|u|space|voffset|sprite|root[0-4])"
    r"(?:\s+[^>]*)?(?:=[^>]*)?>|<#?[0-9A-Fa-f]{6,8}>"
)
METADATA_IDENTIFIER_RE = re.compile(
    r"^(?:[A-Za-z_][A-Za-z0-9_`<>./+:-]*|<[^>]+>)$"
)


def iter_json_array(path):
    """Yield objects from a JSON array while keeping memory bounded."""
    with path.open("r", encoding="utf-8") as input_file:
        array_started = False
        array_closed = False
        expect_item = True
        has_items = False
        after_comma = False
        item_buffer = []
        object_depth = 0
        in_string = False
        escaped = False

        for line in input_file:
            for character in line:
                if array_closed:
                    if not character.isspace():
                        raise ValueError(f"{path}: trailing content after JSON array")
                    continue

                if object_depth == 0:
                    if not array_started:
                        if character.isspace():
                            continue
                        if character != "[":
                            raise ValueError(f"{path}: JSON root must be an array")
                        array_started = True
                        continue

                    if expect_item:
                        if character.isspace():
                            continue
                        if character == "{":
                            item_buffer = [character]
                            object_depth = 1
                            in_string = False
                            escaped = False
                            expect_item = False
                            after_comma = False
                        elif character == "]" and not has_items:
                            array_closed = True
                        else:
                            raise ValueError(
                                f"{path}: expected an object after '[' or ','"
                            )
                        continue

                    if character.isspace():
                        continue
                    if character == ",":
                        expect_item = True
                        after_comma = True
                    elif character == "]":
                        array_closed = True
                    else:
                        raise ValueError(
                            f"{path}: expected ',' or ']' after array item"
                        )
                    continue

                item_buffer.append(character)
                if in_string:
                    if escaped:
                        escaped = False
                    elif character == "\\":
                        escaped = True
                    elif character == '"':
                        in_string = False
                    continue
                if character == '"':
                    in_string = True
                elif character == "{":
                    object_depth += 1
                elif character == "}":
                    object_depth -= 1
                    if object_depth == 0:
                        try:
                            yield json.loads("".join(item_buffer))
                        except json.JSONDecodeError as error:
                            raise ValueError(
                                f"{path}: invalid JSON object: {error}"
                            ) from error
                        item_buffer = []
                        has_items = True
                        expect_item = False
                        after_comma = False

        if object_depth or not array_started or not array_closed:
            raise ValueError(f"{path}: incomplete JSON array")
        if after_comma:
            raise ValueError(f"{path}: trailing comma in JSON array")


class JsonArrayWriter:
    """Write one JSON array atomically, one record at a time."""

    def __init__(self, output_path):
        self.output_path = output_path
        self.temporary_file = None
        self.temporary_path = None
        self.count = 0

    def __enter__(self):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.temporary_file = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=self.output_path.parent,
            prefix=f".{self.output_path.name}.",
            suffix=".tmp",
            delete=False,
        )
        self.temporary_path = Path(self.temporary_file.name)
        self.temporary_file.write("[\n")
        return self

    def write(self, record):
        if self.count:
            self.temporary_file.write(",\n")
        serialized = json.dumps(record, ensure_ascii=False, indent=2)
        self.temporary_file.write("  ")
        self.temporary_file.write(serialized.replace("\n", "\n  "))
        self.count += 1

    def __exit__(self, exception_type, exception, traceback):
        if self.temporary_file is None:
            return False
        try:
            if exception_type is None:
                self.temporary_file.write("\n]\n")
                self.temporary_file.flush()
                self.temporary_file.close()
                if self.output_path.exists():
                    self.temporary_path.chmod(self.output_path.stat().st_mode)
                else:
                    self.temporary_path.chmod(0o644)
                self.temporary_path.replace(self.output_path)
            else:
                self.temporary_file.close()
        finally:
            if self.temporary_path is not None and self.temporary_path.exists():
                self.temporary_path.unlink()
        return False


def load_manifest(raw_dir):
    """Load the small raw manifest and return source metadata."""
    manifest_path = raw_dir / "global-metadata-manifest.json"
    manifest_items = list(iter_json_array(manifest_path))
    if len(manifest_items) != 1 or not isinstance(manifest_items[0], dict):
        raise ValueError(f"{manifest_path}: expected one manifest object")
    return manifest_items[0]


def build_known_text_index(default_dir):
    """Index exact language values from the localization source tables."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE known_text (
            text TEXT NOT NULL,
            language TEXT NOT NULL,
            source_file TEXT NOT NULL,
            source_id TEXT NOT NULL,
            structural_key TEXT NOT NULL,
            UNIQUE(text, language, source_file, source_id, structural_key)
        )
        """
    )
    connection.execute("CREATE INDEX known_text_value ON known_text(text)")

    source_specs = {
        "LocalText.json": (
            "key",
            {"zh-Hans": "ch", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
        "RoleLogLocal.json": (
            "keyID",
            {"zh-Hans": "ch", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
        "NpcNameFirst.json": (
            "id",
            {"zh-Hans": "name", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
        "NpcNameLast.json": (
            "id",
            {"zh-Hans": "name", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
        "HerdNPCNameFirst.json": (
            "id",
            {"zh-Hans": "name", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
        "BattleSkillPrefixName.json": (
            "id",
            {"zh-Hans": "text", "zh-Hant": "tc", "en": "en", "ko": "kr"},
        ),
    }

    for filename, (structural_field, language_fields) in source_specs.items():
        source_path = default_dir / filename
        if not source_path.is_file():
            continue
        for item in iter_json_array(source_path):
            if not isinstance(item, dict):
                continue
            structural_key = item.get(structural_field)
            source_id = item.get("id")
            if not isinstance(structural_key, str) or not isinstance(source_id, str):
                continue
            for language, field in language_fields.items():
                text = item.get(field)
                if isinstance(text, str) and text:
                    connection.execute(
                        "INSERT OR IGNORE INTO known_text "
                        "(text, language, source_file, source_id, structural_key) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (text, language, filename, source_id, structural_key),
                    )
    connection.commit()
    return connection


def lookup_known_text(connection, text):
    """Return known languages and bounded config references for exact text."""
    rows = connection.execute(
        "SELECT language, source_file, source_id, structural_key "
        "FROM known_text WHERE text = ? ORDER BY source_file, source_id, language",
        (text,),
    ).fetchall()
    languages = sorted({row[0] for row in rows})
    references = [
        {
            "source_file": row[1],
            "id": row[2],
            "key": row[3],
            "language": row[0],
        }
        for row in rows[:50]
    ]
    return languages, references, len(rows)


def script_counts(text):
    """Count meaningful Unicode scripts after removing syntax tokens."""
    visible_text = TOKEN_RE.sub("", text)
    counts = {name: 0 for name in SCRIPT_NAMES}
    for character in visible_text:
        codepoint = ord(character)
        if (
            0x3400 <= codepoint <= 0x4DBF
            or 0x4E00 <= codepoint <= 0x9FFF
            or 0xF900 <= codepoint <= 0xFAFF
        ):
            counts["han"] += 1
        elif 0xAC00 <= codepoint <= 0xD7AF:
            counts["hangul"] += 1
        elif 0x3040 <= codepoint <= 0x309F:
            counts["hiragana"] += 1
        elif 0x30A0 <= codepoint <= 0x30FF:
            counts["katakana"] += 1
        elif 0x0041 <= codepoint <= 0x024F or 0x1E00 <= codepoint <= 0x1EFF:
            counts["latin"] += 1
        elif 0x0400 <= codepoint <= 0x052F:
            counts["cyrillic"] += 1
        elif 0x0600 <= codepoint <= 0x06FF:
            counts["arabic"] += 1
        elif 0x0E00 <= codepoint <= 0x0E7F:
            counts["thai"] += 1
        elif 0x0370 <= codepoint <= 0x03FF:
            counts["greek"] += 1
        elif 0x0590 <= codepoint <= 0x05FF:
            counts["hebrew"] += 1
        elif 0x0900 <= codepoint <= 0x097F:
            counts["devanagari"] += 1
    return counts


def visible_words(text):
    """Return lower-case Latin words outside syntax tokens."""
    return {word.lower() for word in WORD_RE.findall(TOKEN_RE.sub("", text))}


def classify_language(text, known_languages):
    """Classify language using exact source matches and conservative heuristics."""
    counts = script_counts(text)
    detected_scripts = [
        SCRIPT_NAMES[name]
        for name, count in counts.items()
        if count
    ]

    if known_languages:
        if len(known_languages) == 1:
            language = known_languages[0]
            return language, [language], 0.99, detected_scripts, [
                "exact match with a known localization field"
            ]
        return "mixed", known_languages, 0.95, detected_scripts, [
            "exact text matches multiple localization language fields"
        ]

    if counts["hangul"] >= 2:
        return "ko", ["ko"], 0.98, detected_scripts, ["contains meaningful Hangul"]
    if counts["hiragana"] + counts["katakana"] >= 2:
        return "ja", ["ja"], 0.92, detected_scripts, ["contains multiple kana characters"]
    if counts["han"] and not counts["latin"] and not counts["hangul"]:
        simplified = len(set(text) & SIMPLIFIED_MARKERS)
        traditional = len(set(text) & TRADITIONAL_MARKERS)
        if simplified and not traditional:
            return "zh-Hans", ["zh-Hans"], 0.72, detected_scripts, [
                "Han text contains simplified-only markers"
            ]
        if traditional and not simplified:
            return "zh-Hant", ["zh-Hant"], 0.72, detected_scripts, [
                "Han text contains traditional-only markers"
            ]
        return "zh-ambiguous", ["zh-ambiguous"], 0.60, detected_scripts, [
            "Han text cannot reliably distinguish simplified from traditional"
        ]

    if len(detected_scripts) > 1:
        return "mixed", ["mixed"], 0.70, detected_scripts, [
            "contains multiple scripts"
        ]

    non_latin_scripts = [script for script in detected_scripts if script != "Latin"]
    if non_latin_scripts:
        if len(non_latin_scripts) == 1:
            return "other", ["other"], 0.90, detected_scripts, [
                f"contains {non_latin_scripts[0]} without a known localization match"
            ]
        return "other", ["other"], 0.75, detected_scripts, [
            "contains multiple non-Latin scripts without a known localization match"
        ]

    if counts["latin"]:
        words = visible_words(text)
        english_score = len(words & ENGLISH_HINTS)
        spanish_score = len(words & SPANISH_HINTS)
        if english_score >= 2 and english_score > spanish_score * 1.5:
            return "en", ["en"], 0.78, detected_scripts, [
                "Latin text has a strong English lexical signal"
            ]
        if spanish_score >= 2 and spanish_score > english_score * 1.5:
            return "es", ["es"], 0.78, detected_scripts, [
                "Latin text has a strong Spanish lexical signal"
            ]
        return "unknown", ["unknown"], 0.40, detected_scripts, [
            "Latin text is too short or ambiguous for reliable language detection"
        ]

    return "unknown", ["unknown"], 0.20, detected_scripts, [
        "no meaningful alphabetic script detected"
    ]


def analyze_record(record, source_namespace, record_offset, known_index):
    """Return a classified record and its output routing information."""
    if not isinstance(record, dict):
        raise ValueError(f"{source_namespace}: raw record is not an object")
    text = record.get("text")
    if not isinstance(text, str):
        raise ValueError(f"{source_namespace}: raw record has no text field")

    known_languages, config_refs, config_ref_count = lookup_known_text(
        known_index, text
    )
    reasons = []
    exclusion_reasons = []
    stripped_text = text.strip(" \t\r\n\x00")
    visible_text = TOKEN_RE.sub("", stripped_text)
    if not stripped_text:
        exclusion_reasons.append("empty_or_nontext_only")
    elif not visible_text.strip():
        exclusion_reasons.append("placeholder_or_format_only")
    elif not any(character.isalpha() for character in visible_text):
        exclusion_reasons.append("numeric_or_symbol_only")
    if "\ufffd" in text:
        exclusion_reasons.append("invalid_utf8_replacement")
    if PATH_OR_FORMAT_RE.search(stripped_text):
        exclusion_reasons.append("path_format_or_hash")
    if TECHNICAL_RE.search(stripped_text):
        exclusion_reasons.append("technical_identifier")
    if (
        source_namespace == "metadata_string"
        and not known_languages
        and METADATA_IDENTIFIER_RE.fullmatch(stripped_text)
    ):
        exclusion_reasons.append("metadata_identifier")

    if not exclusion_reasons:
        language, languages, confidence, detected_scripts, reasons = classify_language(
            text, known_languages
        )
        translation_eligible = True
        classification = "translation_candidate"
    else:
        language = (
            "technical"
            if {"technical_identifier", "metadata_identifier"}
            & set(exclusion_reasons)
            else "excluded"
        )
        languages = []
        confidence = 1.0 if len(exclusion_reasons) == 1 else 0.95
        detected_scripts = [
            SCRIPT_NAMES[name]
            for name, count in script_counts(text).items()
            if count
        ]
        reasons = [f"excluded: {reason}" for reason in exclusion_reasons]
        translation_eligible = False
        classification = "technical" if language == "technical" else "excluded"

    classified = dict(record)
    classified.update(
        {
            "source_namespace": source_namespace,
            "record_offset": record_offset,
            "languages": languages,
            "language_bucket": language,
            "script": detected_scripts,
            "classification": classification,
            "confidence": confidence,
            "classification_reason": reasons,
            "translation_eligible": translation_eligible,
            "config_refs": config_refs,
            "config_ref_count": config_ref_count,
            "exclusion_reasons": exclusion_reasons,
        }
    )
    return classified, language


def classify_file(
    raw_path,
    output_path,
    source_namespace,
    record_offset_base,
    record_size,
    known_index,
    language_writers,
    technical_writer,
    excluded_writer,
):
    """Classify one raw file and write all derived routes."""
    count = 0
    for record in iter_json_array(raw_path):
        record_id = record.get("id") if isinstance(record, dict) else None
        record_offset = None
        if record_offset_base is not None and isinstance(record_id, str) and record_id.isdigit():
            record_offset = record_offset_base + int(record_id) * record_size
        classified, language = analyze_record(
            record,
            source_namespace,
            record_offset,
            known_index,
        )
        output_path.write(classified)
        if classified["translation_eligible"]:
            language_writers[language if language in LANGUAGE_BUCKETS else "unknown"].write(
                classified
            )
        else:
            excluded_writer.write(classified)
            if classified["classification"] == "technical":
                technical_writer.write(classified)
        count += 1
    return count


def parse_args(argv=None):
    """Parse command-line options."""
    scripts_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Classify extracted IL2CPP strings by language and eligibility."
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=scripts_dir / "Raw",
        help="Directory containing the raw extractor output",
    )
    parser.add_argument(
        "--default-dir",
        type=Path,
        default=scripts_dir / "Default",
        help="Directory containing the source localization JSON files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=scripts_dir / "Output" / "Metadata",
        help="Directory for derived classification output",
    )
    parser.add_argument(
        "--literal-only",
        action="store_true",
        help="Classify only string-literal records",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Build all derived outputs."""
    args = parse_args(argv)
    literal_path = args.raw_dir / "global-metadata-string-literals.json"
    table_path = args.raw_dir / "global-metadata-table-strings.json"
    if not literal_path.is_file():
        print(f"ERROR: missing raw input: {literal_path}", file=sys.stderr)
        return 1
    if not args.literal_only and not table_path.is_file():
        print(f"ERROR: missing raw input: {table_path}", file=sys.stderr)
        return 1

    try:
        manifest = load_manifest(args.raw_dir)
        literal_info = manifest["string_literals"]
        metadata_info = manifest["metadata_strings"]
        known_index = build_known_text_index(args.default_dir)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        by_language_dir = args.output_dir / "by-language"

        language_paths = {
            language: by_language_dir / f"{language}.json"
            for language in LANGUAGE_BUCKETS
        }
        classified_paths = {
            "literal": args.output_dir / "classified-string-literals.json",
            "metadata": args.output_dir / "classified-table-strings.json",
        }
        technical_path = args.output_dir / "technical.json"
        excluded_path = args.output_dir / "excluded-for-translation.json"
        counts = {}

        with ExitStack() as stack:
            classified_writers = {
                name: stack.enter_context(JsonArrayWriter(path))
                for name, path in classified_paths.items()
            }
            language_writers = {
                language: stack.enter_context(JsonArrayWriter(path))
                for language, path in language_paths.items()
            }
            technical_writer = stack.enter_context(JsonArrayWriter(technical_path))
            excluded_writer = stack.enter_context(JsonArrayWriter(excluded_path))

            counts["string_literals"] = classify_file(
                literal_path,
                classified_writers["literal"],
                "string_literal",
                literal_info["table_offset"],
                8,
                known_index,
                language_writers,
                technical_writer,
                excluded_writer,
            )
            if counts["string_literals"] != literal_info["count"]:
                raise ValueError(
                    "string literal count mismatch: "
                    f"expected {literal_info['count']}, got {counts['string_literals']}"
                )
            if not args.literal_only:
                counts["metadata_strings"] = classify_file(
                    table_path,
                    classified_writers["metadata"],
                    "metadata_string",
                    None,
                    0,
                    known_index,
                    language_writers,
                    technical_writer,
                    excluded_writer,
                )
                if counts["metadata_strings"] != metadata_info["count"]:
                    raise ValueError(
                        "metadata string count mismatch: "
                        f"expected {metadata_info['count']}, "
                        f"got {counts['metadata_strings']}"
                    )
            else:
                counts["metadata_strings"] = 0

        manifest_output = {
            "raw_manifest": str((args.raw_dir / "global-metadata-manifest.json").resolve()),
            "raw_is_unchanged": True,
            "source_localization_dir": str(args.default_dir.resolve()),
            "output_dir": str(args.output_dir.resolve()),
            "classification": {
                "language_files_contain_translation_eligible_records_only": True,
                "technical_is_a_subset_of_excluded_for_translation": True,
                "config_refs_are_exact_text_matches_only": True,
            },
            "counts": counts,
            "output_files": {
                "classified_string_literals": classified_paths["literal"].name,
                "classified_metadata_strings": classified_paths["metadata"].name,
                "technical": technical_path.name,
                "excluded": excluded_path.name,
                "by_language": {
                    language: f"by-language/{language}.json"
                    for language in LANGUAGE_BUCKETS
                },
            },
        }
        with JsonArrayWriter(args.output_dir / "classification-manifest.json") as writer:
            writer.write(manifest_output)
        known_index.close()
    except (OSError, KeyError, ValueError, sqlite3.Error, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: output directory: {args.output_dir.resolve()}")
    print(f"OK: string literals: {counts['string_literals']:,}")
    print(f"OK: metadata strings: {counts['metadata_strings']:,}")
    print("OK: language-separated and exclusion outputs generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
