# NLLB Translator

Centralized documentation with localized guides.

## Language Selector
- [🇻🇳 Tiếng Việt](README.vi.md)
- [🇬🇧 English](README.en.md)
- [🇯🇵 日本語](README.ja.md)
- [🇰🇷 한국어](README.ko.md)
- [🇨🇳 中文](README.zh.md)
- [🇩🇪 Deutsch](README.de.md)

## Quick Overview
- Multilingual translation service built with FastAPI and Hugging Face NLLB-200 models.
- Distributed as a Docker/Docker Compose setup listening on `http://localhost:1111`.
- API endpoint `GET /translate` accepts `q`, `src`, and `tgt` query parameters.
- Configure via environment variables such as `TRANSLATOR_MODEL`/`MODEL_NAME` and `MAX_INPUT_LENGTH`.
- Supports loading these variables from a `.env` file (python-dotenv).

## Contributing Translations
1. Copy an existing `README.<lang>.md` file as a template.
2. Update the content while keeping the section structure aligned.
3. Add your new file to the language selector list above.

## Author
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)
