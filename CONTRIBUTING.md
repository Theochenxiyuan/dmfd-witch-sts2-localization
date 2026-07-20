# Contributing translations

感谢你帮助改进魔女 Mod 的翻译。

## Editing rules

- Save JSON files as UTF-8.
- Do not rename or remove JSON keys.
- Every locale must contain the same `.json` files and keys as `localization/zhs`.
- Preserve SmartFormat variable and formatter names, for example `{Damage:diff:}`, `{Energy:energyIcons:}`, and `{IfUpgraded:show:...}`.
- You may translate literal text inside formatter choices. For example, the two displayed choices inside `{IfUpgraded:show:...|...}` may differ between languages.
- Preserve gameplay markup such as `[gold]...[/gold]` unless the target language needs a deliberate formatting change.
- Keep changes focused. A pull request for one language is easiest to review.

## Adding a language

Copy the entire `localization/eng` directory and rename it to the locale ID used by *Slay the Spire 2*. Translate all values; leave keys unchanged.

## Validation

Run:

```text
python scripts/validate_localization.py
```

The same validation runs automatically on pull requests. It checks JSON syntax, duplicate keys, file and key parity, string values, and SmartFormat placeholder signatures.
