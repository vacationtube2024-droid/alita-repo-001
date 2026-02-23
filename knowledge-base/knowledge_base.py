#!/usr/bin/env python3
"""
Self-Learning Knowledge Base
An AI-powered knowledge management system.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Document:
    """Represents a document in the knowledge base."""
    id: str
    content: str
    source: str
    metadata: Dict
    
    
class KnowledgeBase:
    """Self-learning knowledge base with semantic search."""
    
    def __init__(self, storage_path: str = "./kb_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.documents: List[Document] = []
        self.index = {}
        
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
        
        # Simple keyword-based indexing (can be upgraded to embeddings)
        words = content.lower().split()
        for word in words:
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(doc_id)
            
        self._save()
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Document]:
        """Search the knowledge base for relevant documents."""
        query_words = query.lower().split()
        scores = {}
        
        for word in query_words:
            if word in self.index:
                for doc_id in self.index[word]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1
        
        # Sort by score
        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.get_doc_by_id(doc_id) for doc_id, _ in sorted_ids[:top_k]]
    
    def get_doc_by_id(self, doc_id: str) -> Optional[Document]:
        """Get a document by ID."""
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None
    
    def _save(self):
        """Save the knowledge base to disk."""
        data = [
            {
                'id': d.id,
                'content': d.content,
                'source': d.source,
                'metadata': d.metadata
            }
            for d in self.documents
        ]
        with open(self.storage_path / "index.json", 'w') as f:
            json.dump({'documents': data, 'index': self.index}, f)
    
    def _load(self):
        """Load the knowledge base from disk."""
        try:
            with open(self.storage_path / "index.json", 'r') as f:
                data = json.load(f)
                self.documents = [
                    Document(d['id'], d['content'], d['source'], d['metadata'])
                    for d in data['documents']
                ]
                self.index = data.get('index', {})
        except FileNotFoundError:
            pass
    
    def query(self, question: str) -> str:
        """Query the knowledge base using RAG-like approach."""
        results = self.search(question)
        
        if not results:
            return "I don't have enough information to answer that yet."
        
        context = "\n\n".join([f"[{r.source}]:\n{r.content[:500]}" for r in results])
        
        # In production, this would use an LLM
        # For now, return the top result
        top_result = results[0]
        return f"Based on my knowledge base:\n\n{top_result.content[:1000]}...\n\n(Source: {top_result.source})"


def main():
    """CLI for the knowledge base."""
    import sys
    
    kb = KnowledgeBase()
    kb._load()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "index":
            # Index a file
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                with open(file_path, 'r') as f:
                    content = f.read()
                doc_id = kb.index_document(file_path, content)
                print(f"Indexed: {file_path} (ID: {doc_id})")
            else:
                print("Usage: python knowledge_base.py index <file_path>")
                
        elif command == "query":
            # Query the knowledge base
            if len(sys.argv) > 2:
                question = " ".join(sys.argv[2:])
                answer = kb.query(question)
                print(answer)
            else:
                print("Usage: python knowledge_base.py query <question>")
        else:
            print("Commands: index <file_path>, query <question>")
    else:
        print("Alita Knowledge Base")
        print("Commands: index <file_path>, query <question>")


if __name__ == "__main__":
    main()
