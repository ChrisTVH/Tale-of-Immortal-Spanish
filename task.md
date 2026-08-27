# Tareas de traducción — Localization/Spanish

> Fuente espejo original: `Scripts/Output/Processed/` (solo lectura). Las entradas nuevas se incorporan mediante `Scripts/update_project_files.py`.

## Tarea — [nombre o shard]

- Archivo: `[ruta del archivo]`
- Índices: `[inicio–fin]`
- Responsable: `[responsable]`
- Estado: `pendiente`
- Alcance: `[descripción de la tarea]`
- Notas o bloqueos: `[ninguno]`

### Checklist

- [ ] Traducción completada.
- [ ] Revisión ortográfica y gramatical completada.
- [ ] Placeholders y etiquetas verificadas.
- [ ] Espacios intencionales, sintaxis y abreviaturas preservados.
- [ ] Inglés residual traducido al español neutro.
- [ ] Sintaxis JSON y codificación UTF-8 verificadas.
- [ ] Validado.

## Validación

```bash
python3 Scripts/update_project_files.py --dry-run
jq empty [ruta-del-archivo].json
jq -e '[.[] | .id] | unique | length == length' [ruta-del-archivo].json > /dev/null
```
