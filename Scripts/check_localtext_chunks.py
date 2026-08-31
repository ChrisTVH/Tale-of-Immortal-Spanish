#!/usr/bin/env python3
"""Read-only structural and placeholder validator for localization chunks.

The processed files are the authoritative source.  This script never writes
to either the processed files or the Spanish resources.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


FILES = {"LocalText.json", "RoleLogLocal.json"}
ALLOWED_LOCALTEXT_EXTRA_IDS = {"9000001"}
LOCALTEXT_EMPTY_SOURCE_EXCEPTION = "24209"
ROLE_INCOMPLETE_CALLIGNORE_EXCEPTION = "10560001"
ROLE_TOKENS = {
    "relation",
    "life",
    "grade",
    "name",
    "gender",
    "school",
    "appellation",
    "callIgnore",
    "yinyangEyeSoul",
    "fixValue点",
    "宗门职位",
    "garde",
}

PLACEHOLDER_RE = re.compile(r"\{[^{}\r\n]*\}")
VARIABLE_RE = re.compile(r"&[^&\r\n]*&")
DICTIONARY_TOKEN_RE = re.compile(r"\$[^$\r\n]*\$")
# Only these known game markup tags are syntax. Other angle-bracketed text is
# visible content and may be translated, for example
# ``<秋枫夜话琉璃盏>`` -> ``<Historia de la Lámpara del Alma>``.
MARKUP_TAG_NAMES = (
    "r|g|b|o|y|p|w|color|size|align|indent|link|u|space|voffset|sprite|"
    "root[0-4]|blod"
)
TAG_PREFIX_RE = re.compile(
    rf"<\s*/?\s*(?:#[0-9A-Fa-f]+|(?:{MARKUP_TAG_NAMES}))(?=[\s=/>])"
)
TAG_RE = re.compile(
    rf"<\s*/?\s*(?:#[0-9A-Fa-f]+|(?:{MARKUP_TAG_NAMES}))(?=[\s=/>])[^<>\r\n]*>"
)
TAG_NAME_RE = re.compile(r"^<\s*/?\s*([A-Za-z][\w:-]*|#[0-9A-Fa-f]+)")


class ValidationIssue:
    """A report item with a CI-relevant severity."""

    def __init__(self, severity, message):
        self.severity = severity
        self.message = message


def _entry_label(index, item=None):
    if item is None:
        return f"índice {index + 1}"
    entry_id = item.get("id", "?")
    return f"índice {index + 1}, id {entry_id}"


def load_json(path):
    """Load one JSON document with strict UTF-8 decoding."""
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def validate_schema(data, path, file_name, side):
    """Validate the resource schema and return an ID-to-entry index."""
    issues = []
    entries_by_id = {}
    seen_ids = {}
    seen_keys = {}
    structural_field = "key" if file_name == "LocalText.json" else "keyID"
    text_field = "es" if side == "spanish" else "en"

    if not isinstance(data, list):
        return [ValidationIssue("ERROR", f"{path}: la raíz debe ser una lista JSON")], {}

    required = ("id", structural_field, text_field)
    for index, item in enumerate(data):
        label = _entry_label(index, item if isinstance(item, dict) else None)
        if not isinstance(item, dict):
            issues.append(ValidationIssue("ERROR", f"{path}: {label} debe ser un objeto JSON"))
            continue

        entry_id = item.get("id")
        valid_id = isinstance(entry_id, str) and entry_id.isdigit()
        if not valid_id:
            issues.append(
                ValidationIssue("ERROR", f"{path}: {label} tiene un id no numérico")
            )
        elif entry_id in seen_ids:
            issues.append(
                ValidationIssue(
                    "ERROR",
                    f"{path}: id duplicado {entry_id!r} en los índices "
                    f"{seen_ids[entry_id] + 1} y {index + 1}",
                )
            )
        else:
            seen_ids[entry_id] = index
            entries_by_id[entry_id] = item

        missing = [field for field in required if field not in item]
        if missing:
            issues.append(
                ValidationIssue(
                    "ERROR",
                    f"{path}: {label} no contiene {', '.join(missing)}",
                )
            )

        if structural_field in item and not isinstance(item[structural_field], str):
            issues.append(
                ValidationIssue(
                    "ERROR",
                    f"{path}: {_entry_label(index, item)}: {structural_field} debe ser texto",
                )
            )
        elif (
            file_name == "LocalText.json"
            and structural_field in item
            and item[structural_field] in seen_keys
        ):
            issues.append(
                ValidationIssue(
                    "ERROR",
                    f"{path}: key duplicada {item[structural_field]!r} en los índices "
                    f"{seen_keys[item[structural_field]] + 1} y {index + 1}",
                )
            )
        elif file_name == "LocalText.json" and structural_field in item:
            seen_keys[item[structural_field]] = index

        if text_field in item and not isinstance(item[text_field], str):
            issues.append(
                ValidationIssue(
                    "ERROR",
                    f"{path}: {_entry_label(index, item)}: {text_field} debe ser texto",
                )
            )

    return issues, entries_by_id


def _matches_with_spans(pattern, text):
    return [(match.group(0), match.start(), match.end()) for match in pattern.finditer(text)]


def _context(position, spans):
    for name, start, end in reversed(spans):
        if start <= position < end:
            return name
    return "text"


def _delimiter_signature(text):
    return tuple(character for character in text if character in "[]【】")


def _escape_signature(text):
    result = []
    index = 0
    while index < len(text):
        if text[index] != "\\":
            index += 1
            continue
        if index + 1 < len(text):
            result.append(text[index : index + 2])
            index += 2
        else:
            result.append("\\")
            index += 1
    return tuple(result)


def _tag_name(tag):
    match = TAG_NAME_RE.match(tag)
    return match.group(1).lower() if match else None


def _syntax_issues(text):
    """Return lightweight syntax diagnostics without normalizing the text."""
    issues = []

    def unmatched_pairs(opening, closing, code):
        stack = []
        for position, character in enumerate(text):
            if opening == closing:
                if character == opening:
                    if stack:
                        stack.pop()
                    else:
                        stack.append(position)
                continue
            if character == opening:
                stack.append(position)
            elif character == closing:
                if stack:
                    stack.pop()
                else:
                    issues.append((code, f"cierre {closing!r} sin apertura"))
        issues.extend((code, f"apertura {opening!r} sin cierre") for _ in stack)

    unmatched_pairs("{", "}", "braces")
    unmatched_pairs("&", "&", "variables")
    unmatched_pairs("$", "$", "dictionary_tokens")
    unmatched_pairs("[", "]", "delimiters")
    unmatched_pairs("【", "】", "delimiters")

    tags = _matches_with_spans(TAG_RE, text)
    # Count only prefixes that identify known markup. Arbitrary angle
    # brackets are visible localization content, not malformed tags.
    tag_prefixes = list(TAG_PREFIX_RE.finditer(text))
    if len(tag_prefixes) != len(tags):
        issues.append(("tags", "tag con < o > sin pareja"))

    stack = []
    self_closing_names = {"br", "sprite"}
    for tag, _, _ in tags:
        name = _tag_name(tag)
        if name is None:
            issues.append(("tags", f"tag no reconocible {tag!r}"))
            continue
        if tag.lstrip().startswith("</"):
            if not stack:
                issues.append(("tags", f"cierre {tag!r} sin apertura"))
            elif stack[-1] != name:
                issues.append(
                    ("tags", f"cierre {tag!r} no corresponde a <{stack[-1]}>")
                )
                if name in stack:
                    while stack and stack[-1] != name:
                        stack.pop()
                    if stack:
                        stack.pop()
                else:
                    stack.pop()
            else:
                stack.pop()
        elif tag.rstrip().endswith("/>") or name in self_closing_names:
            continue
        else:
            stack.append(name)
    issues.extend(("tags", f"tag <{name}> sin cierre") for name in stack)

    if text.endswith("\\"):
        issues.append(("escapes", "escape invertido final sin carácter"))
    return issues


def extract_signatures(text, file_name="LocalText.json"):
    """Extract ordered syntax signatures from a decoded localization value."""
    placeholder_spans = _matches_with_spans(PLACEHOLDER_RE, text)
    variable_spans = _matches_with_spans(VARIABLE_RE, text)
    dictionary_spans = _matches_with_spans(DICTIONARY_TOKEN_RE, text)
    tag_spans = _matches_with_spans(TAG_RE, text)
    all_spans = (
        [("placeholder", start, end) for _, start, end in placeholder_spans]
        + [("variable", start, end) for _, start, end in variable_spans]
        + [("dictionary_token", start, end) for _, start, end in dictionary_spans]
        + [("tag", start, end) for _, start, end in tag_spans]
    )

    placeholders = tuple(value for value, _, _ in placeholder_spans)
    role_tokens = ()
    if file_name == "RoleLogLocal.json":
        role_tokens = tuple(
            value
            for value in placeholders
            if value[1:-1].split("|", 1)[0] in ROLE_TOKENS
        )

    pipes = tuple(
        _context(position, all_spans)
        for position, character in enumerate(text)
        if character == "|"
    )
    percentages = tuple(
        _context(position, all_spans)
        for position, character in enumerate(text)
        if character == "%"
    )
    tags = tuple(value for value, _, _ in tag_spans)
    closures = tuple(value for value in tags if value.lstrip().startswith("</"))
    dictionary_tokens = tuple(value for value, _, _ in dictionary_spans)

    return {
        "placeholders": placeholders,
        "role_tokens": role_tokens,
        "variables": tuple(value for value, _, _ in variable_spans),
        "tokens": dictionary_tokens,
        "dictionary_tokens": dictionary_tokens,
        "tags": tags,
        "closures": closures,
        "delimiters": _delimiter_signature(text),
        "escapes": _escape_signature(text),
        "pipes": pipes,
        "percentages": percentages,
    }


SIGNATURE_FIELDS = (
    "placeholders",
    "role_tokens",
    "variables",
    "tokens",
    "tags",
    "closures",
    "delimiters",
    "escapes",
    "pipes",
    "percentages",
)


def compare_signatures(source_text, spanish_text, file_name):
    """Return signature fields whose required values differ.

    Placeholder expressions may move in a translated sentence. Their complete
    expressions and multiplicity must remain unchanged, while tag and escape
    order remains significant for the rendered result.
    """
    source = extract_signatures(source_text, file_name)
    spanish = extract_signatures(spanish_text, file_name)
    unordered_fields = {"placeholders", "role_tokens", "variables", "tokens"}

    def matches(field):
        if field in unordered_fields:
            return Counter(source[field]) == Counter(spanish[field])
        return source[field] == spanish[field]

    return [field for field in SIGNATURE_FIELDS if not matches(field)], source, spanish


def parse_chunk_spec(spec):
    """Parse 1-based chunk numbers and inclusive ranges."""
    selected = set()
    for part in re.split(r"[,\s]+", spec.strip()):
        if not part:
            continue
        match = re.fullmatch(r"(\d+)(?:\s*(?:-|\.\.|:)\s*(\d+))?", part)
        if not match:
            raise ValueError(f"selección de chunk inválida: {part!r}")
        first = int(match.group(1))
        last = int(match.group(2) or first)
        if first < 1 or last < first:
            raise ValueError(f"rango de chunks inválido: {part!r}")
        selected.update(range(first, last + 1))
    if not selected:
        raise ValueError("la selección de chunks está vacía")
    return selected


def build_chunks(entries, chunk_size):
    """Return 1-based chunk number to its zero-based source slice."""
    if chunk_size < 1:
        raise ValueError("chunk_size debe ser mayor que cero")
    return {
        number: entries[(number - 1) * chunk_size : number * chunk_size]
        for number in range(1, (len(entries) + chunk_size - 1) // chunk_size + 1)
    }


def _format_signature(signature):
    return repr(signature)


def _report_signature_difference(source_text, spanish_text, file_name):
    fields, source, spanish = compare_signatures(source_text, spanish_text, file_name)
    if not fields:
        return None
    details = "; ".join(
        f"{field}: espejo={_format_signature(source[field])}, "
        f"es={_format_signature(spanish[field])}"
        for field in fields
    )
    return details


def _is_incomplete_role_callignore(source_text, entry_id, file_name):
    """Recognize the documented source typo without approving other changes."""
    return (
        file_name == "RoleLogLocal.json"
        and entry_id == ROLE_INCOMPLETE_CALLIGNORE_EXCEPTION
        and source_text.startswith("callIgnore|C|A|1050|1051}")
    )


def validate_documents(
    mirror_data,
    spanish_data,
    file_name,
    mirror_path="espejo",
    spanish_path="español",
    chunk_size=400,
    selected_chunks=None,
    emit=None,
):
    """Validate two loaded documents and return ``(errors, warnings)``."""
    if emit is None:
        emit = print
    structural_field = "key" if file_name == "LocalText.json" else "keyID"
    source_text_field = "en"
    spanish_text_field = "es"

    errors = 0
    warnings = 0

    mirror_issues, mirror_by_id = validate_schema(
        mirror_data, mirror_path, file_name, "mirror"
    )
    spanish_issues, spanish_by_id = validate_schema(
        spanish_data, spanish_path, file_name, "spanish"
    )
    for issue in mirror_issues + spanish_issues:
        emit(f"{issue.severity}: {issue.message}")
        if issue.severity == "ERROR":
            errors += 1

    mirror_ids = set(mirror_by_id)
    spanish_ids = set(spanish_by_id)
    missing_ids = sorted(mirror_ids - spanish_ids, key=lambda value: int(value))
    extra_ids = sorted(spanish_ids - mirror_ids, key=lambda value: int(value))

    for entry_id in missing_ids:
        emit(f"ERROR: falta en español el id {entry_id} ({file_name})")
        errors += 1
    for entry_id in extra_ids:
        if file_name == "LocalText.json" and entry_id in ALLOWED_LOCALTEXT_EXTRA_IDS:
            emit(
                f"WARNING: excepción permitida: id español {entry_id} "
                "(entrada ui_game_spanish fuera del espejo)"
            )
            warnings += 1
        else:
            emit(f"ERROR: sobra en español el id {entry_id} ({file_name})")
            errors += 1

    common_ids = mirror_ids & spanish_ids
    for entry_id in sorted(common_ids, key=lambda value: int(value)):
        mirror_item = mirror_by_id[entry_id]
        spanish_item = spanish_by_id[entry_id]
        mirror_key = mirror_item.get(structural_field)
        spanish_key = spanish_item.get(structural_field)
        if isinstance(mirror_key, str) and isinstance(spanish_key, str) and mirror_key != spanish_key:
            emit(
                f"ERROR: id {entry_id}: {structural_field} no coincide "
                f"(espejo={mirror_key!r}, es={spanish_key!r})"
            )
            errors += 1

    if file_name == "LocalText.json" and LOCALTEXT_EMPTY_SOURCE_EXCEPTION in common_ids:
        mirror_item = mirror_by_id[LOCALTEXT_EMPTY_SOURCE_EXCEPTION]
        if mirror_item.get("en") == "":
            emit(
                "WARNING: excepción manual: LocalText id 24209 "
                "tiene valor vacío en el espejo; se informa sin exigir igualdad"
            )
            warnings += 1

    chunks = build_chunks(mirror_data if isinstance(mirror_data, list) else [], chunk_size)
    selected_chunks = set(chunks) if selected_chunks is None else set(selected_chunks)
    for chunk_number in sorted(selected_chunks):
        chunk_entries = chunks.get(chunk_number)
        if chunk_entries is None:
            emit(
                f"ERROR: chunk {chunk_number} fuera de rango "
                f"(1-{len(chunks)})"
            )
            errors += 1
            continue
        emit(
            f"CHUNK {chunk_number}/{len(chunks)}: "
            f"{len(chunk_entries)} entradas del espejo"
        )
        for source_index, mirror_item in enumerate(
            mirror_data[(chunk_number - 1) * chunk_size : chunk_number * chunk_size],
            start=(chunk_number - 1) * chunk_size,
        ):
            if not isinstance(mirror_item, dict):
                continue
            entry_id = mirror_item.get("id")
            entry_label = (
                f"índice {source_index + 1}, id {entry_id}, "
                f"{structural_field}={mirror_item.get(structural_field)!r}"
            )
            spanish_item = spanish_by_id.get(entry_id)
            if spanish_item is None:
                continue
            source_text = mirror_item.get(source_text_field)
            spanish_text = spanish_item.get(spanish_text_field)
            if not isinstance(source_text, str) or not isinstance(spanish_text, str):
                continue

            is_zero = file_name == "RoleLogLocal.json" and spanish_text == "0"
            is_24209 = (
                file_name == "LocalText.json"
                and entry_id == LOCALTEXT_EMPTY_SOURCE_EXCEPTION
                and source_text == ""
            )
            difference = _report_signature_difference(
                source_text,
                spanish_text,
                file_name,
            )
            if difference:
                if is_zero or is_24209:
                    emit(
                        f"WARNING: {entry_label}: "
                        f"comparación exceptuada ({'es=0' if is_zero else 'id 24209'}); "
                        f"firmas distintas: {difference}"
                    )
                    warnings += 1
                elif _is_incomplete_role_callignore(source_text, entry_id, file_name):
                    emit(
                        f"WARNING: {entry_label}: comparación exceptuada "
                        "por anomalía documentada de callIgnore en el espejo; "
                        f"firmas distintas: {difference}"
                    )
                    warnings += 1
                else:
                    emit(
                        f"ERROR: {entry_label}: "
                        f"firmas distintas: {difference}"
                    )
                    errors += 1
            elif is_zero:
                emit(
                    f"WARNING: {entry_label}: "
                    "es=0; se compara, pero requiere revisión manual"
                )
                warnings += 1

            source_syntax = _syntax_issues(source_text)
            spanish_syntax = _syntax_issues(spanish_text)
            source_signatures = extract_signatures(source_text, file_name)
            spanish_signatures = extract_signatures(spanish_text, file_name)
            syntax_signature_fields = {
                "braces": "placeholders",
                "variables": "variables",
                "dictionary_tokens": "tokens",
                "delimiters": "delimiters",
                "tags": "tags",
                "escapes": "escapes",
            }
            for code, detail in source_syntax:
                emit(
                    f"WARNING: {entry_label}: "
                    f"anomalía heredada del espejo [{code}]: {detail}"
                )
                warnings += 1
            if spanish_syntax:
                for code, detail in spanish_syntax:
                    syntax_field = syntax_signature_fields[code]
                    inherited = (
                        any(source_code == code for source_code, _ in source_syntax)
                        and source_signatures[syntax_field] == spanish_signatures[syntax_field]
                    )
                    if inherited:
                        emit(
                            f"WARNING: {entry_label}: "
                            f"anomalía heredada también presente en español [{code}]: {detail}"
                        )
                        warnings += 1
                    elif is_zero or is_24209:
                        emit(
                            f"WARNING: {entry_label}: "
                            f"sintaxis de es exceptuada [{code}]: {detail}"
                        )
                        warnings += 1
                    else:
                        emit(
                            f"ERROR: {entry_label}: "
                            f"regresión sintáctica española [{code}]: {detail}"
                        )
                        errors += 1

    emit(f"RESUMEN: errores={errors}, advertencias={warnings}")
    emit("RESULTADO: FALLÓ" if errors else "RESULTADO: OK")
    return errors, warnings


def _build_parser():
    parser = argparse.ArgumentParser(
        description="Valida chunks de LocalText.json o RoleLogLocal.json sin escribir archivos."
    )
    parser.add_argument("--file", choices=sorted(FILES), default="LocalText.json")
    parser.add_argument("--chunk-size", type=int, default=400, metavar="N")
    parser.add_argument(
        "--chunk",
        action="append",
        metavar="N[,M-N]",
        help="chunk(s) 1-based; admite listas y rangos, por ejemplo 1,3-4",
    )
    parser.add_argument(
        "--range",
        dest="chunk_range",
        action="append",
        metavar="N-M",
        help="rango inclusivo de chunks (alias explícito de un rango en --chunk)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="valida todos los chunks (también es el comportamiento predeterminado)",
    )
    return parser


def _select_chunks(args, chunk_count):
    if args.all and (args.chunk or args.chunk_range):
        raise ValueError("--all no se puede combinar con --chunk ni --range")
    if args.chunk_size < 1:
        raise ValueError("--chunk-size debe ser mayor que cero")
    if not args.chunk and not args.chunk_range:
        return set(range(1, chunk_count + 1))

    selected = set()
    for spec in (args.chunk or []) + (args.chunk_range or []):
        selected.update(parse_chunk_spec(spec))
    invalid = sorted(number for number in selected if number > chunk_count)
    if invalid:
        raise ValueError(
            f"chunk fuera de rango: {', '.join(map(str, invalid))}; "
            f"el rango válido es 1-{chunk_count}"
        )
    return selected


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.chunk_size < 1:
        parser.error("--chunk-size debe ser mayor que cero")

    scripts_dir = Path(__file__).resolve().parent
    root_dir = scripts_dir.parent
    file_name = args.file
    mirror_path = scripts_dir / "Output" / "Processed" / file_name
    spanish_path = (
        root_dir
        / "ModProject"
        / "ModCode"
        / "ModMain"
        / "Localization"
        / "Spanish"
        / file_name
    )

    try:
        mirror_data = load_json(mirror_path)
        spanish_data = load_json(spanish_path)
        mirror_count = len(mirror_data) if isinstance(mirror_data, list) else 0
        chunk_count = (mirror_count + args.chunk_size - 1) // args.chunk_size
        selected = _select_chunks(args, chunk_count)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: no se pudieron preparar los archivos: {error}")
        return 2

    print(f"Archivo: {file_name}")
    print(f"Espejo: {mirror_path}")
    print(f"Español: {spanish_path}")
    print(f"Chunk size: {args.chunk_size}; chunks seleccionados: {', '.join(map(str, sorted(selected)))}")
    errors, _ = validate_documents(
        mirror_data,
        spanish_data,
        file_name,
        mirror_path=mirror_path,
        spanish_path=spanish_path,
        chunk_size=args.chunk_size,
        selected_chunks=selected,
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
