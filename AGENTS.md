# Guía de Agentes del Mod en Español de Tale of Immortal

Guía de localización para la traducción del juego Tale of Immortal (鬼谷八荒). Archivos JSON de localización que traducen textos del chino al español.

Índice
- Flujo de trabajo
- Validación
- Pruebas
- Git y commits
- PRs
- Guía de edición
- Estilo y convenciones
- Seguridad

## Flujo de trabajo
  - Define el objetivo de la tarea; identifica los archivos afectados.
- Trabaja en ramas temáticas y evita commits grandes en una sola rama.
- Prioriza cambios pequeños y reproducibles; evita cambios masivos sin verificación previa.
- Mantén la consistencia con el repositorio y el proyecto.

## Validación
- Validación JSON/UTF-8:
  ```bash
  # Validar sintaxis JSON en todos los archivos JSON
  for file in **/*.json; do jq empty "$file" && echo "\u2713 $file válido" || echo "\u2717 $file error"; done

  # Validar un archivo individual
  jq empty LocalText.json && echo "\u2713 LocalText.json válido"

  # Comprobar duplicados de IDs
  jq 'group_by(.id) | map(select(length > 1)) | length' LocalText.json
  ```
- Codificación UTF-8 sin BOM:
  ```bash
  iconv -f UTF-8 -t UTF-8 LocalText.json > /dev/null && echo "\u2713 Codificación OK"
  ```
- Revisión de nombres y claves: claves en snake_case; IDs como cadenas; estructuras JSON válidas.

## Pruebas
- Pruebas de traducción (Test) según la guía existente.
- Comprobación de que el archivo LocalText.json tenga estructura y campos obligatorios.

## Git y commits
- Evita realizar cambios destructivos sin confirmación explícita.
- Antes de un commit: revisar estado, diff y log reciente.
- Plantilla de mensaje de commit enfocada en el porqué; 1–2 oraciones.
- Reglas de seguridad: no modificar hooks, no reescribir historial a menos que se solicite expresamente.
- Si hay cambios no deseados, ignóralos; no revertir cambios que no hayas hecho.

## PRs
- Crear PRs con descripción clara de cambios y contexto.
- Verificar que la rama esté sincronizada con remotos y base antes de crear PR.
- Incluir resumen de cambios y impacto esperado.

## Guía de edición
- Formatos y convenciones de LocalText.json, RoleLogLocal.json, etc.
- Mantener caracteres UTF-8, uso correcto de tildes y signos de apertura de exclamación.
- Preservar etiquetas de juego (<r>, <g>, <b>, <color>, </color>, <size>, </size>, <align>, </align>, <indent>, </indent>, <y>, </y>) en las traducciones.
- Mantener consistencia con nombres de archivos y estructuras de directorios descritas.

## Estilo y convenciones
- IDs: cadenas numéricas secuenciales a partir de '1'.
- Claves: snake_case; entradas ordenadas alfabéticamente por clave en LocalText.json.
- Codificación: UTF-8 sin BOM, caracteres especiales en español.
- Evitar traducciones literales; mantener fluidez natural.

## Seguridad
- No revelar secretos; no incluir credenciales en textos traducidos.
- Verificar que no se introduzcan datos sensibles en archivos modificados.

### Estructura JSON

1. Formato de archivo: arreglos JSON válidos de objetos
2. Estructura de objeto:
   - id: Identificador único (cadena, entre comillas)
   - key: Clave de traducción (cadena, snake_case)
   - en: Traducción (UTF-8)

```json
[
  {
    "id": "1",
    "key": "common_shi",
    "en": "Sí"
  }
]
```

### Formato

- Indentación de 2 espacios, sin espacios en blanco al final, finales de línea LF
- IDs como cadenas (no enteros) según la convención existente
- Claves en snake_case, descriptivas y únicas
- Objetos ordenados alfabéticamente por `key` (LocalText.json) o `keyID` (RoleLogLocal.json)

### Directrices de traducción

- Codificación UTF-8 sin BOM
- Caracteres en español: á, é, í, ó, ú, ñ, Ñ, ¿, ¡
- Mantener las traducciones concisas para el espacio de la UI
- Usar terminología de juegos coherente
- Mantener las etiquetas del juego: siempre conservar <r>, <g>, <b>, <color>, </color>, <size>, </size>, <align>, </align>, <indent>, </indent>, <y>, </y> en las traducciones
- Reglas de gramática (RAE):
   - Añadir la apertura de la exclamación al inicio de las exclamaciones (p. ej., ¡Hola!; no ¡Hola, ni Hola!).
  - Corregir acentos en palabras (á, é, í, ó, ú, etc.).
  - Eliminar puntos al final de palabras antes del paréntesis de cierre (usar (texto).).
  - Usar coma antes de etc.
  - Corregir conjugaciones verbales y concordancia sujeto-verbo
  - Aplicar la preposición personal a antes de objetos directos que se refieren a personas (ver a alguien).
  - Usar tiempos verbales consistentes con el texto original.
  - Evitar traducciones literales que suenen poco naturales en español.
  - Asegurar una estructura de oración coherente y un flujo lógico.

### Convenciones de nombres

- Archivos: PascalCase (`LocalText.json`, `NpcNameFirst.json`)
- Claves: snake_case
- IDs: Cadenas numéricas secuenciales, que comienzan en "1"

## Organización de archivos

```
ModProject/
└── ModExcel/
    ├── LocalText.json              # General UI text
    ├── RoleLogLocal.json           # Registros de personajes
    ├── Npcs/                       # Nombres de personajes
    │   ├── NpcNameFirst.json
    │   ├── NpcNameLast.json
    │   └── HerdNPCNameFirst.json
    └── Prefixes/
        └── BattleSkillPrefixName.json
```

### Patrones comunes de traducción

- UI: Confirmar, Cancelar, Aceptar, Sí, No, Nombre, Género, Raza
- Atributos: Vida, Energía, Suerte, Enfoque, Perspicacia, Reputación, Carisma, Edad, Humor, Salud, Resistencia, ATQ, DEF, Movimiento, Res marcial, Res espiritual, CRIT, RES CRIT, Agilidad, CRIT ATQ, CRIT RD, Hoja, Lanza, Espada, Puño, Palma, Dedo, Fuego, Agua, Rayo, Viento, Tierra, Madera, Alquimia, Forja, Feng Shui, Talismanes, Herbología, Minería
- Elementos: Fuego, Agua, Rayo, Viento, Tierra, Madera
- Cultivo: Refinación de Qi, Fundación de Qi, Condensación de Qi, Núcleo Dorado, Origen de Espíritu, Infante Primordial, Recreación de Alma, Iluminación, Reconstitución, Ascensión
- Relaciones: Maestro, Aprendiz, Pareja, Casado

## Checklist de validación

Antes de confirmar:
- [ ] Sintaxis JSON válida
- [ ] Todas las entradas tienen id, key, en
- [ ] IDs únicos por archivo
- [ ] Caracteres en español correctos
- [ ] Sin espacios en blanco al final

## Añadir nuevas entradas

Al añadir traducciones, sigue estos pasos:
1. Usa la siguiente ID secuencial como cadena.
2. Usa una clave descriptiva en snake_case.
3. Mantén las traducciones al español naturales y concisas.
4. Coloca las entradas en el orden correcto de IDs.

## Errores comunes a evitar

- Falta de comillas alrededor del campo id
- IDs duplicados dentro del mismo archivo
- Comas finales en objetos JSON
- Codificación incorrecta (usar UTF-8 sin BOM)
- Traducciones literales que suenen poco naturales en español
- Rutas con espacios no entre comillas en comandos
- Modificar archivos sin comprobar previamente si las rutas contienen espacios
