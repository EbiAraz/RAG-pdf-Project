from retrieval.embedder import embed
from retrieval.retriever import retrieve
from generation.prompt_builder import build_prompt
from generation.llm import generate

def rag_answer(question,index,chunks):

    query_vector = embed([question])

    ids = retrieve(index,query_vector)
    
    context = ""

    for i in ids:
        if i == -1:
            continue
        context += chunks[i] + '\n'

    prompt = build_prompt(question,context)

    answer = generate(prompt)

    return answer