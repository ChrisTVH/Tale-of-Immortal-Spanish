# Tale of Immortal - Traducción al español

Mod de localización que traduce al español el texto del juego **Tale of Immortal** (鬼谷八荒).

El mod carga los archivos JSON como recursos integrados en una DLL de C# y aplica la traducción mediante parches de localización. En la configuración de idioma del juego aparece como una opción independiente de español.

## Estado

- **Versión del juego:** `v1.2.113.259`
- **Última actualización de contenido:** `06/02/2026`

## Instalación y uso

El mod está disponible en los canales oficiales:

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3646970035)
- [Releases de GitHub](https://github.com/ChrisTVH/TL-Spanish/releases)

Después de instalarlo, abre la configuración de idioma del juego y selecciona **Español**. La selección se conserva para usos posteriores.

Al activar el mod, es necesario reiniciar el juego para que el idioma cambie por completo.

Para consultar dudas o problemas frecuentes, visita la [wiki del proyecto](https://github.com/ChrisTVH/TL-Spanish/wiki/Problemas-frecuentes).

## Archivos de traducción

Los recursos de localización se encuentran en `ModProject/ModCode/ModMain/Localization/Spanish/`:

| Archivo | Descripción |
|---------|-------------|
| `LocalText.json` | Interfaz general del juego |
| `RoleLogLocal.json` | Registros de personajes |
| `Npcs/NpcNameFirst.json` | Nombres de pila de NPCs |
| `Npcs/NpcNameLast.json` | Apellidos de NPCs |
| `Npcs/HerdNPCNameFirst.json` | Nombres de NPCs |
| `Prefixes/BattleSkillPrefixName.json` | Prefijos de habilidades de combate |

Los nombres de `Npcs/` y `Prefixes/` se mantienen como pinyin o transliteración del juego.

## Estructura del proyecto

```text
Scripts/
├── Default/                  # Archivos originales de entrada
└── Output/Processed/         # Archivos procesados y validados

ModProject/ModCode/ModMain/
├── Localization/Spanish/     # Recursos de la traducción
└── bin/Release/              # DLL compilada
```

## Actualizar archivos de traducción

Los archivos originales pueden encontrarse en la carpeta raíz del juego siguiendo esta ruta:
`\Mod\modFQA\配置修改教程\配置（只读）Json格式\`.

Copia los archivos de entrada en `Scripts/Default/` y ejecuta los scripts desde la raíz del repositorio:

```bash
python3 Scripts/process_json_files.py --dry-run
python3 Scripts/process_json_files.py

python3 Scripts/update_project_files.py --dry-run
python3 Scripts/update_project_files.py

python3 Scripts/build_global_metadata_candidates.py --dry-run
python3 Scripts/build_global_metadata_candidates.py
```

`process_json_files.py` valida y transforma los archivos en `Scripts/Output/Processed/`. Después, `update_project_files.py` incorpora las entradas nuevas a `Localization/Spanish/`. Este último script no reemplaza automáticamente las traducciones existentes.

`build_global_metadata_candidates.py` actualiza el catálogo editable `GlobalMetadata.json` con los literales chinos no vinculados a una tabla de configuración y genera `GlobalMetadata.runtime.json` con las entradas que ya tienen traducción. El mod solo incorpora este último recurso para no cargar candidatos pendientes en runtime.

## Compilar el mod

La compilación requiere `dotnet`, .NET Framework 4.7.2 y las bibliotecas de MelonLoader y del juego. Si la ruta del juego no coincide con la configurada en el proyecto, indícala mediante `GameRoot`:

```bash
python3 build.py /p:GameRoot="RUTA_AL_JUEGO"
```

La DLL se genera en:

```text
ModProject/ModCode/ModMain/bin/Release/MOD_pzAi9g.dll
```

## Contribuir

Puedes [abrir un issue](https://github.com/ChrisTVH/TL-Spanish/issues) para reportar errores gramaticales, incoherencias o problemas de visualización, o enviar una pull request al repositorio principal.

Antes de contribuir, consulta las [reglas de traducción](translation_guidelines.md), el [glosario](glossary.md) y la [licencia](LICENSE.md). Conserva los identificadores, las claves, los placeholders, las etiquetas y los espacios intencionales. Las aportaciones directas pueden añadirse a la cadena de créditos `ID | 22170 |`.
