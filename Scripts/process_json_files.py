#!/usr/bin/env python3
"""
Script para procesar los archivos de traducción en JSON.
Lee Scripts/Default/ y escribe en Scripts/Output/Processed/.
Realiza limpieza de llaves, renombrado y ordenamiento alfabético.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


def natural_sort_key(text):

    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(c) for c in re.split("([0-9]+)", text)]


def validate_schema(data, schema_name, required_fields, text_fields):
    if not isinstance(data, list):
        raise ValueError(f"{schema_name}: la raíz del JSON debe ser una lista")

    seen_ids = set()
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(
                f"{schema_name}: la entrada {index} debe ser un objeto JSON"
            )

        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ValueError(
                f"{schema_name}: la entrada {index} no contiene los campos: {fields}"
            )

        if not isinstance(item["id"], str) or not item["id"].isdigit():
            raise ValueError(
                f"{schema_name}: la entrada {index} tiene un id no numérico"
            )

        try:
            duplicate_id = item["id"] in seen_ids
        except TypeError as exc:
            raise ValueError(
                f"{schema_name}: la entrada {index} tiene un id no válido"
            ) from exc

        if duplicate_id:
            raise ValueError(
                f"{schema_name}: id duplicado en la entrada {index}: {item['id']!r}"
            )
        seen_ids.add(item["id"])

        for field in text_fields:
            if not isinstance(item[field], str):
                raise ValueError(
                    f"{schema_name}: el campo {field!r} de la entrada {index} debe ser texto"
                )


def process_local_text(data):

    validate_schema(data, "LocalText", ("id", "key", "ch"), ("key", "ch"))

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "key": item.get("key"),
            "en": item.get("ch", ""),
        }
        processed.append(new_item)

    processed.sort(key=lambda x: natural_sort_key(x.get("key", "")))

    return processed


def process_role_log_local(data):

    validate_schema(
        data, "RoleLogLocal", ("id", "keyID", "ch"), ("keyID", "ch")
    )

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "keyID": item.get("keyID"),
            "en": item.get("ch", ""),
        }
        processed.append(new_item)

    processed.sort(key=lambda x: natural_sort_key(x.get("keyID", "")))

    return processed


def process_npc_name_first(data):

    validate_schema(data, "NpcNameFirst", ("id", "name"), ("name",))

    processed = []

    for item in data:
        new_item = {"id": item.get("id"), "en": item.get("name", "")}
        processed.append(new_item)

    return processed


def process_npc_name_last(data):

    validate_schema(data, "NpcNameLast", ("id", "name"), ("name",))

    processed = []

    for item in data:
        new_item = {"id": item.get("id"), "en": item.get("name", "")}
        processed.append(new_item)

    return processed


def process_herd_npc_name_first(data):

    validate_schema(data, "HerdNPCNameFirst", ("id", "name"), ("name",))

    processed = []

    for item in data:
        new_item = {"id": item.get("id"), "en": item.get("name", "")}
        processed.append(new_item)

    return processed


def process_battle_skill_prefix_name(data):

    validate_schema(
        data, "BattleSkillPrefixName", ("id", "text"), ("text",)
    )

    processed = []

    for item in data:
        new_item = {"id": item.get("id"), "en": item.get("text", "")}
        processed.append(new_item)

    return processed


def write_json_atomically(output_path, data):
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, ensure_ascii=False, indent=2)
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Procesa los archivos de traducción en JSON."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="valida y procesa sin escribir archivos",
    )
    args = parser.parse_args(argv)

    scripts_dir = Path(__file__).resolve().parent
    default_dir = scripts_dir / "Default"
    output_dir = scripts_dir / "Output" / "Processed"

    files_to_process = {
        "LocalText.json": process_local_text,
        "RoleLogLocal.json": process_role_log_local,
        "NpcNameFirst.json": process_npc_name_first,
        "NpcNameLast.json": process_npc_name_last,
        "HerdNPCNameFirst.json": process_herd_npc_name_first,
        "BattleSkillPrefixName.json": process_battle_skill_prefix_name,
    }

    print("=" * 60)
    print("Iniciando procesamiento de archivos JSON")
    print("=" * 60)

    had_errors = False
    validated_files = []

    for filename, process_function in files_to_process.items():
        input_path = default_dir / filename
        output_path = output_dir / filename

        if not input_path.exists():
            had_errors = True
            print(f"\nWARNING: {filename} no encontrado en {default_dir}")
            print("   Saltando este archivo...")
            continue

        try:
            print(f"\nINFO: Leyendo {filename}")
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"INFO: Procesando {filename}")
            processed_data = process_function(data)
            validated_files.append(
                (
                    filename,
                    input_path,
                    output_path,
                    process_function,
                    len(processed_data),
                )
            )

        except json.JSONDecodeError as e:
            had_errors = True
            print(f"ERROR: {filename} no es un JSON válido")
            print(f"  Detalle: {e}")
        except Exception as e:
            had_errors = True
            print(f"ERROR procesando {filename}")
            print(f"  Detalle: {e}")

    if had_errors:
        print("\nERROR: No se escribieron archivos por errores de validación")
    elif args.dry_run:
        for filename, _, output_path, _, entry_count in validated_files:
            print(f"DRY-RUN: no se escribirá {output_path}")
            print(f"OK: {filename} validado ({entry_count} entradas)")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, input_path, output_path, process_function, _ in validated_files:
            try:
                with open(input_path, "r", encoding="utf-8") as f:
                    processed_data = process_function(json.load(f))
                print(f"INFO: Guardando {filename}")
                write_json_atomically(output_path, processed_data)
                print(f"OK: {filename} completado ({len(processed_data)} entradas)")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                had_errors = True
                print(f"ERROR escribiendo {filename}")
                print(f"  Detalle: {e}")

    print("\n" + "=" * 60)
    if had_errors:
        print("Procesamiento finalizado con errores")
    elif args.dry_run:
        print("Simulación completada; no se escribieron archivos")
    else:
        print("Procesamiento completado")
        print(f"Archivos guardados en: {output_dir}")
    print("=" * 60)
    return 1 if had_errors else 0


if __name__ == "__main__":
    sys.exit(main())
