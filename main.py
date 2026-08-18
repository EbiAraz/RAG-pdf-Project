from pathlib import Path

from ingestion.build_index import build
from ingestion.sample_pdf import create_sample_pdf
from pipeline.rag_pipeline import rag_answer

PROJECT_ROOT = Path(__file__).resolve().parent
pdf_path = PROJECT_ROOT / 'data' / 'documents' / '1.pdf'

if not pdf_path.is_file():
    print(f'No PDF found at "{pdf_path}". Creating a sample document...')
    create_sample_pdf(pdf_path)

print('Preparing the system...')
index, chunks = build(str(pdf_path))
print('System is ready. Type "exit" when you are done.')

while True:
    question = input('\nQuestion: ').strip()
    if question.lower() in {'exit', 'quit'}:
        break
    if not question:
        print('Please enter a question.')
        continue

    answer, sources = rag_answer(question, index, chunks)
    print('\nAnswer:\n')
    print(answer)
    if sources:
        print('\nRetrieved context:\n')
        print(sources)
