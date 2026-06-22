# RAG PDF Project - Usage Examples & Test Cases

## 🎯 Getting Started with Examples

### Setup Check

**Step 1: Verify Installation**
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip list | grep -E "gradio|faiss|transformers|sentence-transformers|pypdf"

# Expected output:
# faiss-cpu
# gradio
# sentence-transformers
# transformers
# pypdf
```

**Step 2: Verify Project Structure**
```
rag_pdf_project/
├── app.py ✅
├── main.py ✅
├── requirements.txt ✅
├── configs/settings.py ✅
├── data/documents/1.pdf ✅
├── ingestion/ ✅
├── retrieval/ ✅
├── generation/ ✅
└── pipeline/ ✅
```

**Step 3: Start the Application**
```bash
python app.py
# Output: * Running on local URL:  http://127.0.0.1:7860
```

---

## 📋 Test Cases & Examples

### Test Case 1: Load Default PDF

**Action**:
1. Open http://127.0.0.1:7860
2. Click "Use Default PDF" button
3. Wait for "Status" box to update

**Expected Result**:
```
Status: Ready. Loaded default document: 1.pdf
```

**What Happens Internally**:
```
1. PDF loaded: 1.pdf
2. Text extracted: ~5000 words
3. Split into chunks: ~17 chunks (300 words each)
4. Embedded: 17 × 384-dim vectors created
5. Indexed: FAISS index ready for search
6. UI State: index, chunks, document_name updated
```

---

### Test Case 2: Ask a Simple Question

**Scenario**: Analyze a document about "Machine Learning"

**Question**: "What is the main topic?"

**Expected Flow**:
```
INPUT: "What is the main topic?"
  │
  ├─ Embed: "What is the main topic?" → [0.23, -0.15, ..., 0.42]
  │
  ├─ Retrieve: Find 3 most similar chunks
  │  └─ Chunk 1: "This document covers machine learning..."
  │  └─ Chunk 2: "ML is a subset of artificial intelligence..."
  │  └─ Chunk 5: "Key topics include supervised learning..."
  │
  ├─ Build Context:
  │  "This document covers machine learning...
  │   ML is a subset of artificial intelligence...
  │   Key topics include supervised learning..."
  │
  ├─ Build Prompt:
  │  "Answer the question using only the context below...
  │   Context: [above text]...
  │   Question: What is the main topic?
  │   Answer:"
  │
  ├─ Generate Answer (T5):
  │  "The main topic is machine learning, 
  │   which is a subset of artificial intelligence..."
  │
OUTPUT: Display in "Answer" box
```

---

### Test Case 3: Upload Custom PDF

**Action**:
1. Click "Upload PDF"
2. Select a PDF file from your computer
3. Click "Load Uploaded PDF"
4. Wait for status update

**File Requirements**:
- Format: `.pdf` only
- Size: Any size (tested up to 100MB)
- Content: Text extractable (not scanned images)

**Expected Status**:
```
Ready. Loaded uploaded document: your_file.pdf
```

---

### Test Case 4: Multi-turn Conversation

**Scenario**: Ask follow-up questions

**Q1**: "What are the main concepts?"
```
Answer: "The main concepts include..."
```

**Q2**: "Explain concept A in detail"
```
Context: Retrieved chunks about concept A
Answer: "Concept A is..." (focused on specific concept)
```

**Q3**: "How does this relate to the introduction?"
```
Context: Retrieved chunks relevant to relationship
Answer: "This relates to the introduction by..."
```

**Key Point**: Each question is independent (new retrieval), but user context is maintained through conversation history in the UI.

---

## 🧪 Practical Examples

### Example 1: Analyzing a Research Paper

**Document**: `research_paper.pdf` (10 pages)

**Questions & Expected Answers**:

```
Q: "What problem does this paper solve?"
A: "This paper addresses the challenge of [problem] 
    by proposing a novel approach that..."

Q: "What is the methodology?"
A: "The methodology involves three main steps:
    1. Data preparation...
    2. Model training...
    3. Evaluation..."

Q: "What are the key results?"
A: "The key results show that the proposed method
    achieves [metric] improvements over baseline..."

Q: "What are future directions?"
A: "Future work could focus on [directions mentioned in paper]..."
```

### Example 2: Analyzing Product Documentation

**Document**: `product_manual.pdf` (50 pages)

**Questions & Expected Answers**:

```
Q: "How do I install this product?"
A: "Installation involves the following steps:
    1. Unpack the product...
    2. Connect to power...
    3. Configure settings..."

Q: "What should I do if I get error code X?"
A: "Error code X usually indicates... 
    Try the following solutions:
    1. Restart the device...
    2. Check connections..."

Q: "What are the specifications?"
A: "The product specifications are:
    - Power: 110V AC...
    - Operating temperature: 0-40°C...
    - Weight: 5kg..."
```

### Example 3: Analyzing Financial Reports

**Document**: `annual_report.pdf` (100 pages)

**Questions & Expected Answers**:

```
Q: "What is the company's revenue for Q3?"
A: "Q3 revenue was $[amount], representing
    a [percentage] increase/decrease from Q2..."

Q: "What are the main risks mentioned?"
A: "The company identifies the following key risks:
    1. Market volatility...
    2. Supply chain disruptions...
    3. Regulatory changes..."

Q: "What was discussed in the board letter?"
A: "The board letter highlighted...
    Our strategic priorities include..."
```

---

## 📊 Performance Monitoring

### Monitor Query Performance

**Timing Test**:
```
1. Note the time before asking question
2. Ask: "What is this document about?"
3. Note the time when answer appears
4. Calculate elapsed time

Expected: 0.5-2 seconds (depends on answer length)
```

**Performance Breakdown** (typical):
```
- Embedding query: 50-100ms
- FAISS retrieval: 1-5ms
- Prompt building: 1-2ms
- T5 generation: 500-1000ms
─────────────────────────────
- Total: 550-1100ms (~1 second average)
```

### Monitor Quality

**Quality Checklist**:
```
✓ Answer is grounded in document (not hallucinated)
✓ Answer is relevant to the question
✓ Answer is factually accurate
✓ Answer is concise but complete
✓ No duplicate or nonsensical text
```

**If answers are poor**:
1. Check the document has relevant content
2. Try a different question
3. Increase TOP_K to get more context
4. Check chunk quality (no corrupted text)

---

## 🔍 Debugging Examples

### Debug Case 1: Wrong Answer Format

**Symptom**: Answer contains control characters or formatting issues

**Debug Steps**:
```python
# In generation/llm.py, add debug logging:
def generate(prompt):
    # ... existing code ...
    output_ids = model.generate(**inputs, max_new_tokens=200)
    raw_output = tokenizer.decode(output_ids[0])  # Add this
    print(f"DEBUG: Raw output: {repr(raw_output)}")  # Add this
    
    clean_output = raw_output.strip()
    return clean_output
```

**Solution**: May need to adjust tokenizer decode parameters

### Debug Case 2: No Relevant Chunks Retrieved

**Symptom**: Answer says "I do not know" or is irrelevant

**Debug Steps**:
```python
# Add debug output in retrieval/retriever.py:
def retrieve(index, query_vector):
    distances, indices = index.search(query_vector, TOP_K)
    print(f"DEBUG: Retrieved indices: {indices[0]}")
    print(f"DEBUG: Distances: {distances[0]}")
    return indices[0]
```

**Solution**: 
- Increase TOP_K from 3 to 5
- Check document has relevant content
- Try different question phrasing

### Debug Case 3: Slow Generation

**Symptom**: Takes >3 seconds per query

**Debug Steps**:
```python
import time

def rag_answer(question, index, chunks):
    t0 = time.time()
    query_vector = embed([question])
    print(f"Embedding: {time.time()-t0:.3f}s")
    
    t1 = time.time()
    ids = retrieve(index, query_vector)
    print(f"Retrieval: {time.time()-t1:.3f}s")
    
    # ... build context ...
    
    t2 = time.time()
    answer = generate(prompt)
    print(f"Generation: {time.time()-t2:.3f}s")
    
    return answer
```

**Solution**:
- If generation is slow: Use CPU acceleration or reduce model size
- If retrieval is slow: Check FAISS index size

---

## ✅ Validation Checklist

### Pre-Launch Checklist

- [ ] All files in place (project structure intact)
- [ ] requirements.txt has all dependencies
- [ ] Python version is 3.10 or higher
- [ ] Sample PDF exists in data/documents/1.pdf
- [ ] All settings in configs/settings.py are valid
- [ ] No import errors when running `python app.py`

### Functionality Checklist

- [ ] Web UI loads at http://127.0.0.1:7860
- [ ] "Use Default PDF" button works
- [ ] PDF loading shows status message
- [ ] Can ask questions after loading PDF
- [ ] Answers appear in "Answer" box
- [ ] Questions can be cleared
- [ ] Can upload custom PDFs
- [ ] Answer quality is acceptable

### Performance Checklist

- [ ] First query takes <2 seconds
- [ ] Subsequent queries take <1 second
- [ ] No memory leaks (RAM stable after multiple queries)
- [ ] Models load on first use only
- [ ] UI remains responsive while generating

---

## 🎓 Learning Experiments

### Experiment 1: Chunk Size Impact

**Test**: How does chunk size affect answer quality?

```python
# Edit configs/settings.py and test:
CHUNK_SIZE = 100    # Smaller chunks
CHUNK_SIZE = 300    # Default
CHUNK_SIZE = 500    # Larger chunks

# Compare answers for same question
# Smaller = more focused, Larger = more context
```

### Experiment 2: TOP_K Impact

**Test**: How many retrieved chunks are optimal?

```python
# Edit configs/settings.py and test:
TOP_K = 1   # Minimal context
TOP_K = 3   # Default
TOP_K = 5   # Rich context
TOP_K = 10  # Very rich context

# Observe: Quality vs. inference time tradeoff
```

### Experiment 3: Different LLM Models

**Test**: Compare different generation models

```python
# Edit configs/settings.py and test:
GEN_MODEL = 'google/flan-t5-small'   # 250M, fast
GEN_MODEL = 'google/flan-t5-base'    # 580M, balanced
GEN_MODEL = 'google/flan-t5-large'   # 770M, quality

# Compare: answer quality vs. speed
# Note: Larger models need more memory
```

### Experiment 4: Different Embedding Models

**Test**: Compare embedding models

```python
# Edit configs/settings.py and test:
EMBED_MODEL = 'all-MiniLM-L6-v2'      # Fast, English only
EMBED_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'  # Default
EMBED_MODEL = 'all-mpnet-base-v2'     # High quality, slower

# Compare: retrieval relevance and speed
```

---

## 🚨 Troubleshooting Decision Tree

```
Application won't start?
├─ YES → Check Python version: python --version
│        └─ < 3.10? Install Python 3.10+
│        └─ >= 3.10? Install dependencies: pip install -r requirements.txt
│
├─ Web UI won't load?
│  ├─ Port 7860 already in use?
│  │  └─ Kill process or use different port
│  └─ Check terminal for error messages
│
├─ Can't load PDF?
│  ├─ Does 1.pdf exist? 
│  │  └─ NO? Place PDF in data/documents/
│  ├─ Is it a valid PDF?
│  │  └─ Try with different PDF
│  └─ Enough disk space?
│     └─ Check available storage
│
├─ No answer generated?
│  ├─ Did you load a PDF first?
│  │  └─ Click "Use Default PDF" or upload one
│  ├─ Is the question empty?
│  │  └─ Type a question
│  └─ Out of memory?
│     └─ Free up RAM or use smaller model
│
└─ Answer is irrelevant?
   ├─ Is it in the document?
   │  └─ PDF may not contain answer
   ├─ Try different question phrasing
   └─ Increase TOP_K in settings.py
```

---

## 📞 Getting Help

**For issues, check**:
1. QUICK_START.md - Basic usage guide
2. TECHNICAL_DOCS.md - Architecture details
3. Terminal output - Error messages
4. configs/settings.py - Configuration issues

**Common fixes**:
- Reload page: Ctrl+R or Cmd+R
- Restart app: Kill terminal and run app.py again
- Clear browser cache: Ctrl+Shift+Delete

---

**You're now ready to use the RAG PDF Assistant! 🚀**
