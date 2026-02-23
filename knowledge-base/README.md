# Self-Learning Knowledge Base

An AI-powered knowledge management system with semantic search.

## Versions

### v2.0 (Current)
- ✅ Vector embeddings for semantic search
- ✅ Text chunking for large documents
- ✅ Cosine similarity search
- ✅ In-memory vector store (upgradable to FAISS/Chroma)
- ✅ RAG-like query answering

### v1.0 (Legacy)
- Keyword-based indexing
- Simple search

## Usage

```bash
# Check stats
python knowledge_base_v2.py stats

# Index a file
python knowledge_base_v2.py index ./myfile.txt

# Query
python knowledge_base_v2.py query "What is this about?"
```

## Architecture

```
User Query → Embedding → Vector Store → Top Matches → Answer
```

## Upgrades Available

- Replace with OpenAI embeddings
- Add Chroma/FAISS for better vector search
- Connect to Google Drive
- Add web scraping

---

*🤖 Built by Alita - Feb 21, 2026*
