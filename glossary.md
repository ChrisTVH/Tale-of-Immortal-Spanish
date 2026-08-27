# Glosario de localización

## Alcance

Aplicar este glosario al corregir `ModProject/ModCode/ModMain/Localization/Spanish/`. El texto chino de referencia está en `Scripts/Output/Processed/` y se consulta solo para resolver omisiones o confirmar el sentido. No modificar claves ni identificadores durante la corrección; las discrepancias estructurales existentes solo se reparan para hacer coincidir la clave original del espejo y se documentan.

## Terminología de cultivo

| Concepto | Traducción preferida |
| --- | --- |
| cultivation | cultivo |
| cultivator | cultivador / cultivadora según el personaje |
| Qi | Qi |
| spirit | espíritu |
| soul | alma |
| sect | secta |
| artifact | artefacto |
| realm | reino |
| Dao | Dao |
| Qi Refining | Refinación de Qi |
| Foundation Establishment | Fundación |
| Core Formation / Golden Core | Condensación / Núcleo Dorado según el contexto |
| Spirit Origin | Origen de Espíritu |
| Nascent Soul | Infante Primordial |
| Soul Formation | Recreación de Alma |
| Enlightenment | Iluminación |
| Rebirth / Reconstitution | Reconstitución |
| Ascension | Ascensión |

## Interfaz y combate

| Concepto | Traducción preferida |
| --- | --- |
| attack | ATQ |
| defense | DEF |
| health / hit points | PV cuando el espacio sea limitado; Vida en texto narrativo |
| maximum health | PV máx. o Vida máxima según el espacio disponible |
| fire, water, lightning, wind, earth, wood | Fuego, Agua, Rayo, Viento, Tierra, Madera |
| master / disciple | Maestro / Maestra; Aprendiz o Discípulo según género y contexto |
| cooldown | enfriamiento |
| attribute | atributo |
| skill | habilidad |
| technique | técnica |
| secret realm | reino secreto |

## Terminología específica del Shard 3

| Concepto | Traducción preferida |
| --- | --- |
| Nether Air | Aire Abisal |
| Nether Mountains | Montañas Abisales |
| Wave of Monsters | Ola de Monstruos |
| Sharp Awl | Punzón Afilado |
| Sharp Strand | Punta Afilada |
| Aether Breath Manual | Manual de Respiración Etérea |
| Nether Flames | Llamas Abisales |
| Night Rain | Lluvia Nocturna |
| Treasure Pavilion | Pabellón del Tesoro |
| Mysterious Shield | Escudo Misterioso |
| True Shield Stance | Postura de Escudo Verdadero |
| Spirit Fusion | Fusión Espiritual |
| Shield Spirit | Espíritu de Escudo |
| Spirit Blast | Explosión Espiritual |
| Spirit Seal | Sello Espiritual |
| Spirit Orbs | Orbes Espirituales |
| Shield Shadow | Sombra de Escudo |
| Thorny Spirit | Espíritu Espinoso |
| Battle Soul Shrine | Santuario del Alma de Batalla |
| Battle Soul | Alma de Batalla |
| Divine Eye | Ojo Divino |
| Fairy Alliance | Alianza de las Hadas |
| Ghost Valley | Valle Fantasma |
| Fallen Valley | Valle Caído |
| Rocky Valley | Valle Rocoso |
| Spirit Vein Cavern | Caverna de la Vena Espiritual |
| Monster Lair | Guarida de Monstruos |
| Soul Reaver / Soul Devour Sword | Espada Devoradora de Almas |
| Soul Lure | Señuelo del Alma |
| Sword Heart | Corazón de Espada |
| Body Reconstruction Elixir | Elixir de Reconstitución Corporal |
| Tao Soul | Alma Tao |
| Ethereal Power | poder etéreo |
| Forge Quartz | Cuarzo de Forja |
| Spirit Sight | Visión Espiritual |
| Puppet Soul Fusion | Fusión del Alma de Marioneta |
| Divine Mulberry Guardian | Guardiana de la Morera Divina |
| Herb Garden | Jardín de Hierbas |

## Convenciones de nombres

- Mantener nombres propios, topónimos y nombres de personajes en la transliteración pinyin existente: `Yunmozou`, `Muxianzhou`, `Wuji`, `Bugui`, etc.
- Mantener `Npcs/` y `Prefixes/` tal cual; no traducir ni normalizar sus nombres pinyin.
- No cambiar mayúsculas de nombres propios o nombres de técnicas salvo que la corrección gramatical lo exija claramente.

## Formato

- Preservar literalmente placeholders, variables, etiquetas, códigos de color/tamaño, saltos `\n`, espacios intencionales y abreviaturas.
- En textos de UI, preferir la forma breve del glosario cuando el campo tenga espacio limitado.
- Puede quedar texto inglés mezclado únicamente cuando sea un nombre propio, código o término que deba conservarse; cualquier inglés descriptivo residual debe traducirse al español.
