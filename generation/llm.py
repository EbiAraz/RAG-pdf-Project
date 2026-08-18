import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from configs.settings import GEN_MODEL, MAX_INPUT_TOKENS, MAX_NEW_TOKENS, NUM_BEAMS
from generation.prompt_builder import INSTRUCTION

_tokenizer = None
_model = None


def _get_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    mps = getattr(torch.backends, 'mps', None)
    if mps is not None and mps.is_available():
        return torch.device('mps')
    return torch.device('cpu')


def _max_input_tokens(tokenizer):
    raw = getattr(tokenizer, 'model_max_length', MAX_INPUT_TOKENS)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return MAX_INPUT_TOKENS
    if value > 4096 or value < 32:
        return MAX_INPUT_TOKENS
    return min(value, MAX_INPUT_TOKENS)


def _from_pretrained(loader, name):
    try:
        return loader(name, local_files_only=True)
    except Exception:
        return loader(name)


def _get_model_and_tokenizer():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        print(f'Loading generation model: {GEN_MODEL}...')
        _tokenizer = _from_pretrained(AutoTokenizer.from_pretrained, GEN_MODEL)
        _model = _from_pretrained(AutoModelForSeq2SeqLM.from_pretrained, GEN_MODEL)
        _model.config.tie_word_embeddings = False
        _model.to(_get_device())
        _model.eval()
        if hasattr(_model, 'generation_config') and _model.generation_config is not None:
            _model.generation_config.do_sample = False
    return _model, _tokenizer


def _fit_context(question, context, tokenizer, max_tokens):
    """Keep the question intact and truncate only the retrieved context."""
    prefix = f'{INSTRUCTION}\n\nContext: '
    suffix = f'\n\nQuestion: {question.strip()}\nAnswer:'

    prefix_ids = tokenizer(prefix, add_special_tokens=False)['input_ids']
    suffix_ids = tokenizer(suffix, add_special_tokens=False)['input_ids']
    budget = max_tokens - len(prefix_ids) - len(suffix_ids) - 2
    budget = max(32, budget)

    context_ids = tokenizer(context, add_special_tokens=False)['input_ids']
    if len(context_ids) > budget:
        context_ids = context_ids[:budget]
        context = tokenizer.decode(context_ids, skip_special_tokens=True)

    return prefix + context + suffix


def generate(question, context):
    model, tokenizer = _get_model_and_tokenizer()
    max_tokens = _max_input_tokens(tokenizer)
    prompt = _fit_context(question, context, tokenizer, max_tokens)

    inputs = tokenizer(
        prompt,
        return_tensors='pt',
        truncation=True,
        max_length=max_tokens,
    )
    inputs = {key: value.to(model.device) for key, value in inputs.items()}

    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=NUM_BEAMS,
            early_stopping=True,
            no_repeat_ngram_size=3,
            length_penalty=1.0,
        )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
