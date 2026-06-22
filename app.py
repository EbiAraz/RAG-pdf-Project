import os

import gradio as gr

from ingestion.build_index import build
from pipeline.rag_pipeline import rag_answer

DEFAULT_PDF_PATH = 'data/documents/1.pdf'


def load_knowledge_base(pdf_path):
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f'PDF not found at "{pdf_path}".')

    index, chunks = build(pdf_path)
    document_name = os.path.basename(pdf_path)

    return index, chunks, document_name


def load_default_pdf():
    try:
        index, chunks, document_name = load_knowledge_base(DEFAULT_PDF_PATH)
        status = f'Ready. Loaded default document: {document_name}'
        return index, chunks, document_name, status
    except ValueError as e:
        return None, None, '', f'Error: {str(e)}'
    except Exception as e:
        return None, None, '', f'Error loading PDF: {str(e)}'


def load_uploaded_pdf(file_path):
    if not file_path:
        return None, None, '', 'Upload a PDF first.'

    try:
        index, chunks, document_name = load_knowledge_base(file_path)
        status = f'Ready. Loaded uploaded document: {document_name}'
        return index, chunks, document_name, status
    except ValueError as e:
        return None, None, '', f'Error: {str(e)}'
    except Exception as e:
        return None, None, '', f'Error loading PDF: {str(e)}'


def ask(question, index, chunks, document_name):
    if not question or not question.strip():
        return 'Please enter a question.'

    if index is None or not chunks:
        return 'Load a PDF first, then ask a question.'

    answer = rag_answer(question, index, chunks)

    if document_name:
        return f'Document: {document_name}\n\n{answer}'

    return answer


def ask_and_clear(question, index, chunks, document_name):
    result = ask(question, index, chunks, document_name)
    return result, ''


with gr.Blocks(title='RAG PDF Assistant') as demo: # type: ignore
    gr.Markdown('# RAG PDF Assistant')
    gr.Markdown('Upload a PDF or use the bundled sample document, then ask questions against your RAG pipeline.')

    index_state = gr.State(value=None)
    chunks_state = gr.State(value=None)
    document_name_state = gr.State(value='')

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label='Upload PDF', file_types=['.pdf'], type='filepath')
            load_upload_btn = gr.Button('Load Uploaded PDF', variant='secondary')
            load_default_btn = gr.Button('Use Default PDF', variant='primary')
            status_box = gr.Textbox(label='Status', interactive=False, lines=3)

        with gr.Column(scale=2):
            question_box = gr.Textbox(
                label='Your Question',
                placeholder='Ask something about the loaded PDF...',
                lines=4,
            )
            ask_btn = gr.Button('Ask', variant='primary')
            answer_box = gr.Textbox(label='Answer', lines=14, interactive=False)

    load_default_btn.click(
        fn=load_default_pdf,
        inputs=None,
        outputs=[index_state, chunks_state, document_name_state, status_box],
    )

    load_upload_btn.click(
        fn=load_uploaded_pdf,
        inputs=file_input,
        outputs=[index_state, chunks_state, document_name_state, status_box],
    )

    ask_btn.click(
        fn=ask_and_clear,
        inputs=[question_box, index_state, chunks_state, document_name_state],
        outputs=[answer_box, question_box],
    )

    question_box.submit(
        fn=ask_and_clear,
        inputs=[question_box, index_state, chunks_state, document_name_state],
        outputs=[answer_box, question_box],
    )

    demo.load(
        fn=load_default_pdf,
        inputs=None,
        outputs=[index_state, chunks_state, document_name_state, status_box],
    )


if __name__ == '__main__':
    demo.launch(server_name='127.0.0.1', share=False, debug=False, theme=gr.themes.Soft())
