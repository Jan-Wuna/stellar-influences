from __future__ import annotations

from pathlib import Path
import json
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ingest_udo_rudolph_abc import (  # noqa: E402
    SOURCE_FILE,
    TRANSLATION_CACHE_FILE,
    _clean_english_translation,
    _normalize_translation_source_text,
    _required_translation_texts,
)
from tools.udo_rudolph_abc_source import generate_models  # noqa: E402


MODEL_NAME = "Helsinki-NLP/opus-mt-de-en"
BATCH_SIZE = 16


def _load_existing(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _translate_missing(texts: list[str]) -> dict[str, str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    translations: dict[str, str] = {}
    with torch.no_grad():
        for start in range(0, len(texts), BATCH_SIZE):
            batch = texts[start : start + BATCH_SIZE]
            translation_inputs = [_normalize_translation_source_text(text) for text in batch]
            encoded = tokenizer(
                translation_inputs,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(device)
            generated = model.generate(**encoded, max_new_tokens=256)
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            for source, translation in zip(batch, decoded):
                translations[source] = _clean_english_translation(translation)
            print(f"translated {min(start + len(batch), len(texts))}/{len(texts)}", flush=True)
    return translations


def main() -> None:
    root = Path.cwd()
    refresh = "--refresh" in sys.argv[1:]
    cache_path = root / "tools" / TRANSLATION_CACHE_FILE
    factor_blocks, axis_blocks = generate_models(root / "Stellar Influences Vault" / SOURCE_FILE)
    required = _required_translation_texts(factor_blocks, axis_blocks)
    cache = _load_existing(cache_path)
    cache = {text: _clean_english_translation(translation) for text, translation in cache.items()}
    missing = required if refresh else [text for text in required if text not in cache or not cache[text].strip()]
    if missing:
        cache.update(_translate_missing(missing))
    ordered = {text: cache[text] for text in required}
    cache_path.write_text(
        json.dumps(ordered, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(ordered)} translations to {cache_path}")


if __name__ == "__main__":
    main()
