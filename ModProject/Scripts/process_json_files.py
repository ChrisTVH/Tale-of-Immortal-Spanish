#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para procesar los archivos de traducción en JSON
Realiza limpieza de llaves, renombrado y ordenamiento alfabético
"""

import json
import os
import re
from pathlib import Path


def natural_sort_key(text):

    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(c) for c in re.split('([0-9]+)', text)]


def process_local_text(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "key": item.get("key"),
            "en": item.get("ch", "")
        }
        processed.append(new_item)

    processed.sort(key=lambda x: natural_sort_key(x.get("key", "")))

    return processed


def process_role_log_local(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "keyID": item.get("keyID"),
            "en": item.get("ch", "")
        }
        processed.append(new_item)

    processed.sort(key=lambda x: natural_sort_key(x.get("keyID", "")))

    return processed


def process_npc_name_first(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "en": item.get("name", "")
        }
        processed.append(new_item)

    return processed


def process_npc_name_last(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "en": item.get("name", "")
        }
        processed.append(new_item)

    return processed


def process_herd_npc_name_first(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "en": item.get("name", "")
        }
        processed.append(new_item)

    return processed


def process_battle_skill_prefix_name(data):

    processed = []

    for item in data:
        new_item = {
            "id": item.get("id"),
            "en": item.get("text", "")
        }
        processed.append(new_item)

    return processed


def main():

    default_dir = Path("Default")
    output_dir = Path("Output")

    output_dir.mkdir(parents=True, exist_ok=True)

    files_to_process = {
        "LocalText.json": process_local_text,
        "RoleLogLocal.json": process_role_log_local,
        "NpcNameFirst.json": process_npc_name_first,
        "NpcNameLast.json": process_npc_name_last,
        "HerdNPCNameFirst.json": process_herd_npc_name_first,
        "BattleSkillPrefixName.json": process_battle_skill_prefix_name
    }

    print("=" * 60)
    print("Iniciando procesamiento de archivos JSON")
    print("=" * 60)

    for filename, process_function in files_to_process.items():
        input_path = default_dir / filename
        output_path = output_dir / filename

        if not input_path.exists():
            print(f"\n⚠️  ADVERTENCIA: {filename} no encontrado en {default_dir}")
            print(f"   Saltando este archivo...")
            continue

        try:
            print(f"\n📖 Leyendo: {filename}")
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"⚙️  Procesando: {filename}")
            processed_data = process_function(data)

            print(f"💾 Guardando: {filename}")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)

            print(f"✅ Completado: {filename} ({len(processed_data)} entradas)")

        except json.JSONDecodeError as e:
            print(f"❌ ERROR: {filename} no es un JSON válido")
            print(f"   Detalle: {e}")
        except Exception as e:
            print(f"❌ ERROR procesando {filename}")
            print(f"   Detalle: {e}")

    print("\n" + "=" * 60)
    print("✨ Procesamiento completado")
    print(f"📁 Archivos guardados en: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
