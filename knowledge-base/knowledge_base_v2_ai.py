#!/usr/bin/env python3
"""
Self-Learning Knowledge Base - AI-Powered RAG System
Version: 2.1 (AI-Enhanced)

This version uses OpenRouter API for intelligent Q&A using RAG.
"""

import os
import json
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict


# ============================================================================
# CONFIGURATION
# ============================================================================

# Replace with your OpenRouter API key, or set via environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openrouter/auto"

# Embedding configuration
EMBEDDING_DIM = 1536  # OpenAI default


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Document:
    """Represents a document in the knowledge base."""
    id: str
    content: str
    source: str
    metadata: Dict
    chunks: List[str] = None
    
    def __post_init__(self):
        if self.chunks is None:
            self.chunks = self.chunk_text(self.content)
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        overlap = 50  # Words overlap between chunks
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i+chunk_size])
            if chunk:
                chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
                
        return chunks if chunks else [text]


# ============================================================================
# VECTOR STORE (Simple In-Memory)
# ============================================================================

class VectorStore:
    """Simple in-memory vector store with cosine similarity."""
    
    def __init__(self):
        self.documents = []
        self.embeddings = []
    
    def add(self, doc: Document, embedding: List[float]):
        """Add document with embedding."""
        self.documents.append(doc)
        self.embeddings.append(embedding)
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Document, float]]:
        """Search for similar documents."""
        if not self.embeddings:
            return []
        
        scores = []
        for emb in self.embeddings:
            score = self.cosine_similarity(query_embedding, emb)
            scores.append(score)
        
        # Get top k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [(self.documents[i], scores[i]) for i in top_indices]
    
    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot = sum(x*y for x, y in zip(a, b))
        norm_a = sum(x*x for x in a) ** 0.5
        norm_b = sum(x*x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot / (norm_a * norm_b)
    
    def save(self, path: Path):
        """Save to disk."""
        data = {
            'documents': [asdict(d) for d in self.documents],
            'embeddings': self.embeddings
        }
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path: Path):
        """Load from disk."""
        with open(path, 'r') as f:
            data = json.load(f)
            self.documents = [Document(**d) for d in data['documents']]
            self.embeddings = data['embeddings']


# ============================================================================
# EMBEDDING GENERATOR
# ============================================================================

class EmbeddingGenerator:
    """Generate text embeddings using OpenRouter API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
    
    def generate(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if self.api_key == "API_KEY" or not self.api_key:
            # Fallback to hash-based pseudo-embedding
            return self._generate_hash_embedding(text)
        
        try:
            return self._generate_api_embedding(text)
        except Exception as e:
            print(f"⚠️ API error, using fallback: {e}")
            return self._generate_hash_embedding(text)
    
    def _generate_api_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/vacationtube2024-droid/alita-repo-001",
            "X-Title": "Alita Knowledge Base"
        }
        
        payload = {
            "model": "openai/text-embedding-3-small",
            "input": text[:8000]  # Limit input length
        }
        
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['data'][0]['embedding']
        else:
            raise Exception(f"API error: {response.status_code}")
    
    def _generate_hash_embedding(self, text: str) -> List[float]:
        """Generate pseudo-embedding using hash (fallback)."""
        words = text.lower().split()
        embedding = [0.0] * EMBEDDING_DIM
        
        for word in set(words):
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16) % EMBEDDING_DIM
            frequency = words.count(word)
            embedding[hash_val] = frequency
        
        # Normalize
        magnitude = sum(x*x for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x/magnitude for x in embedding]
        
        return embedding


# ============================================================================
# LLM FOR RAG (OpenRouter)
# ============================================================================

class RAGEngine:
    """RAG (Retrieval-Augmented Generation) using OpenRouter."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.model = DEFAULT_MODEL
    
    def answer(self, query: str, context_docs: List[Tuple[Document, float]]) -> str:
        """Answer query using retrieved context."""
        if not context_docs:
            return "I don't have enough information to answer that. Please add some documents to the knowledge base first."
        
        if self.api_key == "API_KEY" or not self.api_key:
            return self._fallback_answer(query, context_docs)
        
        try:
            return self._generate_answer(query, context_docs)
        except Exception as e:
            print(f"⚠️ RAG error: {e}")
            return self._fallback_answer(query, context_docs)
    
    def _prepare_context(self, context_docs: List[Tuple[Document, float]]) -> str:
        """Prepare context from retrieved documents."""
        context_parts = []
        for doc, score in context_docs:
            context_parts.append(f"[Source: {doc.source} (relevance: {score:.2f})]\n{doc.content[:500]}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def _generate_answer(self, query: str, context_docs: List[Tuple[Document, float]]) -> str:
        """Generate answer using LLM."""
        context = self._prepare_context(context_docs)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/vacationtube2024-droid/alita-repo-001",
            "X-Title": "Alita Knowledge Base"
        }
        
        prompt = f"""You are a helpful AI assistant answering questions based on a knowledge base.

Context from knowledge base:
{context}

Question: {query}

Instructions:
1. Use the context above to answer the question
2. If the context doesn't contain enough information, say so
3. Cite the sources when possible
4. Be concise but informative"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant with access to a knowledge base."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"API error: {response.status_code}")
    
    def _fallback_answer(self, query: str, context_docs: List[Tuple[Document, float]]) -> str:
        """Fallback answer without LLM."""
        if not context_docs:
            return "No relevant documents found."
        
        best_doc, score = context_docs[0]
        
        answer = f"Based on my knowledge base (relevance: {score:.2f}):\n\n"
        answer += best_doc.content[:500]
        
        if len(best_doc.content) > 500:
            answer += "...\n\n[Content truncated]"
        
        answer += f"\n\n*Source: {best_doc.source}*"
        
        if len(context_docs) > 1:
            answer += "\n\nOther relevant sources:"
            for doc, _ in context_docs[1:3]:
                answer += f"\n- {doc.source}"
        
        return answer


# ============================================================================
# KNOWLEDGE BASE ORCHESTRATOR
# ============================================================================

class KnowledgeBase:
    """Main knowledge base orchestrator."""
    
    def __init__(self, storage_path: str = "./kb_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.vector_store = VectorStore()
        self.embedding_generator = EmbeddingGenerator()
        self.rag_engine = RAGEngine()
        
        self._load()
    
    def _load(self):
        """Load from disk if available."""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            try:
                self.vector_store.load(index_file)
                print(f"📂 Loaded {len(self.vector_store.documents)} documents from storage")
            except:
                pass
    
    def _save(self):
        """Save to disk."""
        index_file = self.storage_path / "index.json"
        self.vector_store.save(index_file)
    
    def index_document(self, file_path: str, content: str = None, metadata: Dict = None) -> str:
        """Add a document to the knowledge base."""
        # Read content if not provided
        if content is None:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        doc_id = f"doc_{len(self.vector_store.documents)}"
        doc = Document(
            id=doc_id,
            content=content,
            source=file_path,
            metadata=metadata or {}
        )
        
        # Generate embeddings for each chunk
        for chunk in doc.chunks:
            embedding = self.embedding_generator.generate(chunk)
            self.vector_store.add(doc, embedding)
        
        self._save()
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Search for relevant documents."""
        query_embedding = self.embedding_generator.generate(query)
        return self.vector_store.search(query_embedding, top_k)
    
    def query(self, question: str) -> str:
        """Query the knowledge base with RAG."""
        results = self.search(question)
        return self.rag_engine.answer(question, results)
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        return {
            'total_documents': len(self.vector_store.documents),
            'total_chunks': sum(len(d.chunks) for d in self.vector_store.documents),
            'sources': list(set(d.source for d in self.vector_store.documents))
        }


# ============================================================================
# CLI
# ============================================================================

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 Alita Knowledge Base v2.1 (AI-Enhanced)")
        print("\nUsage:")
        print("  python knowledge_base_v2_ai.py index <file>   - Index a document")
        print("  python knowledge_base_v2_ai.py query <question> - Query the knowledge base")
        print("  python knowledge_base_v2_ai.py stats          - Show statistics")
        print("\nNote: Set OPENROUTER_API_KEY env var for AI features")
        return
    
    command = sys.argv[1]
    kb = KnowledgeBase()
    
    if command == "stats":
        stats = kb.get_stats()
        print("📊 Knowledge Base Statistics")
        print(f"   Documents: {stats['total_documents']}")
        print(f"   Chunks: {stats['total_chunks']}")
        print(f"   Sources: {stats['sources']}")
    
    elif command == "index":
        if len(sys.argv) < 3:
            print("Usage: python knowledge_base_v2_ai.py index <file>")
            return
        
        file_path = sys.argv[2]
        doc_id = kb.index_document(file_path)
        print(f"✅ Indexed: {file_path} (ID: {doc_id})")
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("Usage: python knowledge_base_v2_ai.py query <question>")
            return
        
        question = " ".join(sys.argv[2:])
        print(f"🔍 Question: {question}\n")
        answer = kb.query(question)
        print("="*60)
        print("ANSWER:")
        print("="*60)
        print(answer)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
