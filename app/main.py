from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch, os, re, json
from typing import Any


class UnicodeJSONResponse(JSONResponse):
    """Render JSON without escaping Vietnamese characters."""

    def render(self, content: Any) -> bytes:
        return json.dumps(content, ensure_ascii=False).encode("utf-8")


app = FastAPI(title="NLLB EN→VI (fixed lang ids)", default_response_class=UnicodeJSONResponse)

MODEL = os.getenv("MODEL_NAME", "facebook/nllb-200-distilled-600M")
SRC = "eng_Latn"
TGT = "vie_Latn"

# 👉 Dùng slow tokenizer để có lang_code_to_id
tokenizer = AutoTokenizer.from_pretrained(MODEL, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
model.eval()

def normalise_lang_code(token: str) -> str | None:
    trimmed = token.strip()
    if not trimmed:
        return None
    candidates = [
        trimmed,
        trimmed[1:-1] if trimmed.startswith("<") and trimmed.endswith(">") else "",
        trimmed[2:-2] if trimmed.startswith("__") and trimmed.endswith("__") else "",
    ]
    for candidate in candidates:
        candidate = candidate.strip()
        if candidate and "_" in candidate:
            return candidate
    return None

def build_lang_code_map():
    if hasattr(tokenizer, "lang_code_to_id") and tokenizer.lang_code_to_id:
        return dict(tokenizer.lang_code_to_id)
    if hasattr(model.config, "lang_code_to_id") and model.config.lang_code_to_id:
        return dict(model.config.lang_code_to_id)

    # Fallback: derive from special tokens such as "<eng_Latn>"
    fallback = {}

    extra_tokens = getattr(tokenizer, "additional_special_tokens", None) or []
    for tok in extra_tokens:
        code = normalise_lang_code(tok)
        if not code:
            continue
        token_id = tokenizer.convert_tokens_to_ids(tok)
        if token_id == tokenizer.unk_token_id:
            continue
        fallback[code] = token_id
    if fallback:
        return fallback

    special_map = getattr(tokenizer, "special_tokens_map_extended", None) or getattr(
        tokenizer, "special_tokens_map", {}
    )
    if isinstance(special_map, dict):
        for value in special_map.values():
            if isinstance(value, str):
                code = normalise_lang_code(value)
                if not code:
                    continue
                token_id = tokenizer.convert_tokens_to_ids(value)
                if token_id != tokenizer.unk_token_id:
                    fallback[code] = token_id
            elif isinstance(value, list):
                for item in value:
                    if not isinstance(item, str):
                        continue
                    code = normalise_lang_code(item)
                    if not code:
                        continue
                    token_id = tokenizer.convert_tokens_to_ids(item)
                    if token_id != tokenizer.unk_token_id:
                        fallback[code] = token_id
    return fallback

LANG_CODE_TO_ID = build_lang_code_map()
if not LANG_CODE_TO_ID:
    raise RuntimeError("Cannot discover supported languages from tokenizer or model config.")

SUPPORTED_LANGS = sorted(LANG_CODE_TO_ID.keys())
SUPPORTED_LANGS_SET = set(SUPPORTED_LANGS)
LANG_CODE_TO_NAME = getattr(tokenizer, "lang_code_to_name", {}) or {}

tokenizer.src_lang = SRC

def get_lang_id(lang_code: str) -> int:
    if LANG_CODE_TO_ID:
        try:
            return LANG_CODE_TO_ID[lang_code]
        except KeyError as exc:
            raise HTTPException(status_code=400, detail=f"Unsupported language code: {lang_code}") from exc
    token_id = tokenizer.convert_tokens_to_ids(lang_code)
    if token_id == tokenizer.unk_token_id:
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {lang_code}")
    return token_id

def postprocess(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r"\b(\w+)(\s+\1){2,}\b", r"\1 \1", text, flags=re.IGNORECASE)
    return text

def require_text_parameter(q: str | None, legacy_text: str | None) -> str:
    """Prefer `q`, but accept the legacy `text` query parameter."""
    for candidate in (q, legacy_text):
        if candidate is None:
            continue
        value = candidate.strip()
        if value:
            return value
    raise HTTPException(
        status_code=422,
        detail=[{"type": "missing", "loc": ["query", "q"], "msg": "Field required", "input": None}],
    )


@app.get("/translate")
def translate(
    q: str | None = Query(default=None, description="Nội dung cần dịch"),
    text: str | None = Query(
        default=None,
        description="Alias cũ cho nội dung cần dịch",
        include_in_schema=False,
    ),
    src: str = Query(SRC, description="Mã ngôn ngữ nguồn"),
    tgt: str = Query(TGT, description="Mã ngôn ngữ đích"),
):
    text_value = require_text_parameter(q, text)

    if SUPPORTED_LANGS_SET and (src not in SUPPORTED_LANGS_SET or tgt not in SUPPORTED_LANGS_SET):
        raise HTTPException(status_code=400, detail="Unsupported source or target language")

    with torch.no_grad():
        tokenizer.src_lang = src
        enc = tokenizer(
            text_value, return_tensors="pt", padding=True, truncation=True, max_length=512, src_lang=src
        )
        gen = model.generate(
            **enc,
            forced_bos_token_id=get_lang_id(tgt),
            do_sample=False,
            num_beams=4,
            no_repeat_ngram_size=5,
            encoder_no_repeat_ngram_size=5,
            repetition_penalty=1.8,
            length_penalty=1.0,
            max_new_tokens=128,
            early_stopping=True,
        )
        out = tokenizer.decode(gen[0], skip_special_tokens=True)
        return {"source": text_value, "translated": postprocess(out)}