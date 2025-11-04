# NLLB Translator

## Überblick
- Mehrsprachige maschinelle Übersetzung mit [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M), unterstützt über 200 Sprachpaare.
- Implementiert mit FastAPI und liefert JSON-Antworten, die Unicode-Zeichen erhalten.
- Über die Umgebungsvariable `MODEL_NAME` lässt sich das zugrunde liegende Modell austauschen.

## Voraussetzungen
- Docker und Docker Compose (ab Version 3.9).
- Für stabile Inferenz im Container werden mindestens 4 GB RAM und 2 vCPUs empfohlen.

## Start mit Docker Compose
1. `docker compose up -d`
2. Der Dienst lauscht auf `http://localhost:1111`.

Anhalten mit `docker compose down`.

## API
- `GET /translate`
- Query-Parameter:
  - `q` (erforderlich): Zu übersetzender Text. Alias `text` wird akzeptiert.
  - `src`: Quellsprache (Standard `eng_Latn`).
  - `tgt`: Zielsprache (Standard `vie_Latn`).

Beispiel:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

Beispielantwort:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## Erweiterte Konfiguration
- Setzen Sie `TRANSLATOR_MODEL` (oder aus Kompatibilitätsgründen `MODEL_NAME`), um ein anderes Modell zu wählen, z. B. `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`.
- Setzen Sie `MAX_INPUT_LENGTH`, um die maximale Länge der Eingabetokens festzulegen (Standard 512).
- Dank python-dotenv können diese Variablen bequem in einer `.env`-Datei hinterlegt werden.
- Der Container ermittelt unterstützte Sprachcodes automatisch über den Tokenizer; ungültige `src`/`tgt` Werte führen zu HTTP 400.

## Hinweise
- Der Endpunkt verarbeitet pro Anfrage einen Satz oder Absatz; die Eingabe ist auf 512 Tokens begrenzt.
- Beim Modellwechsel sollte der Tokenizer `lang_code_to_id` bereitstellen oder eine kompatible Sprachenliste für `src`/`tgt` liefern.

## Anleitung
1. Dienst starten: `docker compose up -d`.
2. Übersetzungsanfragen per `curl`, Postman oder einem anderen HTTP-Client senden.
3. (Optional) Logs verfolgen: `docker compose logs -f translator`.
4. Dienst beenden: `docker compose down`.

## Autor
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)
