# Self-Learning Knowledge Base - Design Document

## 1. Project Overview

**Project Name:** Self-Learning Knowledge Base  
**Type:** AI-Powered Knowledge Management System  
**Core Functionality:** Index, search, and query documents using semantic embeddings and RAG

## 2. Architecture

```
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  Ingestion   │ -> │  Processing   │ -> │  Storage     │
└──────────────┘    └───────────────┘    └──────────────┘
      │                    │                    │
      v                    v                    v
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ File Reader  │    │ Text Chunker  │    │ Vector Store │
│ URL Scraper  │    │ Embedding Gen │    │ (FAISS/     │
│ API Client   │    │ AI Processor  │    │  Chroma)    │
└──────────────┘    └───────────────┘    └──────────────┘
                                                │
                                                v
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│    Query     │ <- │    Search     │ <- │   Index      │
└──────────────┘    └───────────────┘    └──────────────┘
       │
       v
┌──────────────┐
│ AI Response  │
│  (RAG)       │
└──────────────┘
```

## 3. Components

### 3.1 DocumentIngestion
- **Purpose:** Load documents from various sources
- **Supported Sources:**
  - Local files (TXT, MD, PDF, DOCX)
  - Google Drive (via API)
  - Web URLs
  - Gmail emails

### 3.2 TextProcessor
- **Purpose:** Prepare text for embedding
- **Features:**
  - Text chunking (fixed size + sliding window)
  - Tokenization
  - Cleaning (remove noise, normalize)

### 3.3 EmbeddingGenerator
- **Purpose:** Convert text to vector embeddings
- **Options:**
  - OpenAI text-embedding-3-small
  - OpenRouter API
  - Local (sentence-transformers)

### 3.4 VectorStore
- **Purpose:** Store and search embeddings
- **Implementations:**
  - In-memory (simple)
  - FAISS (production)
  - Chroma (production)

### 3.5 QueryEngine (RAG)
- **Purpose:** Answer questions using retrieved context
- **Flow:**
  1. Convert query to embedding
  2. Search vector store
  3. Get top-k chunks
  4. Send to LLM with context
  5. Return answer

## 4. API Integration

### OpenRouter for LLM
```python
API_KEY = "API_KEY"  # Replace with actual key
MODEL = "openrouter/auto"
```

### Embedding API
```python
# Use OpenRouter or OpenAI for embeddings
EMBEDDING_MODEL = "text-embedding-3-small"
```

## 5. Data Flow

### Indexing Flow
```
Document -> Read -> Chunk -> Embed -> Store in Vector DB
```

### Query Flow
```
User Query -> Embed -> Search Vector DB -> Get Top-K Chunks 
-> Send to LLM with Context -> Return Answer
```

## 6. Storage

### Local Storage Structure
```
kb_data/
├── index.json          # Document metadata
├── embeddings/         # Vector embeddings
└── cache/             # Cached API responses
```

## 7. Testing Strategy

- Unit tests for each component
- Integration tests with sample documents
- Embedding quality tests
- RAG response validation

## 8. Security

- **API Keys:** Never commit to GitHub
- **Environment Variables:** Use .env files
- **Placeholders:** Use "API_KEY" in code

## 9. Future Enhancements

- Google Drive integration
- Gmail integration
- Web scraping
- Multi-modal embeddings
- Agentic search
