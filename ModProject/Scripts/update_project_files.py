#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar archivos principales del proyecto
Añade entradas faltantes desde Output/ a ModExcel/
"""

import json
import os
import re
from pathlib import Path


def natural_sort_key(text):

    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(c) for c in re.split('([0-9]+)', text)]


def merge_entries(main_data, new_data, id_field="id", sort_key=None):

    existing_ids = {item.get(id_field) for item in main_data}

    added_count = 0

    for item in new_data:
        item_id = item.get(id_field)
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


def update_local_text(output_path, main_path):

    print(f"\n📝 Procesando: LocalText.json")

    with open(output_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    with open(main_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    merged_data, added = merge_entries(
        main_data,
        new_data,
        id_field="id",
        sort_key=lambda x: natural_sort_key(x.get("key", ""))
    )

    with open(main_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ {added} entradas añadidas")
    print(f"   📊 Total de entradas: {len(merged_data)}")

    return added


def update_role_log_local(output_path, main_path):

    print(f"\n📝 Procesando: RoleLogLocal.json")

    with open(output_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    with open(main_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    merged_data, added = merge_entries(
        main_data,
        new_data,
        id_field="id",
        sort_key=lambda x: natural_sort_key(x.get("keyID", ""))
    )

    with open(main_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ {added} entradas añadidas")
    print(f"   📊 Total de entradas: {len(merged_data)}")

    return added


def update_simple_file(output_path, main_path, filename):

    print(f"\n📝 Procesando: {filename}")

    with open(output_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    with open(main_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    merged_data, added = merge_entries(
        main_data,
        new_data,
        id_field="id",
        sort_key=None
    )

    with open(main_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"   ✅ {added} entradas añadidas")
    print(f"   📊 Total de entradas: {len(merged_data)}")

    return added


def main():

    print("=" * 70)
    print("Actualizando archivos principales del proyecto")
    print("=" * 70)

    output_dir = Path("Output")
    mod_excel_dir = Path("../ModExcel")

    if not output_dir.exists():
        print(f"\n❌ ERROR: No se encuentra el directorio {output_dir}")
        print(f"   Asegúrate de ejecutar el script desde la carpeta Scripts/")
        return

    if not mod_excel_dir.exists():
        print(f"\n❌ ERROR: No se encuentra el directorio {mod_excel_dir}")
        print(f"   Verifica la estructura de carpetas del proyecto")
        return

    total_added = 0

    files_config = [
        {
            "output": output_dir / "LocalText.json",
            "main": mod_excel_dir / "LocalText.json",
            "function": update_local_text
        },
        {
            "output": output_dir / "RoleLogLocal.json",
            "main": mod_excel_dir / "RoleLogLocal.json",
            "function": update_role_log_local
        },
        {
            "output": output_dir / "BattleSkillPrefixName.json",
            "main": mod_excel_dir / "Prefixes" / "BattleSkillPrefixName.json",
            "function": lambda o, m: update_simple_file(o, m, "BattleSkillPrefixName.json")
        },
        {
            "output": output_dir / "NpcNameFirst.json",
            "main": mod_excel_dir / "Npcs" / "NpcNameFirst.json",
            "function": lambda o, m: update_simple_file(o, m, "NpcNameFirst.json")
        },
        {
            "output": output_dir / "NpcNameLast.json",
            "main": mod_excel_dir / "Npcs" / "NpcNameLast.json",
            "function": lambda o, m: update_simple_file(o, m, "NpcNameLast.json")
        },
        {
            "output": output_dir / "HerdNPCNameFirst.json",
            "main": mod_excel_dir / "Npcs" / "HerdNPCNameFirst.json",
            "function": lambda o, m: update_simple_file(o, m, "HerdNPCNameFirst.json")
        }
    ]

    for config in files_config:
        output_path = config["output"]
        main_path = config["main"]
        process_func = config["function"]

        if not output_path.exists():
            print(f"\n⚠️  ADVERTENCIA: {output_path.name} no encontrado en Output/")
            print(f"   Saltando este archivo...")
            continue

        if not main_path.exists():
            print(f"\n⚠️  ADVERTENCIA: {main_path} no encontrado")
            print(f"   Saltando este archivo...")
            continue

        try:
            added = process_func(output_path, main_path)
            total_added += added

        except json.JSONDecodeError as e:
            print(f"\n❌ ERROR: Archivo JSON inválido")
            print(f"   Detalle: {e}")
        except Exception as e:
            print(f"\n❌ ERROR procesando archivo")
            print(f"   Detalle: {e}")

    print("\n" + "=" * 70)
    print(f"✨ Actualización completada")
    print(f"📊 Total de entradas añadidas: {total_added}")
    print("=" * 70)


if __name__ == "__main__":
    main()
