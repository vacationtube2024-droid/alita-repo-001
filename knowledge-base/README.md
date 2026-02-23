# Self-Learning Knowledge Base

An AI-powered knowledge management system with semantic search and RAG (Retrieval-Augmented Generation).

## 🚀 Quick Start

```bash
# Clone or download this script
git clone https://github.com/vacationtube2024-droid/alita-repo-001.git
cd alita-repo-001/knowledge-base

# Index a document
python knowledge_base_v2_ai.py index myfile.txt

# Query the knowledge base
python knowledge_base_v2_ai.py query "What is this about?"
```

## 📋 Requirements

- Python 3.8+
- (Optional) OpenRouter API key for AI features

## 🔑 API Key Setup

### Option 1: Environment Variable (Recommended)
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### Option 2: Edit the Script
Open `knowledge_base_v2_ai.py` and replace:
```python
OPENROUTER_API_KEY = "API_KEY"  # Replace with your key
```

## 📖 Usage Examples

### 1. Check Statistics
```bash
python knowledge_base_v2_ai.py stats
```
Output:
```
📊 Knowledge Base Statistics
   Documents: 5
   Chunks: 20
   Sources: ['file1.txt', 'file2.py', ...]
```

### 2. Index a Document
```bash
# Index a text file
python knowledge_base_v2_ai.py index myfile.txt

# Index a Python file
python knowledge_base_v2_ai.py index myscript.py

# Index a Markdown file
python knowledge_base_v2_ai.py index README.md
```

### 3. Query the Knowledge Base
```bash
# Ask a question
python knowledge_base_v2_ai.py query "What is this project about?"

# Ask about specific topic
python knowledge_base_v2_ai.py query "How do I use authentication?"
```

## 🤖 AI Features (with API key)

With OpenRouter API key, you get:
- **Semantic Search**: Find relevant documents using embeddings
- **RAG-powered Answers**: AI-generated answers based on your documents
- **Better Relevance**: More accurate search results

Without API key, it uses:
- **Hash-based Embeddings**: Simple fallback search
- **Keyword Matching**: Basic document retrieval

## 🏗️ Architecture

```
User Query → Embedding Model → Vector Database → Top-K Results → LLM → Answer
                                                    ↑
Document → Chunking → Embedding → Storage ──────────┘
```

## 💾 Data Storage

Documents are stored in `kb_data/index.json`:
```
knowledge-base/
├── kb_data/
│   └── index.json    # Your indexed documents
└── knowledge_base_v2_ai.py
```

## 📁 Files

| File | Description |
|------|-------------|
| `knowledge_base.py` | v1.0 - Basic keyword search |
| `knowledge_base_v2.py` | v2.0 - Vector embeddings |
| `knowledge_base_v2_ai.py` | v2.1 - AI-powered RAG (recommended) |
| `DESIGN.md` | Technical design document |

## 🔒 Security Note

Never commit your API key to GitHub!
- Use environment variables
- Or keep keys in a separate `.env` file

## 🚢 Use Cases

- **Personal Wiki**: Store and query your notes
- **Codebase Search**: Index your code and ask questions
- **Document Q&A**: Create a Q&A system for your documents
- **Research Assistant**: Index papers and ask questions

## 📝 License

MIT License

---

*🤖 Built by Alita*
