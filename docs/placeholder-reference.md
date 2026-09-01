# Placeholder and markup reference

This reference describes the formats found in `Scripts/Output/Processed/`. Treat the processed Chinese files as the semantic source of truth and preserve the syntax when editing the Spanish resources.

The inventory below is a static scan of one repository snapshot. Each `total / distinct` value means total matches / distinct matched lexemes; it does not mean entries containing the format. The relevant snapshot hashes are:

| File | SHA-256 |
| --- | --- |
| `LocalText.json` | `0b4219221b1a78799e2ae59cc71de96c37f1c242454c1e759d5d90b71b361c1c` |
| `RoleLogLocal.json` | `3273f070c869a431454d9b6160961189e30f60055dfe5ad64e0ff9e83e082543` |

## Inventory

| Format | `LocalText.json` | `RoleLogLocal.json` | Purpose |
| --- | ---: | ---: | --- |
| `{...}` | 6,461 | 26,839 | Numeric, named, keyed, or argument placeholders |
| `&...&` | 6,841 | 0 | Dynamic values and expressions |
| `$...$` | 1,723 | 0 | Terms with an `s_` dictionary key |
| Rich-text tags | 14,415 | 1,308 | Color, size, alignment, links, and UI formatting |
| `[ ... ]` | 11 | 0 | Keyboard prompts and visible delimiters |
| `【 ... 】` | 566 | 1 | Visible Chinese brackets, sometimes around placeholders |
| `\\n` / `\\t` | 8,370 / 23 | 147 / 0 | Escape sequences processed by the game as newlines and tabs; counts are from the inspected mirror snapshot |
| `|` | 756 | 33,209 | Arguments, expressions, visible separators, and dialogue delimiters |
| `%` | 3,857 | 6 | Dynamic operators or visible percentage text |

The three NPC name files and `BattleSkillPrefixName.json` contain none of these dynamic formats in the inspected snapshot.

## Curly-brace placeholders

Preserve the complete expression, including its case, `#`, pipes, and argument order.

```text
{0}
{mapData125}
{#areaName8}
{name|A}
{relation|A|B}
{customParam|...}
```

`LocalText.json` contains numeric, named, `#`-prefixed, and argument forms. `RoleLogLocal.json` additionally uses families such as `relation`, `life`, `grade`, `name`, `gender`, `school`, `appellation`, `callIgnore`, and `yinyangEyeSoul`.

Known suspicious forms must not be normalized without runtime or source confirmation:

- `{fixValue点}`
- `{宗门职位}`
- `{garde|A}`
- An incomplete `callIgnore` expression in `RoleLogLocal.json` around line 106070

## Dynamic variables

`&...&` variables appear only in `LocalText.json`:

```text
&1001_gongji&
&700158_bjbl|/10000|+1|f2&
&103_killHp%88&
&81051_fwcs+1&
&s_1_0_1&
```

Preserve operators and suffixes such as `%88`, `+1`, `/10000`, `x...`, `f0`, and `f2`. Their meaning belongs to the game runtime, not the translation layer.

The pipe character is overloaded. Inside `{...}` and `&...&` it separates arguments or operations; elsewhere it can be a visible list separator, dialogue separator, or part of an emoticon. Do not change every `|` mechanically.

## Dictionary tokens

`$...$` tokens use the `s_` prefix:

```text
$s_dao$
$s_jian$
$s_huo$
$s_chixushifa$
```

Do not translate or remove the token. Translate only the surrounding text.

## Color and rich-text tags

The game uses internal color aliases as well as Unity-style tags:

```text
<r>...</r>    <g>...</g>    <b>...</b>    <o>...</o>
<y>...</y>    <p>...</p>    <w>...</w>
<color=#004FCA>...</color>
<#791515>...</color>
```

Other observed tags include `<size=...>`, `<align=...>`, `<indent=...>`, `<link=...>`, `<u>`, `<space=...>`, `<voffset=...>`, and `<sprite ...>`.

`<color={0}>` is also present. The placeholder inside the tag is part of the syntax and must remain unchanged.

Do not assume that `<r>`, `<g>`, or `<b>` are standard Unity rich text. The available evidence suggests that they may be aliases processed by the game's localization helpers, but the exact conversion still requires matching native binaries or a runtime test. A translated string that bypasses those helpers can display the tags literally or lose its colors. See [the Assembly-CSharp guide](assembly-csharp-localization.md).

Preserve nesting and closing order. The inspected source contains known malformed or ambiguous cases:

- `LocalText.json` around lines 151925, 259710, and 267920 has invalid nesting or mismatched color closures.
- Several `<size=130%>`/`<size=100%>` blocks around lines 207880, 266620, 266625, 269795, and 269800 have no explicit closing tag.
- `<root0>` through `<root4>` are game-specific tags, not colors.
- `<blod>` appears to be a possible typo, but must be confirmed before correction.
- The validator recognizes only known game markup names. Other angle-bracketed
  content is visible text and may be translated, such as
  `<秋枫夜话琉璃盏>` becoming `<Historia de la Lámpara del Alma>`.

## Brackets, delimiters, and escapes

Square brackets are usually visible keyboard prompts or UI delimiters:

```text
[F12]
[Alt]
[{0}]
```

Chinese brackets such as `【{0}】`, quotation marks such as `「...」`, and full-width parentheses `（...）` are normally visible text. Preserve them unless the surrounding sentence requires a grammatical correction.

The game processes the escape sequences `\n`, `\t`, and `\\` as a newline, a tab, and a literal backslash. Distinguish JSON source encoding from the value received by the game: a JSON source token such as `"\\n"` decodes to the two characters `\` and `n`, which the localization pipeline then processes as a newline. The processed mirror may contain duplicated or misplaced escape tokens because of a mirror-generation defect; its raw escape layout is not authoritative for runtime behavior. Preserve the logical position of every escape in the translated sentence and validate the resulting JSON and in-game rendering. The same rule applies to `\\t`, escaped backslashes, and `\\"`.

## Editing rules

1. Compare the Spanish value with the matching processed source entry.
2. Keep every placeholder, variable, tag, escape, and intentional separator; validate escape semantics against the game rather than copying a defective mirror representation.
3. Translate text outside syntax only.
4. Do not replace internal color aliases with arbitrary HTML colors.
5. Validate JSON, unique IDs, placeholder signatures, and tag nesting before committing.
