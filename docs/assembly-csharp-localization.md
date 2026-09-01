# Assembly-CSharp localization guide

This guide records the localization pipeline observed in the current `Assembly-CSharp.dll` snapshot and provides a safe workflow for investigating rendering issues.

## Files and scope

The inspected managed assembly is:

```text
ModProject/ModCode/ModMain/dll/Assembly-CSharp.dll
```

The SHA-256 of that inspected copy is `05d30ab47001a88f658513c07f881a50b88696e12fdfca9a476ad39c6647cf57`. The project itself resolves its compile-time reference from `$(ManagedPath)/Assembly-CSharp.dll`, so the copied DLL and the one used for a build must be compared before drawing conclusions.

The game uses IL2CPP. `Assembly-CSharp.dll` exposes managed wrappers; the method bodies call `il2cpp_runtime_invoke`. The actual implementation is in the matching game `GameAssembly.dll`, so wrappers alone cannot prove how a tag is transformed.

For a matching game installation, collect these files without committing them:

```text
<game root>/GameAssembly.dll
<game root>/guigubahuang_Data/il2cpp_data/Metadata/global-metadata.dat
```

Do not use a `GameAssembly.dll` from another game or another game build.

## Relevant API

The generated wrapper exposes these methods on `GameTool`:

```csharp
public static string LS(string keys);
public static string LS(string keys, int bgType);
public static string SetTextReplaceColorKey(string text, string colorKey);
public static string SetTextReplaceColorKey(string text, string colorKey, int bgType);
public static string SetTextReplaceColorKeyUGUI(string text, string colorKey);
public static string TextToData(string text, int bgType);
public static string LSTextReplaceColor(string text, int bgType);
```

`StrPar` is also exposed through several overloads for string substitution; inspect their complete generated signatures before calling them.

`GameTool` also exposes color-related helpers such as `LevelToColor`, `LevelToColorKey`, `HrefColor`, and `textColors`.

The analyzed native mapping reported these RVAs for the matching native binary snapshot:

| Method | RVA |
| --- | ---: |
| `LSTextReplaceColor` | `0x2fd17d0` |
| `SetTextReplaceColorKey` | `0x2fd2f00` |
| `SetTextReplaceColorKeyUGUI` | `0x2fd2c50` |
| `TextToData` | `0x2fd4650` |

RVAs are build-specific and must be regenerated after a game update.

No matching `GameAssembly.dll` or `global-metadata.dat` is committed with this project, and the native binary identity was not recorded here. Therefore these RVAs are investigation notes, not portable patch offsets. A usable native result must record the architecture and hashes of all three matching files.

## Native resolution for the installed game build

The following resolution was made against the locally installed game build. It is useful for validation only; do not use these offsets for another build.

| File | SHA-256 |
| --- | --- |
| `GameAssembly.dll` | `affd4e9446b933678fe74fbe0a7732476ed638b9d2fd94cf5296fc4fe14fdde9` |
| `global-metadata.dat` | `d2351023ac89b11fa437c5a2c044216ae333c6eadecc2bd13d2bbaba9265ae3b` |
| `Assembly-CSharp.dll` | `05d30ab47001a88f658513c07f881a50b88696e12fdfca9a476ad39c6647cf57` |

`global-metadata.dat` is metadata version 27. `GameTool.LSTextReplaceColor(string, int)` has token `0x06007BF3`, method definition offset `0x01F78F3C`, and method-pointer index `31730` (zero-based). The matching `Assembly-CSharp.dll` code registration resolves that index to:

| Measure | Value |
| --- | --- |
| Native RVA | `0x02FD17D0` |
| Preferred-image VA | `0x182FD17D0` |
| File offset | `0x02FCFFD0` |
| Function range | `0x02FD17D0–0x02FD1BAC` |

The PE image base is `0x180000000` and `DYNAMIC_BASE` is enabled. At runtime, compute the target address from the loaded module base plus the RVA, not from the preferred-image VA. The method-pointer table entry is at file offset `0x069A4590` and stores `0x0000000182FD17D0`.

Reproduce the resolution with:

```bash
sha256sum GameAssembly.dll \
  guigubahuang_Data/il2cpp_data/Metadata/global-metadata.dat \
  MelonLoader/Managed/Assembly-CSharp.dll
hexdump -s 0x69a4590 -n 8 -e '1/8 "%016x\n"' GameAssembly.dll
objdump -d -Mintel --no-show-raw-insn \
  --start-address=0x182fd17d0 --stop-address=0x182fd1bac GameAssembly.dll
```

The native prologue preserves the Win64 `RCX` text argument and `EDX` background-type argument, then follows the game color tables and replacement logic. This corroborates the wrapper signature but does not replace an in-game rendering test.

The one-argument `GameTool.LS(string)` overload delegates to `GameTool.LS(string, 1)`. The Spanish formatter therefore uses background type `1` for hooks that do not receive an explicit context. Hooks for `GameTool.LS(string, int)` preserve the caller's actual `bgType`.

## Current mod behavior

`SpanishLocalePatches.cs` replaces `__result` in postfixes for `GameTool.LS`, `ConfLocalTextEx.text`, and the other localization properties. Spanish `LocalText` and `RoleLogLocal` values are passed through `GameTool.TextToData` before replacement. The native function runs its data-substitution passes and ends by calling `LSTextReplaceColor`; this is the game pipeline used to process dynamic text, the escape sequences `\n`, `\t`, and `\\`, and internal color aliases. The processed mirror may contain a defective duplicated or misplaced escape representation; runtime behavior, not that mirror artifact, is authoritative. Explicit TextMeshPro tags such as `<color=#004FCA>` are preserved. The final rendering behavior must still be verified in-game.

This color conversion addresses literal `<r>`, `<g>`, and `<b>` tags, which are internal game aliases rather than standard Unity rich text. The managed wrapper does not prove the native transformation; confirm the complete behavior with `GameAssembly.dll` analysis or a runtime test.

The `RoleLogLocal.json` schema must use `es` in the Spanish resource. The current loader reads `es`, and `update_project_files.py` converts the processed mirror's `en` field to `es` when merging new entries. Verify this invariant before using role logs as a color test.

The same direct replacement bypasses any other game-side processing for `{...}`, `&...&`, `$...$`, escape sequences, and game-specific tags. A color helper alone must not be assumed to solve those formats.

## Safe investigation workflow

1. Use the `Assembly-CSharp.dll`, `GameAssembly.dll`, and metadata from the same game build.
2. Inspect the managed signatures with an IL disassembler. Record wrappers separately from native implementations.
3. Use an IL2CPP metadata tool or native disassembler to resolve `GameTool` methods and string references.
4. Test the native helpers in the game runtime rather than assuming Unity's parser accepts the aliases.
5. Patch only one processing stage. Avoid applying the same transformation both in `LS` and at the final UI assignment.
6. Recheck `Text`, `TextMeshProUGUI`, dialogue, logs, and tooltips independently.

## Runtime test matrix

Use a controlled set of strings and record the returned value and screenshot:

```text
plain text
<r>red</r>
<g>green</g>
<b>blue</b>
<color=#004FCA>explicit color</color>
<b><u><size=30>nested</size></u></b>
{name|A} <r>$s_dao$</r>\n&1001_gongji&
```

Compare these paths where available:

```text
GameTool.LS(key)
GameTool.LS(key, bgType)
GameTool.TextToData(text, bgType)
GameTool.LSTextReplaceColor(text, bgType)
GameTool.SetTextReplaceColorKey(text, colorKey)
GameTool.SetTextReplaceColorKey(text, colorKey, bgType)
```

The expected result is not merely a changed string: verify that the final Unity UI component renders the intended color and that placeholders remain functional.

## Patch design notes

The likely first experiment is to process a translated value through the game's color helper before assigning `__result`, preserving the `bgType` available in the two-argument `LS` postfix. The property patch for `ConfLocalTextEx.text` has no `bgType`, so its correct helper or final UI hook must be determined by runtime testing.

Do not hardcode a color mapping or convert every alias to `<color=...>` until the native helper behavior is confirmed. Keep malformed source tags documented and fix them separately from the runtime pipeline.
