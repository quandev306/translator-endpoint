# NLLB Translator

## Overview
- Multilingual machine translation powered by [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) covering 200+ language pairs.
- Built with FastAPI and returns Unicode-safe JSON responses.
- Replace the underlying model via the `MODEL_NAME` environment variable.

## Requirements
- Docker and Docker Compose (v3.9+).
- At least 4 GB RAM and 2 vCPUs for smooth inference inside the container.

## Run with Docker Compose
1. `docker compose up -d`
2. Service listens on `http://localhost:1111`

Stop the service with `docker compose down`.

## API
- `GET /translate`
- Query parameters:
  - `q` (required): text to translate. `text` is accepted as an alias.
  - `src`: source language code (default `eng_Latn`).
  - `tgt`: target language code (default `vie_Latn`).

Example:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

Sample response:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## Advanced Configuration
- Set `TRANSLATOR_MODEL` (or legacy `MODEL_NAME`) to switch models, e.g. `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`.
- Set `MAX_INPUT_LENGTH` to cap the tokenized input length (default 512).
- Store these variables in a `.env` file; the app loads it automatically via python-dotenv.
- The container discovers supported language codes from the tokenizer; unsupported `src`/`tgt` values trigger HTTP 400.

## Notes
- Endpoint currently handles one sentence/paragraph per request with an input cap of 512 tokens.
- When swapping models, make sure the tokenizer exposes `lang_code_to_id` or provides a compatible language list for `src`/`tgt`.

## Usage Guide
1. Start the service: `docker compose up -d`.
2. Send translation requests via `curl`, Postman, or any HTTP client.
3. (Optional) Tail logs: `docker compose logs -f translator`.
4. Stop the service when done: `docker compose down`.

## Author
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)
