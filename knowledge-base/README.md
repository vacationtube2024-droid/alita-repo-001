# Self-Learning Knowledge Base

An AI-powered knowledge management system that learns from your documents.

## Features

- [ ] Document ingestion (PDF, TXT, MD, DOCX)
- [ ] Semantic search using embeddings
- [ ] RAG-based Q&A
- [ ] Learning from user feedback
- [ ] Multi-source indexing (Drive, local files, emails)

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Documents  │ -> │  Embeddings  │ -> │  Vector DB  │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              v
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   User     │ <- │    LLM       │ <- │   Search   │
│  Query     │    │   (RAG)      │    │   Results  │
└─────────────┘    └──────────────┘    └─────────────┘
```

## Usage

```bash
# Index documents
python knowledge_base.py index ./docs

# Query the knowledge base
python knowledge_base.py query "What is my project about?"
```

## Requirements

- Python 3.8+
- OpenAI API key (for embeddings + LLM)
- or local embeddings (sentence-transformers)

---

*Last updated: February 22, 2026*
