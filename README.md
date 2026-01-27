# Tale of Immortal - Traducción al Español

Mod de localización que traduce el texto del juego "Tale of Immortal" (鬼谷八荒)
del chino al español.

Este mod funciona de tal manera que sobreescribe el idioma inglés al español.

También se podrían traducir las imágenes al español, pero si viste el
"ModProjectPreview.png" te darás cuenta de que tengo cero habilidad con ello.

¿Tiene dudas o problemas sobre el juego? [Vea aquí](https://github.com/ChrisTVH/Tale-of-Immortal-Spanish/wiki/Problemas-frecuentes).

## Archivos de Traducción - v1.2.112.259 - 26/01/2026

| Archivo | Descripción |
|---------|-------------|
| `ModExcel/LocalText.json` | Interfaz general del juego |
| `ModExcel/RoleLogLocal.json` | Registros de personajes |
| `ModExcel/Npcs/NpcNameFirst.json` | Nombres de pila de NPCs |
| `ModExcel/Npcs/NpcNameLast.json` | Apellidos de NPCs |
| `ModExcel/Npcs/HerdNPCNameFirst.json` | Nombres de NPCs de manada |
| `ModExcel/Prefixes/BattleSkillPrefixName.json` | Prefijos de habilidades de combate |

## ¿Cómo contribuir al proyecto?

Puedes abrir un [**Issue**](https://github.com/ChrisTVH/Tale-of-Immortal-Spanish/issues) y reportar fallos gramaticales o incoherencias;
también puedes hacer un **Fork** y enviar [**Pull requests**](https://github.com/ChrisTVH/Tale-of-Immortal-Spanish/pulls) con tus propias
correcciones.

Puedes encontrar los archivos de localización originales desde la carpeta raíz
del juego siguiendo esta ruta: "`\Mod\modFQA\配置修改教程\配置（只读）Json格式\`".

En el proyecto las herramientas se guardan en `ModProject/Scripts/` puedes añadir los archivos
originales a la carpeta `Default` y procesarlos con **process_json_files.py** y añadir las
nuevas entradas al proyecto principal con **update_project_files.py**.

Los que hagan aportaciones directas podrán ser añadidos a la cadena `ID | 22170 |`.