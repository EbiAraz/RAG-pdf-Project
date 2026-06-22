def build_prompt(question, context):
    prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt