# Reglas de traducción

- Traducir al español neutro, con lenguaje natural, claro y conciso.
- Mantener el significado, el tono, el género, el tiempo verbal y la terminología del juego.
- Conservar todos los marcadores y etiquetas del juego: `<r>`, `<g>`, `<b>`, `<color>`, `</color>`, `<size>`, `</size>`, `<align>`, `</align>`, `<indent>`, `</indent>`, `<y>` y `</y>`.
- Preservar placeholders, variables y formatos especiales del texto original.
- Usar correctamente tildes, ñ, ¿ y ¡; evitar traducciones literales poco naturales.
- Aplicar la gramática española: concordancia, conjugaciones correctas, preposición personal «a» y coma antes de «etc.».
- Mantener los archivos en UTF-8 sin BOM, con finales de línea LF y sin espacios finales.
- Usar arreglos JSON de objetos con `id`, el campo estructural (`key` o `keyID`) y el campo de texto `es` tanto en los espejos procesados como en todos los recursos de localización del mod.
- Mantener los `id` como cadenas numéricas únicas y secuenciales; usar claves descriptivas en `snake_case`.
- Ordenar las entradas por `key` en `LocalText.json` y por `keyID` en `RoleLogLocal.json`.
- Preservar espacios intencionales, sintaxis y abreviaturas: la fuente en chino no usa espacios o dispone de espacio muy limitado en UI; no añadir ni eliminar espacios de forma innecesaria y conservar abreviaturas como `ATQ`, `DEF`, `PV`, `Pmáx`, `U. Dao` si aportan concisión.
- `Npcs/` y `Prefixes/` se mantienen tal cual (pinyin/transliteración); solo se corrigen errores evidentes de formato, sin retraducir nombres.
- El chino de `Scripts/Output/Processed/` es la fuente autoritativa para el significado. El campo `en` de `Scripts/Default/` tiene calidad variable y solo sirve como contexto auxiliar; que una traducción española coincida con él no valida su calidad ni impide mejorarla.
- Las diferencias de placeholders entre el chino y el inglés original no deben resolverse mediante sustitución automática: deben comprobarse según la sintaxis que acepte el juego y el contexto de cada entrada.

## Chequeo de sintaxis

```bash
shopt -s globstar nullglob
for file in Scripts/Output/Processed/*.json ModProject/ModCode/ModMain/Localization/Spanish/**/*.json; do
  jq empty "$file" || exit 1
  iconv -f UTF-8 -t UTF-8 "$file" > /dev/null || exit 1
  jq -e 'all(.[]; has("id") and (has("en") or has("es")))' "$file" || exit 1
  test "$(jq 'map(.id) | length == (unique | length)' "$file")" = true || exit 1
done
```
