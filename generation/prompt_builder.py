INSTRUCTION = (
    'Answer the question using only the context. '
    'If the answer is not in the context, say you do not know. '
    'Be concise and factual. Answer in the same language as the question.'
)


def build_prompt(question, context):
    return (
        f'{INSTRUCTION}\n\n'
        f'Context: {context}\n\n'
        f'Question: {question.strip()}\n'
        f'Answer:'
    )


def snippet(text, limit=280):
    compact = ' '.join(str(text).split())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + '...'
