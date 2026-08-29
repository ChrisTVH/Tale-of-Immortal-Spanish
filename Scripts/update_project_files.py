#!/usr/bin/env python3
"""
Script para actualizar los archivos de localización del proyecto.
Añade entradas faltantes desde Scripts/Output/Processed/ a
ModProject/ModCode/ModMain/Localization/Spanish/.
"""

import argparse
import json
import os
import re
import tempfile
from pathlib import Path


class ValidationError(ValueError):
    """Raised when a project JSON file has an unsafe structure."""


def to_localization_entry(item):
    """Convert a processed source entry into the Spanish resource schema."""
    localization_item = dict(item)
    localization_item["es"] = localization_item.pop("en")
    return localization_item


def write_json_atomically(output_path, data):
    """Write JSON through a sibling temporary file and replace the target."""
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


def natural_sort_key(text):

    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(c) for c in re.split('([0-9]+)', text)]


def _id_key(value):
    """Return a comparable key for a JSON scalar ID."""
    try:
        hash(value)
    except TypeError as exc:
        raise ValidationError(
            "los IDs deben ser valores simples, no listas u objetos"
        ) from exc

    return (type(value).__name__, value)


def validate_entries(data, id_field, path, required_fields=()):
    """Validate entries, required fields, IDs and duplicate IDs."""
    if not isinstance(data, list):
        raise ValidationError(f"{path} debe contener una lista JSON")

    seen_ids = {}
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValidationError(
                f"{path}: la entrada {index} debe ser un objeto JSON"
            )

        if id_field not in item or item[id_field] is None:
            raise ValidationError(
                f"{path}: la entrada {index} no contiene un ID válido ({id_field})"
            )
        if not isinstance(item[id_field], str) or not item[id_field].isdigit():
            raise ValidationError(
                f"{path}: la entrada {index} tiene un ID no numérico ({id_field})"
            )

        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ValidationError(
                f"{path}: la entrada {index} no contiene los campos: {fields}"
            )

        for field in required_fields:
            if field != id_field and not isinstance(item[field], str):
                raise ValidationError(
                    f"{path}: el campo {field!r} de la entrada {index} debe ser texto"
                )

        try:
            item_id = _id_key(item[id_field])
        except ValidationError as exc:
            raise ValidationError(
                f"{path}: la entrada {index} tiene un ID no válido ({id_field})"
            ) from exc

        if item_id in seen_ids:
            previous_index = seen_ids[item_id]
            raise ValidationError(
                f"{path}: ID duplicado {item[id_field]!r} en las entradas "
                f"{previous_index} y {index}"
            )

        seen_ids[item_id] = index

    return seen_ids


def find_structural_conflicts(
    main_data, new_data, id_field, structural_field, main_path, output_path
):
    """Find changed structural keys without comparing translatable text."""
    if structural_field is None:
        return []

    main_by_id = {_id_key(item[id_field]): item for item in main_data}
    conflicts = []

    for index, item in enumerate(new_data):
        item_id = _id_key(item[id_field])
        existing_item = main_by_id.get(item_id)
        if existing_item is None:
            continue

        if (
            structural_field in item or structural_field in existing_item
        ) and item.get(structural_field) != existing_item.get(structural_field):
            conflicts.append(
                f"Conflicto estructural para id {item[id_field]!r} en "
                f"{structural_field} (entrada {index} de {output_path.name}, "
                f"destino {main_path.name})"
            )

    return conflicts


def merge_entries(main_data, new_data, id_field="id", sort_key=None):

    validate_entries(main_data, id_field, "destino")
    validate_entries(new_data, id_field, "entrada")

    existing_ids = {
        _id_key(item[id_field])
        for item in main_data
    }

    new_entries = [
        item
        for item in new_data
        if _id_key(item[id_field]) not in existing_ids
    ]

    if sort_key and new_entries:
        main_keys = [sort_key(item) for item in main_data]
        new_keys = [sort_key(item) for item in new_entries]
        if main_keys == sorted(main_keys) and new_keys == sorted(new_keys):
            merged_data = []
            main_index = 0
            new_index = 0

            while main_index < len(main_data) and new_index < len(new_entries):
                if new_keys[new_index] < main_keys[main_index]:
                    merged_data.append(new_entries[new_index])
                    new_index += 1
                else:
                    merged_data.append(main_data[main_index])
                    main_index += 1

            merged_data.extend(main_data[main_index:])
            merged_data.extend(new_entries[new_index:])
            main_data[:] = merged_data
            return main_data, len(new_entries)

    added_count = 0

    for item in new_data:
        item_id = _id_key(item[id_field])
        if item_id not in existing_ids:
            if sort_key:

                item_sort_value = sort_key(item)
                insert_pos = 0

                for i, existing_item in enumerate(main_data):
                    if sort_key(existing_item) > item_sort_value:
                        insert_pos = i
                        break
                    insert_pos = i + 1

                main_data.insert(insert_pos, item)
            else:
                main_data.append(item)

            existing_ids.add(item_id)
            added_count += 1

    return main_data, added_count


def _load_and_validate(
    output_path,
    main_path,
    id_field,
    structural_field=None,
    required_fields=(),
    main_required_fields=None,
):
    with open(output_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    with open(main_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    validate_entries(new_data, id_field, str(output_path), required_fields)
    validate_entries(
        main_data,
        id_field,
        str(main_path),
        required_fields if main_required_fields is None else main_required_fields,
    )

    conflicts = find_structural_conflicts(
        main_data,
        new_data,
        id_field,
        structural_field,
        main_path,
        output_path,
    )
    if conflicts:
        raise ValidationError("; ".join(conflicts))

    return new_data, main_data


def _update_file(
    output_path,
    main_path,
    filename,
    id_field="id",
    structural_field=None,
    required_fields=(),
    main_required_fields=None,
    sort_key=None,
    entry_transform=None,
    dry_run=False,
):
    print(f"\nINFO: Procesando {filename}")

    new_data, main_data = _load_and_validate(
        output_path,
        main_path,
        id_field,
        structural_field,
        required_fields,
        main_required_fields,
    )

    if entry_transform is not None:
        new_data = [entry_transform(item) for item in new_data]

    merged_data, added = merge_entries(
        main_data,
        new_data,
        id_field=id_field,
        sort_key=sort_key,
    )

    if not dry_run:
        write_json_atomically(main_path, merged_data)

    if dry_run:
        print(f"   DRY-RUN: se añadirían {added} entradas")
    else:
        print(f"   OK: {added} entradas añadidas")
    print(f"   Total de entradas: {len(merged_data)}")

    return added


def update_local_text(output_path, main_path, dry_run=False):
    return _update_file(
        output_path,
        main_path,
        "LocalText.json",
        structural_field="key",
        required_fields=("id", "key", "en"),
        main_required_fields=("id", "key", "es"),
        sort_key=lambda x: natural_sort_key(x.get("key", "")),
        entry_transform=to_localization_entry,
        dry_run=dry_run,
    )


def update_role_log_local(output_path, main_path, dry_run=False):
    return _update_file(
        output_path,
        main_path,
        "RoleLogLocal.json",
        structural_field="keyID",
        required_fields=("id", "keyID", "en"),
        main_required_fields=("id", "keyID", "es"),
        sort_key=lambda x: natural_sort_key(x.get("keyID", "")),
        entry_transform=to_localization_entry,
        dry_run=dry_run,
    )


def update_simple_file(output_path, main_path, filename, dry_run=False):
    return _update_file(
        output_path,
        main_path,
        filename,
        required_fields=("id", "en"),
        main_required_fields=("id", "es"),
        entry_transform=to_localization_entry,
        dry_run=dry_run,
    )


def build_files_config(output_dir, localization_dir):
    return [
        {
            "filename": "LocalText.json",
            "output": output_dir / "LocalText.json",
            "main": localization_dir / "LocalText.json",
            "id_field": "id",
            "structural_field": "key",
            "required_fields": ("id", "key", "en"),
            "main_required_fields": ("id", "key", "es"),
            "sort_key": lambda x: natural_sort_key(x.get("key", "")),
            "entry_transform": to_localization_entry,
        },
        {
            "filename": "RoleLogLocal.json",
            "output": output_dir / "RoleLogLocal.json",
            "main": localization_dir / "RoleLogLocal.json",
            "id_field": "id",
            "structural_field": "keyID",
            "required_fields": ("id", "keyID", "en"),
            "main_required_fields": ("id", "keyID", "es"),
            "sort_key": lambda x: natural_sort_key(x.get("keyID", "")),
            "entry_transform": to_localization_entry,
        },
        {
            "filename": "BattleSkillPrefixName.json",
            "output": output_dir / "BattleSkillPrefixName.json",
            "main": localization_dir / "Prefixes" / "BattleSkillPrefixName.json",
            "id_field": "id",
            "structural_field": None,
            "required_fields": ("id", "en"),
            "main_required_fields": ("id", "es"),
            "sort_key": None,
            "entry_transform": to_localization_entry,
        },
        {
            "filename": "NpcNameFirst.json",
            "output": output_dir / "NpcNameFirst.json",
            "main": localization_dir / "Npcs" / "NpcNameFirst.json",
            "id_field": "id",
            "structural_field": None,
            "required_fields": ("id", "en"),
            "main_required_fields": ("id", "es"),
            "sort_key": None,
            "entry_transform": to_localization_entry,
        },
        {
            "filename": "NpcNameLast.json",
            "output": output_dir / "NpcNameLast.json",
            "main": localization_dir / "Npcs" / "NpcNameLast.json",
            "id_field": "id",
            "structural_field": None,
            "required_fields": ("id", "en"),
            "main_required_fields": ("id", "es"),
            "sort_key": None,
            "entry_transform": to_localization_entry,
        },
        {
            "filename": "HerdNPCNameFirst.json",
            "output": output_dir / "HerdNPCNameFirst.json",
            "main": localization_dir / "Npcs" / "HerdNPCNameFirst.json",
            "id_field": "id",
            "structural_field": None,
            "required_fields": ("id", "en"),
            "main_required_fields": ("id", "es"),
            "sort_key": None,
            "entry_transform": to_localization_entry,
        }
    ]


def validate_configured_files(files_config):
    valid_configs = []
    had_errors = False

    for config in files_config:
        output_path = config["output"]
        main_path = config["main"]

        if not output_path.exists():
            had_errors = True
            print(f"\nWARNING: {output_path.name} no encontrado en {output_path.parent}")
            print("   Saltando este archivo...")
            continue

        if not main_path.exists():
            had_errors = True
            print(f"\nWARNING: {main_path} no encontrado")
            print("   Saltando este archivo...")
            continue

        try:
            _load_and_validate(
                output_path,
                main_path,
                config["id_field"],
                config["structural_field"],
                config["required_fields"],
                config["main_required_fields"],
            )
            valid_configs.append(config)

        except json.JSONDecodeError as e:
            print("\nERROR: Archivo JSON inválido")
            print(f"  Detalle: {e}")
            had_errors = True
        except (OSError, TypeError, ValueError) as e:
            print("\nERROR procesando archivo")
            print(f"  Detalle: {e}")
            had_errors = True

    return valid_configs, had_errors


def update_configured_files(valid_configs, dry_run):
    total_added = 0
    had_errors = False

    for config in valid_configs:
        try:
            total_added += _update_file(
                config["output"],
                config["main"],
                config["filename"],
                id_field=config["id_field"],
                structural_field=config["structural_field"],
                required_fields=config["required_fields"],
                main_required_fields=config["main_required_fields"],
                sort_key=config["sort_key"],
                entry_transform=config["entry_transform"],
                dry_run=dry_run,
            )
        except OSError as e:
            print("\nERROR escribiendo archivo")
            print(f"  Detalle: {e}")
            had_errors = True

    return total_added, had_errors


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Actualiza los archivos principales del proyecto."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="informa de las entradas nuevas sin modificar la localización del proyecto",
    )
    args = parser.parse_args(argv)

    print("=" * 70)
    print("Actualizando archivos principales del proyecto")
    print("=" * 70)

    if args.dry_run:
        print("Modo dry-run: no se modificarán archivos de localización")

    scripts_dir = Path(__file__).resolve().parent
    output_dir = scripts_dir / "Output" / "Processed"
    localization_dir = (
        scripts_dir.parent
        / "ModProject"
        / "ModCode"
        / "ModMain"
        / "Localization"
        / "Spanish"
    )

    if not output_dir.is_dir():
        print(f"\nERROR: No se encuentra el directorio {output_dir}")
        print("   Ejecuta primero process_json_files.py")
        return 1

    if not localization_dir.is_dir():
        print(f"\nERROR: No se encuentra el directorio {localization_dir}")
        print("   Verifica la estructura de carpetas del proyecto")
        return 1

    files_config = build_files_config(output_dir, localization_dir)
    valid_configs, validation_errors = validate_configured_files(files_config)
    if validation_errors:
        print("\nERROR: No se realizaron cambios por errores de validación")
        return 1

    total_added, update_errors = update_configured_files(
        valid_configs, args.dry_run
    )

    print("\n" + "=" * 70)
    if update_errors:
        print("Actualización terminada con errores")
    elif args.dry_run:
        print("Simulación completada")
        print(f"Total de entradas que se añadirían: {total_added}")
    else:
        print("Actualización completada")
        print(f"Total de entradas añadidas: {total_added}")
    print("=" * 70)

    return 1 if update_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
