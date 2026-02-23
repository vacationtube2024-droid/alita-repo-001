#!/usr/bin/env python3
"""
Knowledge Base v2.0
Enhanced AI-powered knowledge management with vector embeddings.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


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
        """Split text into chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks


class VectorStore:
    """Simple in-memory vector store (can be upgraded to FAISS/Chroma)."""
    
    def __init__(self):
        self.documents = []
        self.embeddings = []
        
    def add(self, doc: Document, embedding: List[float]):
        """Add document with embedding."""
        self.documents.append(doc)
        self.embeddings.append(embedding)
        
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Document]:
        """Search for similar documents using cosine similarity."""
        if not self.embeddings:
            return []
            
        # Simple cosine similarity
        scores = []
        for emb in self.embeddings:
            score = self._cosine_similarity(query_embedding, emb)
            scores.append(score)
            
        # Get top k
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.documents[i] for i in top_indices]
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity."""
        dot = sum(x*y for x, y in zip(a, b))
        norm_a = sum(x*x for x in a) ** 0.5
        norm_b = sum(x*x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot / (norm_a * norm_b)


class KnowledgeBaseV2:
    """Enhanced knowledge base with semantic search."""
    
    def __init__(self, storage_path: str = "./kb_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.vector_store = VectorStore()
        self.documents = []
        
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate a simple embedding using hash-based approach.
        In production, use OpenAI embeddings or sentence-transformers.
        """
        # Simple hash-based "embedding" for demo
        # This creates a pseudo-embedding based on word frequencies
        words = text.lower().split()
        embedding = [0.0] * 100
        
        for i, word in enumerate(set(words)):
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16) % 100
            frequency = words.count(word)
            embedding[hash_val] = frequency
            
        # Normalize
        magnitude = sum(x*x for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x/magnitude for x in embedding]
            
        return embedding
    
    def index_document(self, file_path: str, content: str, metadata: Dict = None) -> str:
        """Add a document to the knowledge base."""
        doc_id = f"doc_{len(self.documents)}"
        doc = Document(
            id=doc_id,
            content=content,
            source=file_path,
            metadata=metadata or {}
        )
        
        self.documents.append(doc)
        
        # Generate embedding for each chunk
        for chunk in doc.chunks:
            embedding = self._generate_embedding(chunk)
            self.vector_store.add(doc, embedding)
            
        self._save()
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Document]:
        """Semantic search using embeddings."""
        query_embedding = self._generate_embedding(query)
        return self.vector_store.search(query_embedding, top_k)
    
    def _save(self):
        """Save to disk."""
        data = [asdict(d) for d in self.documents]
        with open(self.storage_path / "kb_v2.json", 'w') as f:
            json.dump({'documents': data}, f, indent=2)
    
    def _load(self):
        """Load from disk."""
        try:
            with open(self.storage_path / "kb_v2.json", 'r') as f:
                data = json.load(f)
                self.documents = [Document(**d) for d in data['documents']]
                for doc in self.documents:
                    for chunk in doc.chunks:
                        embedding = self._generate_embedding(chunk)
                        self.vector_store.add(doc, embedding)
        except FileNotFoundError:
            pass
    
    def query(self, question: str) -> str:
        """Query with RAG-like approach."""
        results = self.search(question)
        
        if not results:
            return "I don't have enough information to answer that yet."
        
        context = "\n\n".join([f"[{r.source}]:\n{r.content[:300]}..." for r in results[:3]])
        
        return f"""## Answer

Based on my knowledge base:

{results[0].content[:500]}...

### Sources:
"""
        + "\n".join([f"- {r.source}" for r in results[:3]])
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        return {
            'total_documents': len(self.documents),
            'total_chunks': sum(len(d.chunks) for d in self.documents),
            'sources': list(set(d.source for d in self.documents))
        }


def main():
    """CLI for knowledge base v2."""
    import sys
    
    kb = KnowledgeBaseV2()
    kb._load()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            stats = kb.get_stats()
            print("📊 Knowledge Base Statistics")
            print(f"   Documents: {stats['total_documents']}")
            print(f"   Chunks: {stats['total_chunks']}")
            print(f"   Sources: {stats['sources']}")
            
        elif command == "index":
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                with open(file_path, 'r') as f:
                    content = f.read()
                doc_id = kb.index_document(file_path, content, {'type': 'file'})
                print(f"✅ Indexed: {file_path} (ID: {doc_id})")
            else:
                print("Usage: python knowledge_base_v2.py index <file_path>")
                
        elif command == "query":
            if len(sys.argv) > 2:
                question = " ".join(sys.argv[2:])
                answer = kb.query(question)
                print(answer)
            else:
                print("Usage: python knowledge_base_v2.py query <question>")
        else:
            print("Commands: stats, index <file_path>, query <question>")
    else:
        print("🤖 Alita Knowledge Base v2.0")
        print("Commands: stats, index <file_path>, query <question>")


if __name__ == "__main__":
    main()
