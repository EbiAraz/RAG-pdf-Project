# RAG PDF Assistant - Quick Start Guide

## 🚀 Running the Application

The application is already running! Access it here:
- **Web UI**: http://127.0.0.1:7860

## 📋 Features

✅ **PDF Upload** - Upload any PDF file to analyze
✅ **Default PDF** - Test with bundled sample document (1.pdf)
✅ **Ask Questions** - Natural language questions about PDF content
✅ **RAG Answers** - Context-aware responses using Retrieval Augmented Generation
✅ **Web Interface** - User-friendly Gradio UI

## 🎯 How to Use

### Step 1: Load a PDF
- **Option A**: Click "Use Default PDF" to use the sample document
- **Option B**: Click "Upload PDF" and select your PDF file, then click "Load Uploaded PDF"

### Step 2: Ask Questions
- Type your question in the "Your Question" field
- Press Enter or click the "Ask" button
- The system will:
  1. Convert your question to embeddings
  2. Search for relevant chunks in the PDF
  3. Build a context-aware prompt
  4. Generate an answer using AI

### Step 3: Get Answers
- Results appear in the "Answer" box
- Shows the document name and the generated answer
- Ask follow-up questions as needed

## 🔧 System Architecture

```
INPUT (PDF)
    ↓
[PDF Loader] → Extract text from PDF
    ↓
[Chunker] → Split into 300-word chunks
    ↓
[Embedder] → Convert chunks to vectors (multilingual-MiniLM)
    ↓
[FAISS Index] → Store vectors for fast search
    ↓
QUERY (User Question)
    ↓
[Embedder] → Convert question to vector
    ↓
[Retriever] → Find top-3 similar chunks (FAISS)
    ↓
[Prompt Builder] → Create context-aware prompt
    ↓
[LLM] → Generate answer (FLAN-T5-Small)
    ↓
OUTPUT (Answer)
```

## 📊 Configuration

All settings are in `configs/settings.py`:
- **EMBED_MODEL**: `paraphrase-multilingual-MiniLM-L12-v2` (Supports 100+ languages)
- **GEN_MODEL**: `google/flan-t5-small` (Lightweight, fast inference)
- **CHUNK_SIZE**: 300 words per chunk
- **TOP_K**: Retrieve top 3 chunks for context
- **MAX_NEW_TOKENS**: 200 token limit for answers

## 🗂️ Project Structure

```
├── app.py                      # Main Gradio web UI
├── main.py                     # CLI interface (alternative)
├── requirements.txt            # Python dependencies
│
├── configs/
│   └── settings.py            # Configuration settings
│
├── data/
│   └── documents/
│       └── 1.pdf              # Sample PDF
│
├── ingestion/                 # PDF processing
│   ├── build_index.py         # Main pipeline
│   ├── pdf_loader.py          # Extract text from PDFs
│   └── chunker.py             # Split text into chunks
│
├── retrieval/                 # Vector search
│   ├── embedder.py            # Create embeddings
│   ├── retriever.py           # Search FAISS index
│   └── vector_store.py        # FAISS initialization
│
├── generation/                # Answer generation
│   ├── llm.py                 # T5 model & tokenizer
│   └── prompt_builder.py      # Create prompts
│
└── pipeline/
    └── rag_pipeline.py        # Complete RAG pipeline
```

## 💾 Key Components

### 1. **PDF Loader** (`ingestion/pdf_loader.py`)
- Uses PyPDF to extract text from PDFs
- Handles multi-page documents
- Preserves document structure

### 2. **Chunker** (`ingestion/chunker.py`)
- Splits text into 300-word chunks
- Maintains context between chunks
- Optimized for semantic search

### 3. **Embedder** (`retrieval/embedder.py`)
- Uses SentenceTransformer (multilingual-MiniLM)
- Converts text to 384-dimensional vectors
- Cached model loading for efficiency

### 4. **Vector Store** (`retrieval/vector_store.py`)
- FAISS (Facebook AI Similarity Search)
- L2 distance metric for similarity
- O(1) query time for similarity search

### 5. **Retriever** (`retrieval/retriever.py`)
- Searches for top-3 most similar chunks
- Returns chunk indices for context building

### 6. **Prompt Builder** (`generation/prompt_builder.py`)
- Creates instruction-following prompts
- Includes context and question
- Prevents hallucination with grounding text

### 7. **LLM** (`generation/llm.py`)
- Google FLAN-T5-Small (250M parameters)
- Lightweight but capable
- Automatic prompt truncation to avoid overflow
- Max 200 new tokens per answer

## ⚙️ How RAG Works

**RAG = Retrieval Augmented Generation**

Instead of asking the LLM directly (which can hallucinate), RAG:
1. **Retrieves** relevant information from your PDF
2. **Augments** the question with this information
3. **Generates** an answer grounded in your document

Benefits:
- Factually accurate answers from your documents
- No hallucination because answers are grounded in text
- Efficient for large documents
- Supports any domain/topic

## 🆘 Troubleshooting

**Q: The page won't load**
- A: Make sure the terminal shows "Running on local URL: http://127.0.0.1:7860"
- Check if port 7860 is available

**Q: Getting error "PDF not found"**
- A: Upload a PDF first or ensure 1.pdf exists in data/documents/

**Q: Answers are too short/long**
- A: Modify `MAX_NEW_TOKENS` in `generation/llm.py`

**Q: Models taking time to load**
- A: First run downloads embedding and LLM models (~1GB total)
- Models are cached after first download

**Q: Out of memory**
- A: The T5-Small model requires ~2GB RAM
- For limited resources, use quantized models

## 🔄 Alternative: CLI Interface

Run `main.py` for command-line interface:
```bash
python main.py
```

Then enter questions at the prompt:
```
question: What is this document about?
answer: [RAG-generated answer]

question: exit
```

## 📝 Try These Questions

With the sample PDF, try:
- "What is the main topic?"
- "Summarize the key points"
- "What does [specific term] mean?"
- "How does [concept] work?"

## 🛠️ Customization

### Change the LLM Model
Edit `configs/settings.py`:
```python
GEN_MODEL = 'google/flan-t5-base'  # Larger, more capable
# or
GEN_MODEL = 'google/flan-t5-large'  # Even larger
```

### Change Embedding Model
```python
EMBED_MODEL = 'all-MiniLM-L6-v2'  # English-only, faster
```

### Adjust Chunk Size
```python
CHUNK_SIZE = 500  # Larger chunks = more context
```

### Change Number of Retrieved Chunks
```python
TOP_K = 5  # Retrieve 5 chunks instead of 3
```

## ✨ Features Overview

| Feature | Status | Details |
|---------|--------|---------|
| PDF Upload | ✅ | Upload any PDF, multiple formats supported |
| Default PDF | ✅ | Test with sample document |
| Multi-language | ✅ | Embedding model supports 100+ languages |
| Fast Search | ✅ | FAISS provides instant similarity search |
| Accurate Answers | ✅ | RAG prevents hallucination |
| Caching | ✅ | Models cached after first load |
| Web UI | ✅ | Gradio interface, no installation needed |

## 🎓 Learn More

- **RAG Papers**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- **FAISS**: https://github.com/facebookresearch/faiss
- **SentenceTransformers**: https://www.sbert.net/
- **FLAN-T5**: https://huggingface.co/google/flan-t5-small

---

**Enjoy using RAG PDF Assistant! 🚀**
