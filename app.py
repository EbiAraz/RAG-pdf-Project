import os
from pathlib import Path

import gradio as gr

from ingestion.build_index import build
from ingestion.sample_pdf import create_sample_pdf
from pipeline.rag_pipeline import rag_answer

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_PDF_PATH = PROJECT_ROOT / 'data' / 'documents' / '1.pdf'


def _file_path(file_obj):
    if not file_obj:
        return None
    if isinstance(file_obj, str):
        return file_obj
    return getattr(file_obj, 'name', None)


def _ensure_default_pdf():
    if DEFAULT_PDF_PATH.is_file():
        return str(DEFAULT_PDF_PATH)
    return create_sample_pdf(DEFAULT_PDF_PATH)


def load_knowledge_base(pdf_path):
    if not pdf_path or not os.path.isfile(pdf_path):
        raise FileNotFoundError(f'PDF not found at "{pdf_path}".')

    index, chunks = build(pdf_path)
    document_name = Path(pdf_path).name
    return index, chunks, document_name


def load_default_pdf():
    try:
        pdf_path = _ensure_default_pdf()
        index, chunks, document_name = load_knowledge_base(pdf_path)
        status = (
            f'Ready. Loaded default document: {document_name} '
            f'({len(chunks)} chunks indexed).'
        )
        return index, chunks, document_name, status
    except ValueError as e:
        return None, None, '', f'Error: {str(e)}'
    except Exception as e:
        return None, None, '', f'Error loading PDF: {str(e)}'


def load_uploaded_pdf(file_path):
    pdf_path = _file_path(file_path)
    if not pdf_path:
        return None, None, '', 'Upload a PDF first.'

    try:
        index, chunks, document_name = load_knowledge_base(pdf_path)
        status = (
            f'Ready. Loaded uploaded document: {document_name} '
            f'({len(chunks)} chunks indexed).'
        )
        return index, chunks, document_name, status
    except ValueError as e:
        return None, None, '', f'Error: {str(e)}'
    except Exception as e:
        return None, None, '', f'Error loading PDF: {str(e)}'


def ask(question, index, chunks, document_name):
    if not question or not str(question).strip():
        return 'Please enter a question.', ''

    if index is None or not chunks:
        return 'Load a PDF first, then ask a question.', ''

    answer, sources = rag_answer(question, index, chunks)
    if document_name:
        answer = f'Document: {document_name}\n\n{answer}'
    return answer, sources


def ask_and_clear(question, index, chunks, document_name):
    answer, sources = ask(question, index, chunks, document_name)
    return answer, sources, ''


with gr.Blocks(title='RAG PDF Assistant') as demo:  # type: ignore
    gr.Markdown('# RAG PDF Assistant')
    gr.Markdown(
        'Upload a PDF or use the bundled sample document, then ask questions '
        'against your RAG pipeline. Answers are generated only from retrieved PDF text.'
    )

    index_state = gr.State(value=None)
    chunks_state = gr.State(value=None)
    document_name_state = gr.State(value='')

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label='Upload PDF', file_types=['.pdf'], type='filepath')
            load_upload_btn = gr.Button('Load Uploaded PDF', variant='secondary')
            load_default_btn = gr.Button('Use Default PDF', variant='primary')
            status_box = gr.Textbox(
                label='Status',
                value="Click 'Use Default PDF' or upload a document to start.",
                interactive=False,
                lines=3,
            )

        with gr.Column(scale=2):
            question_box = gr.Textbox(
                label='Your Question',
                placeholder='Ask something about the loaded PDF...',
                lines=4,
            )
            ask_btn = gr.Button('Ask', variant='primary')
            answer_box = gr.Textbox(label='Answer', lines=10, interactive=False)
            sources_box = gr.Textbox(label='Retrieved context', lines=8, interactive=False)

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
        outputs=[answer_box, sources_box, question_box],
    )

    question_box.submit(
        fn=ask_and_clear,
        inputs=[question_box, index_state, chunks_state, document_name_state],
        outputs=[answer_box, sources_box, question_box],
    )


if __name__ == '__main__':
    # Keep Gradio's localhost health check off system/Windows proxies.
    os.environ.setdefault('NO_PROXY', '127.0.0.1,localhost,::1')
    os.environ.setdefault('no_proxy', '127.0.0.1,localhost,::1')

    is_space = bool(os.getenv('SPACE_ID'))
    server_name = '0.0.0.0' if is_space else '127.0.0.1'
    server_port = int(os.getenv('GRADIO_SERVER_PORT', '7860'))
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=False,
        debug=False,
        ssr_mode=False,
        inbrowser=False,
    )
