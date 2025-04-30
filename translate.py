from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, src_lang="en", tgt_lang="hi"):
    model_name_map = {
        "hi": "Helsinki-NLP/opus-mt-en-hi",
        "fr": "Helsinki-NLP/opus-mt-en-fr",
        "es": "Helsinki-NLP/opus-mt-en-es"
    }

    if tgt_lang not in model_name_map:
        return text  # fallback to original

    model_name = model_name_map[tgt_lang]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)
