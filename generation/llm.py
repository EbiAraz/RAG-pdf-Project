from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from configs.settings import GEN_MODEL

MAX_NEW_TOKENS = 200

_tokenizer = None
_model = None

def _get_model_and_tokenizer():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        print(f'Loading generation model: {GEN_MODEL}...')
        _tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
        _model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)
    return _model, _tokenizer

def _truncate_prompt(prompt):
    _, tokenizer = _get_model_and_tokenizer()
    max_context_tokens = getattr(tokenizer, 'model_max_length', 512)
    
    encoded = tokenizer(prompt, truncation=True, max_length=max_context_tokens)

    return tokenizer.decode(encoded['input_ids'], skip_special_tokens=True)


def generate(prompt):
    model, tokenizer = _get_model_and_tokenizer()
    max_context_tokens = getattr(tokenizer, 'model_max_length', 512)
    
    safe_prompt = _truncate_prompt(prompt)
    inputs = tokenizer(
        safe_prompt,
        return_tensors='pt',
        truncation=True,
        max_length=max_context_tokens,
    )
    output_ids = model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()