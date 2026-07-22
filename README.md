# DMFD Witch localization

Community-maintained localization files for the **DMFD Witch** mod for *Slay the Spire 2*.

魔女 Mod 的社区本地化仓库。欢迎修正翻译、润色文本，或贡献新的语言。

## Languages

| Directory | Language | Status |
| --- | --- | --- |
| `localization/zhs` | 简体中文 | Source language |
| `localization/eng` | English | Maintained |
| `localization/jpn` | 日本語 | Community translation |

## Contributing

1. Fork this repository and create a branch.
2. Edit an existing locale, or copy `localization/eng` to a new directory using the game's locale ID.
3. Follow the recurring gameplay terminology in [GLOSSARY.md](GLOSSARY.md).
4. Keep every JSON key and SmartFormat placeholder unchanged. Text inside formatter choices may be translated.
5. Run `python scripts/validate_localization.py`.
6. Open a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details. Accepted translations are pinned by the main mod repository and included in a later mod release; merging here does not silently alter an installed build.

## License

[MIT](LICENSE)
