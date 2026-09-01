# Glosario canónico de localización

## Alcance y prioridad

Aplicar este glosario al corregir `ModProject/ModCode/ModMain/Localization/Spanish/`. El campo chino de `Scripts/Output/Processed/` es la fuente autoritativa; el inglés de `Scripts/Default/` solo aporta contexto auxiliar. No modificar claves ni identificadores durante una corrección.

Cuando existan variantes, usar esta prioridad:

1. Reglas generales de `translation_guidelines.md`.
2. Equivalencia confirmada por el espejo chino mediante `id` y `key`.
3. Decisión más reciente revisada por `spell-checker-es`.
4. Forma canónica indicada aquí, con el contexto explícito cuando sea necesario.

No conservar como variantes activas las formas antiguas que contradigan una forma canónica. En particular, `Holy Spring` se traduce como **Fuente Sagrada**; `Manantial Sagrado` es una forma anterior descartada.

## Reglas de formato y estructura

- Traducir al español neutro, claro y conciso. Todo inglés descriptivo residual debe traducirse.
- Preservar literalmente placeholders, variables, escapes, saltos `\n`, pipes (`|`), porcentajes, delimitadores, espacios intencionales y el orden de los argumentos.
- Conservar el markup real del juego, incluidas `<r>`, `<g>`, `<b>`, `<color>`, `</color>`, `<size>`, `</size>`, `<align>`, `</align>`, `<indent>`, `</indent>`, `<y>`, `</y>` y las etiquetas con código de color como `<#e92828>`.
- En UI usar formas breves cuando el espacio sea limitado: `ATQ`, `DEF`, `PV`, `PV máx.`, `Pmáx` y `U. Dao` cuando correspondan.
- Mantener `Qi`, `Dao`, `EXP`, códigos y abreviaturas válidos; `EXP` se reserva para contextos de experiencia, no para cultivo.
- `Npcs/` se mantiene tal cual: conservar los nombres pinyin o transliterados y corregir únicamente errores evidentes de formato.
- `Prefixes/` se mantiene tal cual: no traducir ni normalizar nombres pinyin de prefijos.
- No trasladar esta terminología a los espejos chinos ni a los caches protegidos.

## Cultivo, cosmología y jerarquía

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| cultivation | cultivo | Incluye el cultivo de personajes y bestias. |
| cultivator | cultivador / cultivadora | Según el personaje. |
| 仙长 | Cultivador mayor | Tratamiento respetuoso para un cultivador de mayor rango o experiencia. |
| 仙侠 | héroe inmortal | Persona cultivadora de carácter heroico. |
| 前辈 / senior | superior / mayor | Tratamiento jerárquico; usar según el contexto de la frase. |
| 师姐 / senior sister | superiora | Tratamiento femenino para una discípula de mayor rango o antigüedad. |
| 小师妹 / junior sister | discípula menor | Tratamiento femenino para una discípula de menor rango o antigüedad. |
| 晚辈 / junior | discípulo menor | Autorreferencia respetuosa de una persona de menor rango o antigüedad. |
| 后生 / junior cultivator | cultivador menor | Tratamiento para un cultivador de menor rango o antigüedad; especialmente en RoleCall. |
| 灵素前辈 / Senior Lingsu | superior Lingsu | Tratamiento jerárquico; no forzar el género cuando el contexto no lo determina. |
| 亚神 / Senior Soul | conciencia superior | Una de las tres conciencias; corresponde a la conciencia de mayor antigüedad. |
| 上宗 / Secta Senior | Secta Mayor | Denominación jerárquica de una secta superior en RoleLogLocal. |
| 下宗 / Secta Junior | Secta Menor | Denominación jerárquica de una secta inferior en RoleLogLocal. |
| Qi | Qi | No traducir. |
| spirit | espíritu | — |
| soul | alma | — |
| sect | secta | No usar «sección». |
| artifact | artefacto | — |
| realm | reino | — |
| Dao | Dao | No traducir. |
| 地元仙根 / Earth Immortal Root | Raíz Inmortal Terrenal | — |
| True Blood Mysterious Body | Cuerpo misterioso de Sangre Verdadera | — |
| 道人 / Daoist | Daoísta | Título. |
| 真人 / True Person | Persona Verdadera | Título. |
| 真君 / True Lord | Señor Verdadero | Título. |
| 天尊 / Celestial Venerable | Venerable Celestial | Título. |
| Qi Refining | Refinación de Qi | — |
| Foundation Establishment | Fundación | Nombre general de la etapa. |
| Core Formation / Golden Core | Condensación / Núcleo Dorado | «Condensación» para la etapa; «Núcleo Dorado» para el núcleo o su contexto específico. |
| Spirit Origin | Origen de Espíritu | — |
| Nascent Soul | Infante Primordial | — |
| Soul Formation | Recreación de Alma | — |
| Enlightenment | Iluminación | — |
| Rebirth / Reconstitution | Reconstitución | — |
| Ascension | Ascensión | No cambiar el nombre válido del reino. |
| Body Reconstruction | Reconstitución corporal | — |
| Body Reconstruction Elixir | Elixir de Reconstitución Corporal | — |
| Tao Soul | Alma Tao | Conservar «Tao» en este nombre confirmado. |
| 道种 / Dao seed | semilla del Dao | — |
| 天骄 / chosen of heaven | Elegido del Cielo | — |
| 人道筑基 / Human Foundation | Fundación Humana | — |
| 地道筑基 / Earthly Foundation | Fundación Terrenal | — |
| 天道筑基 / Heavenly Foundation | Fundación Celestial | — |
| 天道庇佑 / Celestial Path Protection | Protección del Camino Celestial | — |
| 结晶境 / crystal realm | Cristalización | Etapa de cultivo. |
| 金丹良品心法 / Golden Core excellent mental skill | habilidad mental de grado excelente del Núcleo Dorado | — |
| 金丹极品心法 / Golden Core supreme mental skill | habilidad mental de grado supremo del Núcleo Dorado | — |
| cultivation partner / 道侣 | pareja de cultivo | — |
| 散修 / rogue cultivator | cultivador rebelde | — |
| 师兄 / senior brother | superior / hermano mayor | Tratamiento masculino para un discípulo de mayor rango o antigüedad; usar según el contexto. |
| 正道 / righteous path | camino recto | — |
| 魔道 / demonic path | camino demoníaco | — |
| 情花 / love flower | flor del amor | — |
| 正气 / righteous energy | energía recta | — |
| 灵气 / spiritual Qi | Qi espiritual | — |
| 冥气 / nether Qi | Aire Abisal | No confundir con Qi espiritual. |
| 冥妖 / Nether Demon(s) | Demonio Abisal / Demonios Abisales | Singular o plural según el contexto. |
| 灵冥二气 | Qi espiritual y Aire Abisal | — |
| 先天一气 / Primordial Qi | Aire Primordial | — |
| 浩然气 / Vast Qi | energía vasta | — |
| 木灵 / Wood Spirit | espíritu de Madera | — |
| 道根 / Dao Root | raíz del Dao | — |
| 道力 / Dao Power | poder del Dao | — |
| Ethereal Power / 飘渺之力 / ethereal power | poder etéreo | — |
| 神念 / divine sense | conciencia divina | — |
| 神识 (RoleLogLocal) | conciencia espiritual | En los diálogos asignados de RoleLogLocal. |
| 主神 / main spirit | conciencia principal | — |
| 次神 / secondary spirit | conciencia secundaria | — |
| 元灵 / primordial spirit | espíritu primordial | — |
| 识海 / Sea of Consciousness | Mar Mental | — |
| 识灵 / Consciousness Spirit | Espíritu Mental | — |
| 愿力 / Wish Power | Poder de los Deseos | — |
| 修为 / gained cultivation | cultivo obtenido | En texto general. |
| 修为 (bestia calabaza) | cultivo | No sustituir por `EXP`. |
| 增加修为 / increased cultivation | cultivo aumentado | No sustituir por `EXP`. |
| 减少修为 / reduced cultivation | cultivo reducido | No sustituir por `EXP`. |
| 道心坚定度 / Taoist Mind Dedication | firmeza del corazón taoísta | — |
| 筑基后期 / late Foundation stage | etapa tardía de la Fundación de Qi | — |
| 登仙之人 / person who ascends | persona ascendida / persona que asciende | Según la oración. |
| 血祭入门 / Blood Sacrifice Beginner | Sacrificio de Sangre básico | — |
| 血祭进阶 / Blood Sacrifice Advanced | Sacrificio de Sangre avanzado | — |
| Branch (school system) | división | Sistema de escuelas o ramas. |
| 宗门职位 / sect position | puesto en la secta | — |
| 宗门正式弟子 / formal sect disciple | discípulo formal de la secta | — |
| 外门弟子 / 内门弟子 | discípulo externo / discípulo interno | — |
| master / disciple | Maestro / Maestra; Aprendiz o Discípulo | Según género y contexto. |
| spirit root / 灵根 | raíz espiritual | — |
| 三阴绝脉体质 / 三阴绝脉体 | constitución de los Tres Meridianos Yin Extremos | Constitución cuyos meridianos están bloqueados por energía yin. |
| insight / 心得 | conocimiento o comprensión | Según el contexto. |
| progress / 进益 | progreso | — |
| 气运 / fortune | fortuna | — |
| 劲气 / forceful energy | ráfaga de energía | — |
| player / 玩家 | jugador | — |

## Interfaz, combate y atributos

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| attack | ATQ | UI breve. |
| defense | DEF | UI breve. |
| evasion / dodge (stat) | Evasión | — |
| health / hit points | PV / Vida | `PV` en UI; `Vida` en texto narrativo. |
| maximum health | PV máx. / Vida máxima | Según el espacio disponible. |
| stamina / 体力 | Resistencia | — |
| stamina recovery / 体力回复 | recuperación de resistencia | — |
| fire, water, lightning, wind, earth, wood | Fuego, Agua, Rayo, Viento, Tierra, Madera | Elementos. |
| cooldown | enfriamiento | — |
| attribute | atributo | — |
| skill | habilidad | — |
| technique | técnica | — |
| secret realm | reino secreto | — |
| critical multiplier / 暴击倍数 | multiplicador de golpe crítico | — |
| skill projectile range / 技能弹道射程 | alcance balístico de la habilidad | — |
| skill range / 技能范围 | rango de habilidad | — |
| 符谱 / talisman manual | manual de talismán | — |
| 刀法 / saber technique | técnica de sable | — |
| 刀法资质 / saber aptitude | aptitud con el sable | — |
| movement speed / 移动速度 | velocidad de movimiento | — |
| attack speed / 攻击速度 | velocidad de ataque | — |
| resistance / 抗性 | resistencia | — |
| Shield Vitality / 护盾值 | puntos de escudo | — |
| saber / 刀 | sable | Tipo de arma. |
| spear / 枪 | lanza | Tipo de arma. |
| sword / 剑 | espada | Tipo de arma. |
| fist / 拳 | puño | Tipo de ataque. |
| palm / 掌 | palma | Tipo de ataque. |
| finger / 指 | dedo | Tipo de ataque. |
| 血绽 / Bloodbath | Baño de sangre | Mantener separado de `Upgrade`. |
| 升级 / Upgrade | Actualizar | Verbo de UI. |
| 虚弱 / Weakened | Debilitado | — |
| combinable quantity / 可合成数量 | cantidad combinable | — |
| obtained items | objetos que obtuviste | Construcción confirmada en textos de robo. |
| EXP | EXP | Solo experiencia. |
| 割裂 / RIP | Desgarro | Efecto aplicado tras acumular Sangrado. |
| 归神 / Eternal Rest | Descanso eterno | Efecto de habilidad. |
| 归神掌 / Eternal Rest Palm | Palma del descanso eterno | Nombre de habilidad; conservar como referencia en sus descripciones. |
| 星耀 / Starshine | Brillo de estrellas | Efecto acumulable. |
| 星耀九霄 / Starlight II | Luz de las estrellas II | Nombre de habilidad; conservar la forma relacionada. |

## Habilidades, técnicas y efectos

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| Sharp Awl | Punzón Afilado | — |
| Sharp Strand | Punta Afilada | — |
| Aether Breath Manual | Manual de Respiración Etérea | — |
| Nether Flames | Llamas Abisales | — |
| Night Rain | Lluvia Nocturna | — |
| True Shield Stance | Postura de Escudo Verdadero | — |
| Spirit Fusion | Fusión Espiritual | — |
| Shield Spirit | Espíritu de Escudo | — |
| Spirit Blast | Explosión Espiritual | — |
| Spirit Seal | Sello Espiritual | — |
| Spirit Orbs | Orbes Espirituales | — |
| Shield Shadow | Sombra de Escudo | — |
| Thorny Spirit | Espíritu Espinoso | — |
| Battle Soul | Alma de Batalla | — |
| Soul Reaver / Soul Devour Sword | Espada Devoradora de Almas | — |
| Soul Lure | Señuelo del Alma | — |
| Sword Heart | Corazón de Espada | — |
| Puppet Soul Fusion | Fusión del Alma de Marioneta | — |
| Spirit Sight | Visión Espiritual | — |
| 真视灵烟 / True Sight Smoke | Humo de Visión Verdadera | Humo que bloquea ligeramente el Aire Abisal. |
| 天道之气 / Heaven Auras | Aura Celestial | Recurso obtenido en los registros mensuales. |
| 三清 / Three Pure Ones | Tres Purezas | — |
| 太荒蝡蛇劲 | Técnica de la Gran Serpiente Primordial | — |
| 蓄势 / Power Build | Preparación de Fuerza | — |
| 溃痕 / Scar | Cicatriz | — |
| 熔甲 / Melting Armor | Armadura fundida | — |
| 守护风暴 / Stormward | Tormenta Protectora | — |
| 震荡波 / Shockwave | Onda de choque | — |
| 无相爆 / Signless Explosion | Explosión Sin Forma | — |
| 崩山拳 / Hillbreaker Fist | Puño Rompemontañas | — |
| 排云掌 / Cloudshift Palm | Palma Despejanubes | — |
| 冰晶爆 / Ice Blast | Explosión de Hielo | — |
| 缠绕荆棘 / Entangling Thorn | Espina Enredadora | — |
| 菊花红、菊花烫、菊花残 / Burning Butt | Trasero Ardiente | — |
| 血煞大法 / Blood Power | Poder Sanguíneo | — |
| 血爪 / Blood Claw | Garra de Sangre | — |
| 斩龙剑气 / Dragonslayer Sword Aura | Aura de Espada Mata Dragones | — |
| Immortal Ladle | cucharón inmortal | — |
| 奔雷 / Rushing Thunder | Rayo Desatado | — |
| 雷云 / Lightning Cloud | Nube de Rayos | — |
| 暗雷球 / Dark Lightning Orb | Esfera de Rayo Oscuro | — |
| 雷球 / Lightning Ball | orbe de Rayo | — |
| Skycleaver / Skycleaver sword | Rompecielos como habilidad; espada Rompecielos como arma | Diferenciar el nombre de la habilidad del nombre del arma. |
| Deicide Cleave | Tajo Deicida | — |
| 一气化三清 / One Qi Transforms into Three Pure Ones | técnica de Un Qi se transforma en Tres Purezas | — |
| 断筋刺 / Piercing Sting | Picadura perforadora | — |
| 破体箭 / Sundering Arrow | Flecha desgarradora | No confundir con `Flecha que se divide`. |
| 分裂箭 / Split Arrow | Flecha que se divide | No confundir con `Flecha desgarradora`. |
| 飞芒 / Sharp Edge | Vanguardia | — |
| 啸斩 / Roaring Slash | Tajo rugiente | — |
| 断筋 / Hamstring | Bíceps femoral | — |
| 辰火硫骨 / Dawnfire Husk | Hueso de azufre del Fuego del Alba | — |
| 水意冰 / Flowing Ice | Hielo Fluyente | — |
| 魔印掌 / Demonic Mark Palm | Palma de marca demoníaca | — |
| 落石 / Falling Rock | Roca que cae | — |
| 灵流术 / Spiritual Torrent | Flujo Espiritual | — |
| 掌身法 / Palm Movement Technique | habilidad de movimiento de palma | — |
| 火意拳 / Fire-Intent Fist | Puño Ardiente | — |
| 冥意剑 / Nether-Intent Sword | Espada Abisal | — |
| 冰风之眼 / Ice Wind Eye | Ojo Helado Celestial | — |
| 冰霜风暴 / Frost Storm | Tormenta de Hielo | — |
| 轰天拳 / Skyblast Fist | Puño Explosivo del Cielo | — |
| 骤天剑 / Skyfall Sword | Espada de Caída del Cielo | — |
| 裂天风涌 / Skybreak Storm | Tormenta Rompecielos | — |
| 残天式 / Move of Broken Sky | Movimiento del Cielo Roto | — |
| 青空重瞳 / Sky Double Pupils | Pupilas dobles del cielo | — |
| 小小左 / Lil' Left | Pequeño Izquierdo | — |
| 天翎剑意 / Empyrean Edge | Filo empíreo | — |
| 蕴魂蒲阳 / Soul Basis Vine | vid de base del alma | — |
| 疾影 / Swift Shadow | Sombra veloz | — |
| 潮涌 / Tidal Surge | Marejada | — |
| 裂魂 / Soul Break | Alma rota | Efecto o estado; no confundir con un nombre de arma. |
| 狂暴 / Berserk | Frenesí | — |
| 草木皆兵 / Flora Minions | Plantas belicosas | — |
| 烈风喷涌 / Gust Gush | Oleada de vendaval | — |
| 草木牵引 / Flora Attraction | Atracción de plantas | — |
| 霸道斩 / Overbearing Cleave | Tajo Dominante | — |

## Objetos, materiales, plantas y alquimia

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| 灵丹 | elixir espiritual | — |
| 灵宝 | tesoro espiritual | — |
| 灵石 / spirit stone | Piedra Espiritual | — |
| Holy Spring | Fuente Sagrada | Forma canónica; no usar «Manantial Sagrado». |
| Spirit Fruits G4 | Frutas espirituales G4 | — |
| Bagua Jade Point | Puntos de Jade Bagua | — |
| Mysterious Shield | Escudo Misterioso | — |
| Forge Quartz | Cuarzo de Forja | — |
| Soul Jade | Jade de Alma | — |
| 心梦镜 / Heartdream Mirror | Espejo del Corazón Onírico | Artefacto de los diálogos de RoleLogLocal. |
| 玄珠 / Arcane Bead | Perla Misteriosa | — |
| 界元石 / Realm Origin Stone | Piedra del Origen | — |
| 冥屑 / Nether Shard | Fragmento Abisal | Nombre de material. |
| 冥气结晶 / Nether Qi Crystal | cristal de Aire Abisal | Material utilizado por el Espejo del Corazón Onírico. |
| 星砾 / Star Fragment | Fragmento Estelar | Nombre de material. |
| 羽圭 / Gentle Scintilla | Destello Suave | Nombre de material. |
| 仙琼 / Immortal Jade | Jade Inmortal | Nombre de material. |
| 上古遗迹传送符 / Ancient Ruins Teleportation Talisman | Talismán de teletransportación a ruinas antiguas | — |
| 太古残卷 / Aeon Remnant Scroll | Pergamino Antiguo | Tesoro que puede cambiar el destino de una secta. |
| 啸天元元鼎 / Sky Roarer Primordial Cauldron | Caldero Primordial de Aullido Celestial | — |
| 玄黄母气 / Primordial Xuanhuang Qi | Esencia Madre de Xuanhuang | — |
| 龙珠 / Dragon Orb | Orbe del Dragón | Una única equivalencia para todas sus apariciones. |
| 龙鳞 / Dragon Scale | Escama de Dragón | — |
| 龙威 / Dragon Majesty | Poder del Dragón | — |
| 苍鸣之磬 / Wailing Chime | Campana Resonante | — |
| 魂灯 / Soul Lamp | lámpara del alma | — |
| 琉璃宗 / Azurite Sect | Secta de Cristal | — |
| 月精 / Lunar Spirit | espíritu lunar | — |
| 驺吾 / Zouyu | Zouyu | Criatura nombrada. |
| 玲珑魂灯 / exquisite Soul Lamp | lámpara de alma exquisita | — |
| 玲珑石盘 / Exquisite Stone Plate | Placa de Piedra Exquisita | Objeto del minijuego de geomancia. |
| 玄灵液 / Arcane Dew | Rocío Arcano | — |
| Spirit Gathering Shell | Concha Reunidora de Espíritus | — |
| 炼妖壶 / Mythical Gourd | Calabaza Mítica | — |
| 六道灵珠 / Qi Orb | orbe de Qi | — |
| 六道灵斗气 / Condensed Qi | Qi condensado | — |
| 六道灵斗珠 / Condensed Qi Orb | orbe de Qi condensado | — |
| 坛子 / jar | vasija | — |
| 护盾值 / Shield Vitality | puntos de escudo | — |
| 骨盾 / Bone Shield | escudo de hueso | — |
| 摘星戒 / Star Catcher ring | anillo Atrapaestrellas | — |
| 残破锁灵阵 / Damaged Spirit-Locking Formation | formación de bloqueo espiritual dañada | — |
| 残破封魔阵 / Damaged Demon-Sealing Formation | formación de sellado demoníaco dañada | — |
| 藏宝图 / Treasure Map | mapa del tesoro | — |
| 堪舆 / geomancy | geomancia | — |
| 幻灵锅 / Mirage Pot | Caldero Ilusorio | — |
| 破格 / Rule Breaker | Rompe-Reglas | — |
| 缚命仙祠 / Destiny Catcher shrine | Santuario del Destino Atado | — |
| 双鱼佩 / Shuangyu Pei | Doble Pez (talismán) | Nombre de objeto; conservar la referencia pinyin. |
| 阳炎精金 / Sun Flame | Llama del Sol | — |
| 阳炎晶金 / Sunfire Crystal | Cristal de Fuego Solar | — |
| 镇川 / Zhenchuan | Zhenchuan | Nombre del colgante de jade de los diálogos de RoleLogLocal. |
| Osmanthus | osmanto | — |
| 紫元花 | flor Zi Yuan | Planta específica; no sustituir por «flor púrpura». |
| 妄象 | Espejismo | — |
| 玄召 | Invocación arcana | — |
| 魅壤 / Tempting Soil | Tierra Tentadora | — |
| 炼体丹 / Physique Elixir | Elixir físico | — |
| 玉冰烧 / Jade Ice | Hielo de Jade | Nombre de bebida en los diálogos de RoleLogLocal. |
| 竹叶青 | Bambú Verde | Nombre de bebida en los diálogos de RoleLogLocal. |
| 万年春 / Wannianchun | Primavera Milenaria | Nombre de bebida en los diálogos de RoleLogLocal. |
| 十八仙 | Dieciocho Inmortales | Nombre de bebida en los diálogos de RoleLogLocal. |
| 醉生梦死 | Sueño Ebrio | Nombre de bebida en los diálogos de RoleLogLocal. |
| 拘灵符 / Soul Cage Talisman | Talismán de la jaula del alma | — |
| 迅雷符 / Thunder Talisman | Talismán del Trueno | — |
| 灵盾符 / Spiritual Shield Talisman | Talismán del Escudo Espiritual | — |
| 凶卫符 / Necromancer's Talisman | Talismán del Guardián Feroz | — |
| 瞬移符 / Teleportation Talisman | Talismán de Teletransportación | — |
| 甘露符 / Manna Talisman | Talismán de maná | — |
| 诱兽符 / Monster Lure Talisman | Talismán de señuelo de monstruos | — |
| 浴火石 / Flameward Stone | Piedra bañada en fuego | — |
| 云中丹 / Cloud Elixir | Elixir de nube | — |
| 四品蜕骨丹 / G4 Golden Bone Elixir | Elixir de hueso dorado G4 | — |
| 三品复生丹 / G3 Revival Elixir | Elixir de avivamiento G3 | — |
| 四品子午丹 / G4 Meridian Elixir | Elixir del meridiano G4 | — |
| 赤阳丹 / Scarlet Sun Elixir | Elixir del sol escarlata | — |
| 壶妖修为丹 / Imp EXP Elixir / Imp Cultivation Elixir | Elixir de EXP de bestia en contexto de experiencia; Elixir de cultivo de bestia en contexto de cultivo | No sustituir el cultivo por `EXP`. |
| 壶妖境界丹 / Imp Realm Elixir | Elixir del reino de la bestia calabaza | — |
| 极意化瘀丹 | Elixir de Vida refinado | — |
| 极意培元丹 | Elixir de nutrición refinado | — |
| 三品玄元丹 / Unity Elixir G3 | Elixir de unidad G3 | — |
| 万年灵泉乳 | Leche de Manantial Espiritual Milenario | — |
| 真诰 | Canon Verdadero | — |
| 凤仙宝箓 / Phoenix Talisman | Talismán del Fénix | — |
| 道心果 / Dao Heart Fruit | Fruto del Corazón del Dao | — |
| 神魂 / Divine Souls | Almas Divinas | — |
| 真火 / True Flame / Samadhi Flame (forja) | Llama Verdadera; Llama Samadhi | Usar «Llama Samadhi» solo en contexto de forja. |
| 精魄 / Vitality Essence | Esencia Vital | — |
| 精魄丸 | Píldora de Esencia Vital | Objeto. |
| 精魄之息 | Aliento de Esencia Vital | Material de refinación. |
| 玉器 / Jadeware | objetos de jade | — |
| 龙璃灵金 / Dragonglass Gold | Oro de Vidriodragón | — |
| 星耀之光 / Starlight | Luz Estelar | — |
| 赤龙形态 / Crimson Dragon Form | Forma de Dragón Carmesí | — |
| 九幽无义草 / Red Spider Lily | Hierba Sin Lealtad de los Nueve Abismos | — |
| 乐仙 / Music Immortal | Inmortal de la Música | — |
| Aether Fern | Helecho Etéreo | — |
| 青须藤 / Emerald Vine | Enredadera Esmeralda | — |
| 大蓟根茎 / Thistle Stalk | Tallo de Cardo | — |
| 太玄松茸 / Taixuan Matsutake | Matsutake Taixuan | — |
| 太阴真火 / Taiyin True Flame | Llama Verdadera Taiyin | Llama verdadera; no traducir como agua. |
| 化晶丹 / Crystalization Elixir | Elixir de Cristalización | — |
| 土茯苓 / Filling the Earth | Poria Terrestre | — |
| 赤灵荆 / Crimson Thorn | Espina Carmesí | — |
| 深红矢车菊 / Crimson Cornflower | Centaurea Carmesí | — |
| 细叶雾水草 / Dew Grass | Hierba de Rocío | — |
| 赤魂玫瑰 / Crimson Rose | Rosa Carmesí | — |
| 向天草 / Sky Grass | Hierba Celeste | — |
| 蔽日仙菌 / Sun-Blocking Celestial Mushroom | Hongo Celestial Bloqueador del Sol | — |
| 谷箻桑 / Avian Berry | Baya Aviana | — |
| 万年白茯神 / Millennium Yam | Ñame del Milenio | — |
| 九曲灵参 / Melody Ginseng | Ginseng Melódico | — |
| 复盆麦门冬 / Dwarf Lilyturf | Lirio enano | Forma consolidada. |
| 泪玉之瞳 / Tear Jade Eye | Ojo de Jade Lagrimal | — |
| 固本肉苁蓉 / Desert Broomrape | jopo del desierto | — |
| 灵糠 / Spirit Bran | Salvado Espiritual | — |
| 霓裳草 / Silk Grass | Hierba de seda | — |
| 溟霖鼎 / Water Dragon Cauldron | Caldero del Dragón de Agua | — |
| 陶埙 / clay xun | ocarina de barro | — |
| 天光七叶莲 / Sky Ray Schefflera | Rayo Celeste de Esqueflera | — |
| 融血阳芝 / Blood Sun Lingzhi | Sol de sangre Lingzhi | — |
| 血魂麝香 / Blood Musk Mallow | Malva almizclera de sangre | — |
| 金阳火榴果 / Blazing Sun Berry | Baya del Sol Ardiente | — |
| 阳王丹炉 / Sun Crow Furnace | Horno del Rey Sol | — |
| 云锦素绢 / Brocade Silk | Seda Brocada | — |
| 编修 | editor / compilador | Cargo del Pabellón Langya; elegir según el contexto. |
| 结庐 | construir o establecer una cabaña o vivienda | Acción de establecer una residencia temporal. |
| 水工 | trabajador / ingeniero hidráulico | Oficio de los descendientes encargados del control de inundaciones. |
| 冰羽石像 | Estatua de Plumas de Hielo | — |
| 镇元锁灵阵 / Spiritlock Array | formación de bloqueo espiritual que suprime el Yuan | — |
| 念力 / Focus | Enfoque | — |
| 花妖后 / Flower Fairy Queen | Reina de las hadas de las flores | — |
| 驻颜果 / Beauty Fruit | Fruta de belleza | — |
| 天葵鸟尾草 / Begonia Grass | Hierba begonia | — |
| 破魂飞剑 / Soulbreak Flying Sword | Espada voladora Rompealmas | — |
| 霸王盾 / Overlord's Shield | Escudo del Señor Supremo | — |

## Criaturas, especies y clanes

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| 三足乌 / three-legged crow | Cuervo de tres patas | — |
| 何罗鱼 / Helo fish | Leviatán | — |
| 人参娃娃 / ginseng doll | muñeco de ginseng | — |
| 灵狐 / spirit fox | zorro espiritual | — |
| 竹木之精 | espíritu de bambú y madera | — |
| 竹妖 | demonio de bambú | — |
| 剧毒鬼蛛 | araña fantasma venenosa | — |
| 青狐剑士 | espadachín zorro verde | — |
| 青炎狐妖 | demonio zorro de llama azul | — |
| 草精 | espíritu de hierba | — |
| 木精 / Wood Sprite | espíritu de madera | — |
| 黄狐 | zorro amarillo | — |
| 大妖兽 / Greater demon beast / greater demon beast | bestia demoníaca mayor | — |
| 骷髅弓箭手 / Archer Skeletons | arqueros esqueleto | — |
| 巨灵神 / Spirit Giant | Gigante Espiritual | — |
| 魂婴树 / Soul Infant Tree | Árbol de la Iluminación | — |
| 魂婴果 / Soul Infant Fruit | Perla de la Iluminación | — |
| 妖兽之王——苍魂鸣蛇 / Beast King—Azure Soul Chiming Serpent | Rey de las Bestias: Serpiente Resonante del Alma Azul | — |
| 鸓 / Fly Mouse | Ratón volador | — |
| 两足犬 / Bipedal Hound | Sabueso bípedo | — |
| 牢笼僵尸 / Cage Zombie | Zombi de Jaula | — |
| 狐灵玉 / Vixen Jade | Zorra Jade | — |
| 大跟屁虫 / Large Follower Bug | Insecto Seguidor grande | — |
| 跟屁虫 / follower bug | insecto seguidor | — |
| 蚤妖 | demonio pulga | — |
| 壶妖 / Gourd Imp | bestia calabaza | No convertir en «duende»; nombre de criatura. |
| 小跟屁龙 / Small Follower Dragon | Pequeño Dragón Seguidor | — |
| 炼狱当康 / Hellish Dangkang | Dangkang Infernal | — |
| 鲮鱼 / Lingyu | Carpia | — |
| 朱雀 / Vermilion Bird | Pájaro Bermellón | — |
| 鲲鹏 / Roc | Roc | Conservar el nombre mitológico. |
| 凤凰 / Phoenix | Fénix | — |
| 玄鸟 / Arcane Bird | Pájaro Arcano | — |
| 青鸾 / Azure Luan | Pájaro Azul | — |
| 孔雀 / peacock | Pavo Real | — |
| 魔猿 / Dire Ape(s) | simio feroz / simios feroces | Singular o plural según la oración. |
| 小怪 / mobs | monstruos | En descripciones de enemigos genéricos. |
| 冥气仙卫 / Nether Air Guard | Guardia del Aire Abisal | — |
| 鸣蛇 / Chiming Serpent | Serpiente Resonante | — |
| 幽冥青蛇 / Netherworld Green Serpent | Serpiente Verde Abisal | — |
| 蛟龙 / Jiaolong | Dragón Jiao | Nombre de criatura. |
| 成蛟 / Jiao dragon | Dragón Jiao | Título o forma de la criatura según el contexto. |
| 兀蛇族 | Clan de la Serpiente Vudú | — |
| 蛮豚族 | Clan del Jabalí Salvaje | — |
| 灼龙族 / Flaming Dragon clan | Clan del Dragón Llameante | — |
| 戾斑族 / Brute Mark Clan | Clan de la Marca Fiera | — |
| 玉鸾族 / Jade Luan clan | Clan Pájaro de Jade | — |
| 岫兕族 / Jade Rhinoceros clan | Clan Rinoceronte de Jade | — |
| 神农族 | pueblo Shennong | Nombre de pueblo; conservar Shennong. |
| Guardian Beast | Bestia Guardiana | — |
| 保护对象 / protected person | protegido / protegida | Según el personaje. |
| 山猪 / mountain pig | jabalí | — |
| Divine Mulberry Guardian / 扶桑树守护者 | Guardiana de la Morera Divina | — |
| 龙鸾 / Dragon-Luan | clanes del Dragón y del Pájaro de Jade | — |

## Lugares, facciones y términos de mundo

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| Nether Air | Aire Abisal | Forma canónica para este término. |
| Nether Mountains | Montañas Abisales | — |
| Wave of Monsters / 兽潮 | Ola de Monstruos | — |
| Treasure Pavilion / 聚宝仙楼 | Pabellón del Tesoro | Una única forma canónica. |
| Battle Soul Shrine | Santuario del Alma de Batalla | — |
| Divine Eye | Ojo Divino | — |
| Celestial Eye | Ojo Celestial | — |
| Fairy Alliance | Alianza de las Hadas | — |
| Ghost Valley | Valle Fantasma | — |
| Fallen Valley | Valle Caído | — |
| Rocky Valley / 千岩谷 | Valle Rocoso | Una única forma canónica. |
| Spirit Vein Cavern | Caverna de la Vena Espiritual | — |
| Monster Lair | Guarida de Monstruos | — |
| Herb Garden | Jardín de Hierbas | — |
| 八荒 | Ocho Yermos | — |
| 八荒界 / Eight Wastelands Realm | Reino de los Ocho Yermos | — |
| 大冶台 | Dayetai | Lugar; conservar esta forma propia en RoleLogLocal. |
| 赤幽州 | prefectura de Chiyou | Topónimo de RoleLogLocal; conservar Chiyou como nombre propio. |
| 议事大厅 | Salón del Consejo | — |
| 招贤堂 | salón de reclutamiento | — |
| 龙门 / Dragon Gate | Puerta del Dragón | — |
| Point Race | Carrera de Puntos | — |
| Open Challenge Match | Partido de Desafío Abierto | — |
| Sect Tradition | Tradición de la Secta | — |
| Everfrost | Páramo Helado | Nombre de lugar. |
| 永恒冰原 / Everlasting Icefield | Páramo Helado | Misma forma canónica de lugar. |
| 迷途荒漠 / Wayward Desert | Desierto del Extravío | Lugar. |
| Dark Wind Grass | Hierba Viento Oscuro | — |
| Dragon Vein / 龙脉 | Vena de Dragón | — |
| 流沙之域 / Quicksand's Reach | Tierras de Arenas Movedizas | — |
| 炙炎之域 / Blazing Lands | Tierras Ardientes | — |
| 极寒之地 / Arctic Field | Campo Ártico | — |
| 雷罚之地 / Lightning Lands | Tierras del Rayo | — |
| 暴风山谷 / Stormvale | Valle de la Tormenta | — |
| 醉花林境 / Drunk Flower Forest | Bosque de Flores Borrachas | — |
| Mountain Hamlet / 山庄 | aldea montañosa | — |
| Cloud Cave / 碧云洞天 | Cueva de las Nubes Azules | — |
| Sandbank of Mist / 雾海烟渚 | Banco de Arena del Mar Brumoso | — |
| World Map Dungeon / 大地图副本 | mazmorra del mapa del mundo | — |
| Alliance Mission / 仙盟任务 | Misión de la Alianza | — |
| Hidden Caves Beyond the Wall / 墙外隐穴 | Cuevas Ocultas Más Allá del Muro | — |
| 十万大山 / Hundred Thousand Mountains | Cien Mil Montañas | — |
| 桃花幻境 / Peach Blossom Illusion Realm | Reino de la Flor de Melocotón | — |
| 树人之森 / Treefolk Forest | Bosque de los Hombres Árbol | — |
| 不归玄境 / No Return Xuan | Reino del Misterio del No Retorno | — |
| 御龙山庄 / Dragon-Taming Mountain Villa | Secta de la Montaña Domadora de Dragones | — |
| 御兽山庄 / Beast-Taming Mountain Villa | Secta de la Montaña Domadora de Bestias | — |
| 御龙仙师 / Dragon-Taming Immortal Master | Maestro Inmortal Domador de Dragones | Título. |
| 建木 / Jianmu | árbol Jianmu | Árbol mítico de los diálogos de RoleLogLocal. |
| 太古玄门 / Primordial Mysterious Sect | Puerta Misteriosa Primordial | Facción vinculada a Xingtian. |
| 玄天斩仙阵 | Formación Celestial de Ejecución Inmortal | — |
| 祈天台 / Prayer Heaven Platform | Terraza de Oración Celestial | Lugar. |
| 幽窟 | caverna abisal | — |
| 藏经阁 / Manual Library | Biblioteca de manuales | — |
| 灵阁 / Spirit Pavilion | Pabellón de los Espíritus | — |
| 东海 / East Sea | Mar del Este | — |
| 神水 / divine water | Agua Divina | — |
| 龙涎涧 / Dragon Saliva Ravine | Barranco de Saliva del Dragón | — |
| 落剑亭 | Pabellón de la Espada Caída | Lugar. |
| 山海界 / Mountains and Seas Realm | Reino de Montañas y Mares | — |
| 兄友弟恭 | respeto entre hermanos | — |
| 兄弟阋墙 | hermanos que se enfrentan | — |
| 逍遥 | libre / despreocupado | Según el título o la frase. |
| 最敬重的前辈 / most respected senior | mentor favorito / persona mayor más respetada | Según el contexto. |
| 心仪之人 / beloved person | persona amada | — |

## Terminología específica del Shard 3 y de RoleLogLocal

| Inglés o chino | Forma canónica en español | Contexto o nota |
| --- | --- | --- |
| 药灵 | espíritu medicinal | RoleLogLocal. |
| 散财天尊 | Venerable Celestial Dispensador de Riquezas | RoleLogLocal. |
| 霓裳仙君 / 霓裳仙子 | Señor Inmortal de las Vestiduras / Hada de las Vestiduras | Según el título y el género. |
| 斗魂-芦花王 / Battle Soul King Luhua | Rey de las Almas de Batalla Luhua | RoleLogLocal. |
| 灵宝道人 / Lingbao Daoist | Daoísta de los Tesoros Espirituales | Título. |
| 灵宝真人 / Lingbao True Person | Persona Verdadera de los Tesoros Espirituales | Título. |
| 灵宝真君 / Lingbao True Lord | Señor Verdadero de los Tesoros Espirituales | Título. |
| 灵宝天尊 / Lingbao Celestial Venerable | Venerable Celestial de los Tesoros Espirituales | Título. |
| 御鸡 | domador de pollos | — |
| 御鸡道人 / Chicken-Taming Daoist | Daoísta Domador de Pollos | Título. |
| 御鸡真人 / Chicken-Taming True Person | Persona Verdadera Domadora de Pollos | Título femenino en español si el personaje lo exige. |
| 御鸡真君 / Chicken-Taming True Lord | Señor Verdadero Domador de Pollos | — |
| 御鸡天尊 / Chicken-Taming Celestial Venerable | Venerable Celestial Domador de Pollos | — |
| 斩妖 | exterminación de demonios | — |
| 宗门大比 | gran competición de la secta | — |
| Starnight | Starnight | Nombre que se conserva. |
| 铁尺 / iron ruler | regla de hierro | — |
| Guigu Studio | Guigu Studio | Nombre de entidad; no traducir. |
| 历练日志 / Adventure Log | Registro de aventuras | En interfaz de aventura. |
| 历练编队 / Teaming | Formación de aventura | — |
| 技艺栏 / skills tab | pestaña de técnicas | — |

## Nombres propios, pinyin y transliteraciones

Conservar los siguientes nombres en su forma canónica. No convertirlos en traducciones genéricas ni alterar sus mayúsculas sin una razón gramatical clara.

| Fuente o alias | Forma canónica | Nota |
| --- | --- | --- |
| Yunmozou, Muxianzhou, Wuji, Bugui | Yunmozou, Muxianzhou, Wuji, Bugui | Pinyin ya establecido. |
| 扶桑 / Fusang | Morera Divina | Topónimo o entidad; conservar la referencia Fusang cuando aparezca como nombre. |
| 赤幽别志 | Anécdotas de Chi You | Título del libro de los diálogos de RoleLogLocal; no confundir con el topónimo `赤幽州`. |
| 扶桑树枝 / Mulberry Branch | rama de morera | Objeto; no traducir como «sucursal». |
| 昆仑仙池 / Kunlun Immortal Pond | Estanque Inmortal Kunlun | Lugar. |
| 息壤 / Xirang | Xirang / Piedra Divina Xirang | `Xirang` como nombre; «Piedra Divina Xirang» en contexto descriptivo. |
| 当康 / Dangkang | Dangkang | Criatura nombrada. |
| 双仪村 / Shuangyi Village | Aldea Dual | — |
| 剑红尘 / Jian Hongchen | Jian Hongchen | Personaje. |
| 青罗 / Qingluo | Qingluo | Personaje. |
| 武罗 / Wuluo | Wuluo | Personaje. |
| 雷神 | Dios del Trueno | Nombre o título. |
| 擎天寨 / Qingtian Stronghold | Fuerte Qingtian | Lugar. |
| 星耀宫 / Xingyao Palace | Palacio Celestial | Lugar. |
| 太行山 / Taihang Mountains | montañas Taihang | Topónimo. |
| 王屋山 / Wangwu Mountains | montañas Wangwu | Topónimo. |
| 愚村 / Fool Village | Aldea de los Tontos | Lugar. |
| 天元山 / Tian Yuan Mountain | Montaña Tian Yuan | Topónimo. |
| 胡雪儿 / Snow Hu | Snow Hu | Personaje femenino. |
| 玄龟 / Xuangui | Tortuga Negra | Criatura. |
| 夸父 / Kuafu | Kuafu | Personaje o criatura. |
| 阿夸 / A Kua | Agar | Nombre confirmado. |
| 勾陈 / Gouchen | Gouchen | Nombre propio. |
| 重明 / Chongming | Chongming | Nombre propio. |
| 陆吾 / Luwu | Luwu | Nombre propio. |
| 盘龙山 / Panlong Mountain | Montaña Panlong | Lugar. |
| 通幽谷 / Secluded Valley | Valle Recóndito | Lugar. |
| 镇邪峰 / Exorcism Peak | Pico del Exorcismo | Lugar. |
| 月落山 / Moonfall Mountain | Montaña Moonfall | Conservar `Moonfall` como parte del nombre. |
| 刑天 / Xingtian Slayer | Xingtian, el Asesino | Nombre o título. |
| 衡天 / Hengtian | Hengtian | Nombre propio. |
| 碎梦山挥 / Dreambreaker Mountain Spectre | Espectro Montañoso Rompesueños | Criatura o título. |
| 灵狐族 / Linghu clan | clan Linghu | Conservar el nombre del clan. |
| 斗魂王芦花 / Battle Soul King Luhua | Rey de las Almas de Batalla Luhua | Personaje o título. |
| Bi Fang / 毕方 | Bi Fang | Criatura. |
| Cangya / 苍牙 | Cangya | Nombre propio. |
| 长乘 / Changcheng | Changcheng | Nombre propio. |
| 孤云长乘 / Lonely Cloud Leonid | Changcheng de la Nube Solitaria | Nombre o título. |
| 血魅鲮鱼 / Bloodspell Carpia | Carpia Hechicera de Sangre | Nombre de criatura. |
| 天宝真人 / Tianbao True Person | Persona Verdadera Tianbao | Título y nombre. |
| 丑道人 / Ugly Daoist | Daoísta Feo | Personaje o título. |
| 沧崖 / Cangya | Cangya | Personaje masculino. |
| 沧泷 / Canglong | Canglong | Personaje femenino. |
| 璃星 / Lixing | Lixing | Personaje femenino. |
| 沐晴 / Muqing | Muqing | Personaje femenino. |
| 茗雪 / Mingxue | Mingxue | Personaje femenino. |
| 离朱 / Lizhu | Lizhu | Personaje femenino. |
| 智叟 / Zhisou | Zhisou | Personaje masculino. |
| Qingqiu | Qingqiu / Colina del Zorro | Usar la forma según el contexto; no reemplazar automáticamente el nombre. |
| 琅琊阁 / Langya Pavilion | Pabellón Langya | Lugar. |
| 八荒琅琊阁主 | Maestro del Pabellón Langya de los Ocho Yermos | Título. |
| Zheng / 正 | Zheng | Nombre de pueblo, no «justo» ni «recto». |
| 小小 / Lil' / little | Pequeño | En nombres de mazmorra. |
| 夕颜 / Xiyan | flor Xiyan | Nombre de planta. |
| 小姐 | señorita | Tratamiento para una mujer joven. |
| 九霄雷神 / Cloud Nine Hatuibwari | Dios del Trueno de los Nueve Cielos | Nombre o título. |
| 东方沐晴 / Dongfang Muqing | Dongfang Muqing | Personaje femenino. |
| 沁圭 / Qingui | Qingui | Guqin. |
| 李四 / Li Si | Li Si | Personaje masculino. |
| 风萍末 / Feng Pingmo | Feng Pingmo | Personaje femenino. |
| 龙女 / Dragon Girl | Chica Dragón | Personaje femenino. |
| 小芒 / Xiaomang | Xiaomang | Personaje masculino. |
| 枣枣 / Zaozao | Zaozao | Personaje femenino. |
| 韩枣枣 / Han Zaozao | Han Zaozao | Personaje femenino. |
| 阿毛 / A Mao | Amao | Criatura. |
| 阿聪 / A Cong | Acong | Criatura. |
| 大角 / Daijiao | Daijiao | Espíritu guardián. |
| 鬼谷小宝 / Guigu Xiaobao | Guigu Xiaobao | Nombre propio. |
| 于儿神 / Yu'er Shen | Yu'er Shen | Criatura. |
| 当扈 / Danghu | Danghu | Criatura. |
| 獙獙 / Bibi | Bibi | Criatura. |
| 开明兽 | Lidra | Criatura. |
| 人面鸮王 / human-faced owl king | Señor Arpía | Personaje masculino. |
| 大个子 / big guy | Grandote | Personaje masculino. |
| 相柳 / Xiangliu | Xiangliu | Serpiente. |
| 朱厌 / Zhu Yan | Zhu Yan | Criatura. |
| 钦原 / Qinyuan | Qinyuan | Criatura. |
| 灭蒙 / Miemeng | Miemeng | Criatura. |
| 烛照 / Zhuzhao | Luz de Vela | Nombre propio. |
| 幽荧 / Youying | Luciérnaga | Nombre propio; no tratarlo como una criatura genérica si funciona como nombre. |
| 吞天·饕餮 / Skydevourer Taotie | Taotie Devoracielos | Criatura o título; conservar Taotie. |
| 噬魂塔 / Soul Devour Tower | Torre Devoradora de Almas | Lugar u objeto nombrado. |
| 斗魂-芦花王 | Rey de las Almas de Batalla Luhua | Alias de RoleLogLocal. |
| 青鳞池 / Greenscale Pool | Estanque de Escama Verde | Lugar. |
| 蝡蛇大王 | Rey de la Gran Serpiente | Título de personaje. |
| 九凤族 / Nine Phoenix clan | Clan Nueve Fénix | Facción; conservar el nombre. |
| 乔 / Jo (cuando el espejo indica 李四) | Li Si | Alias residual en traducciones antiguas; usar solo cuando el chino confirme 李四. |
| 木正句芒 / Muzheng Goumang | Muzheng Goumang | Personaje; género no determinado. |
| Lydra / 开明兽 | Lidra | Nombre canónico de la criatura. |
| Coatl / Cóatl / 鸣蛇 | Serpiente Resonante | Alias antiguo; usar la forma canónica cuando el espejo confirme 鸣蛇. |
| Jiaolong / 蛟龙 | Dragón Jiao | Nombre canónico de la criatura. |
| 天玄真人 | Persona Verdadera Tianxuan | Título y nombre propios. |

## Criterios para verificar traducciones

- El inglés descriptivo siempre se traduce.
- Los nombres propios, el pinyin, los códigos y las abreviaturas válidos se conservan.
- Comparar cada traducción con el espejo chino por `id` y `key`.
- Preservar las firmas sintácticas: placeholders, variables, escapes, pipes, porcentajes, delimitadores y markup.
- Usar `jq --indent 2` al terminar cada despliegue, mediante un temporal seguro para cada JSON de localización modificado.
