---
title: RAG PDF Assistant
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: true
---

# RAG PDF Assistant

A production-ready **Retrieval Augmented Generation (RAG)** system for interactive PDF analysis and question answering using semantic search and large language models.

**🌟 Hosted on HuggingFace Spaces** | **📦 Models from HuggingFace Hub** | **⚡ Production Ready**

---

## 🎯 Features

- **📤 PDF Upload** - Upload any PDF or use the bundled sample
- **🔍 Smart Retrieval** - FAISS-based vector similarity search over PDF content
- **🤖 AI-Powered Answers** - FLAN-T5 language model generation (HuggingFace)
- **🌍 Multilingual Support** - 100+ languages via multilingual embeddings
- **⚡ Fast Performance** - ~0.5-1 second per query after model load
- **🎨 User-Friendly UI** - Gradio web interface (no coding needed)
- **✅ Production Ready** - Full error handling, model caching, and validation

---

## 🚀 Quick Start

### Option 1: Local Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/rag_pdf_project.git
cd rag_pdf_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser to: **http://127.0.0.1:7860**

### Option 2: HuggingFace Spaces (Cloud)

1. Create a new Gradio Space on HuggingFace
2. Upload this repository
3. The app will deploy automatically!

---

## 📖 Usage

### Web UI (Recommended)

1. **Load PDF**: Click "Use Default PDF" or upload your own
2. **Ask Questions**: Type your question
3. **Get Answers**: RAG-powered answers appear instantly

### CLI Interface

```bash
python main.py
```

---

## 🏗️ Architecture

```
PDF Upload
    ↓
PDF Loader (PyPDF)
    ↓
Text Chunking (300-word chunks)
    ↓
Embedding (HuggingFace: Multilingual-MiniLM, 384-dim)
    ↓
FAISS Vector Index (L2 distance)
    ↓
User Question
    ↓
Query Embedding + Retrieval (Top-3 chunks)
    ↓
Prompt Building
    ↓
HuggingFace FLAN-T5 Generation (200 tokens max)
    ↓
Answer Display
```

---

## 📂 Project Structure

```
rag_pdf_project/
├── app.py                       # Gradio web UI
├── main.py                      # CLI interface
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── .gitignore                   # Git configuration
│
├── configs/
│   └── settings.py              # Model & parameter config
│
├── data/documents/
│   └── 1.pdf                    # Sample PDF
│
├── ingestion/                   # PDF processing
│   ├── build_index.py
│   ├── pdf_loader.py
│   └── chunker.py
│
├── retrieval/                   # Vector search
│   ├── embedder.py
│   ├── retriever.py
│   └── vector_store.py
│
├── generation/                  # Answer generation
│   ├── llm.py
│   └── prompt_builder.py
│
└── pipeline/
    └── rag_pipeline.py
```

---

## 🔧 Configuration

Edit `configs/settings.py`:

```python
# HuggingFace Embedding Model
EMBED_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'

# HuggingFace Generation Model
GEN_MODEL = 'google/flan-t5-small'

# Chunking
CHUNK_SIZE = 300  # words

# Retrieval
TOP_K = 3  # chunks

# Generation
MAX_NEW_TOKENS = 200  # tokens
```

---

## 🤖 HuggingFace Integration

### Models Used

| Component | Model | Source |
|-----------|-------|--------|
| Embedding | `paraphrase-multilingual-MiniLM-L12-v2` | SentenceTransformers |
| Generation | `google/flan-t5-small` | Google |
| Tokenizer | Auto | HuggingFace |

### Deploy to HuggingFace Spaces

```bash
# 1. Login to HuggingFace
huggingface-cli login

# 2. Create Space
huggingface-cli repo create rag-pdf-assistant --type space --space-sdk docker

# 3. Push code
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/rag-pdf-assistant
git push hf main
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| First Query | 1.5-2 seconds |
| Subsequent Queries | 0.5-1 second |
| Model Size | ~2GB |
| Memory Usage | 4-6GB |

---

## 🧪 Testing

```bash
python app.py
# Click "Use Default PDF"
# Ask: "What is this document about?"
```

---

## 📚 Documentation

- [QUICK_START.md](QUICK_START.md) - Basic usage
- [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md) - Deep architecture
- [EXAMPLES_AND_TESTS.md](EXAMPLES_AND_TESTS.md) - Examples & debugging

---

## 📦 Dependencies

- **transformers** - HuggingFace T5 models
- **sentence-transformers** - Multilingual embeddings
- **faiss-cpu** - Vector search
- **pypdf** - PDF extraction
- **gradio** - Web UI
- **numpy** - Numerical computing

---

## 🚀 Deployment

### Local
```bash
python app.py
```

### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### HuggingFace Spaces ⭐
Just push to HuggingFace!

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

- **HuggingFace** - Models and transformers
- **Facebook Research** - FAISS
- **Google** - FLAN-T5
- **SentenceTransformers** - Embeddings
- **Gradio** - Web interfaces

---

**Built with ❤️ using HuggingFace models**

Made with [Transformers](https://huggingface.co/transformers/) • [SentenceTransformers](https://www.sbert.net/) • [FAISS](https://github.com/facebookresearch/faiss) • [Gradio](https://gradio.app/)
