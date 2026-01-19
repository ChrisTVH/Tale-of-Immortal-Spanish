# Tale of Immortal Spanish Mod - Agent Guide

Spanish translation mod for "Tale of Immortal" (鬼谷八荒). JSON localization files that translate game text from Chinese to Spanish.

## Build/Development Commands

### Validation (Lint)
```bash
# Validate all JSON files
for file in **/*.json; do jq empty "$file" && echo "✓ $file valid" || echo "✗ $file error"; done

# Validate single file
jq empty LocalText.json && echo "✓ LocalText.json valid"

# Check for duplicate IDs
jq 'group_by(.id) | map(select(length > 1)) | length' LocalText.json
```

### Testing Translations (Test)
```bash
# Run single test: validate JSON syntax
jq empty LocalText.json && echo "✓ LocalText.json valid"

# Count entries in file
jq 'length' LocalText.json

# Validate UTF-8 encoding
iconv -f UTF-8 -t UTF-8 LocalText.json > /dev/null && echo "✓ encoding OK"
```

### File Organization
```bash
# List JSON files by size
ls -la **/*.json | sort -k5 -n
```

## Code Style Guidelines

### JSON Structure Standards

1. **File Format**: Valid JSON arrays of objects
2. **Object Structure**:
   - `id`: Unique identifier (string, quotes required)
   - `key`: Translation key (string, snake_case)
   - `en`: Spanish translation (string, UTF-8)

```json
[
  {
    "id": "1",
    "key": "common_shi",
    "en": "Sí"
  }
]
```

### Formatting

- 2-space indentation, no trailing whitespace, LF line endings
- IDs as strings (not integers) per existing convention
- Keys in snake_case, descriptive and unique
- Objects ordered alphabetically by `key` (LocalText.json) or `keyID` (RoleLogLocal.json)

### Translation Guidelines

- UTF-8 encoding without BOM
- Spanish characters: á, é, í, ó, ú, ü, ñ, Ñ, ¿, ¡
- Keep translations concise for UI space
- Use consistent gaming terminology
- **Preserve game tags**: Always keep `<r>`, `<g>`, `<b>`, `<color>`, `</color>`, `<size>`, `</size>`, `<align>`, `</align>`, `<indent>`, `</indent>`, `<y>`, `</y>` tags in translations as they format game text (colors, sizes, alignment, indentation, highlighting)
- **Grammar corrections (RAE rules)**:
  - Add missing `¡` before exclamations (e.g., `¡Hola!`, not `¡Hola`)
  - Fix accent marks on words (é, á, í, ó, ú, ná, más, pero, etc.)
  - Use proper diacritics on `ü` when needed (vergüenza, but pingüino)
  - Remove periods before closing parentheses (use `(texto).` not `(texto.)`)
  - Use comma before `etc.` when applicable
  - Correct verb conjugations and subject-verb agreement
  - Apply personal `a` before direct objects referring to people (ver a alguien)
  - Use consistent verb tense matching the original text
  - Avoid literal translations that sound unnatural in Spanish
  - Ensure coherent sentence structure and logical flow

### Naming Conventions

- **Files**: PascalCase (`LocalText.json`, `NpcNameFirst.json`)
- **Keys**: snake_case (`common_shi`, `role_character_name1`)
- **IDs**: Sequential numeric strings, starting from "1"

## File Organization

```
ModProject/
└── ModExcel/
    ├── LocalText.json              # General UI text
    ├── RoleLogLocal.json           # Character logs
    ├── Npcs/                       # Character names
    │   ├── NpcNameFirst.json
    │   ├── NpcNameLast.json
    │   └── HerdNPCNameFirst.json
    └── Prefixes/
        └── BattleSkillPrefixName.json
```

## Common Translation Patterns

- **UI**: Confirmar, Cancelar, Aceptar, Sí, No, Nombre, Género, Raza
- **Attributes**: Vitalidad, Energía, Suerte, Enfoque, Perspicacia, Reputación, Carisma, Longevidad, Humor, Salud, Resistencia, ATQ, DEF, Movimiento, Res marcial, Res espiritual, CRIT, RES CRIT, Agilidad, CRIT ATQ, CRIT RD, Hoja, Lanza, Espada, Puño, Palma, Dedo, Fuego, Agua, Rayo, Viento, Tierra, Madera, Alquimia, Forja, Feng Shui, Talismanes, Herbología, Minería
- **Elements**: Fuego, Agua, Rayo, Viento, Tierra, Madera
- **Cultivation**: Refinación de Qi, Fundación de Qi, Condensación de Qi, Núcleo Dorado, Origen de Espíritu, Infante Primordial, Recreación de Alma, Iluminación, Reconstitución, Ascensión
- **Relations**: Maestro, Aprendiz, Pareja, Casado

## Validation Checklist

Before committing:
- [ ] JSON syntax valid
- [ ] All entries have id, key, en
- [ ] IDs unique per file
- [ ] Spanish characters correct
- [ ] No trailing whitespace

## Adding New Entries

When adding translations, follow these steps:
1. Use the next sequential ID as a string.
2. Use a descriptive snake_case key.
3. Keep Spanish translations natural and concise.
4. Place entries in the correct ID order.

## Common Errors to Avoid

- Missing quotes around id field
- Duplicate IDs within the same file
- Trailing commas in JSON objects
- Incorrect character encoding (use UTF-8 without BOM)
- Literal translations that sound unnatural in Spanish
- Paths with spaces not properly quoted in commands
- Modifying files without first checking if paths contain spaces
