# language_translation.py

from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, target_language="fr"):
    model_name = f'Helsinki-NLP/opus-mt-en-{target_language}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
    translated_tokens = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(translated_tokens[0])

    return translated_text
