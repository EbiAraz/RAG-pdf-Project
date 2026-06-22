import os
from ingestion.build_index import build
from pipeline.rag_pipeline import rag_answer


pdf_path = 'data/documents/1.pdf'

if not os.path.exists(pdf_path):
    print(f'Error: PDF not found at "{pdf_path}". Please add the file and try again.')
    exit(1)

print('preparing for the system ...')

index, chunks = build(pdf_path)

print("system is ready .enter (exit) if you've done")

while True:
    q = input('\n question : ')

    if q == 'exit':
        break

    answer = rag_answer(q, index, chunks)

    print('\n answer : \n')

    print(answer)