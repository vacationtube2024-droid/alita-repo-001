# Auto-Code Documenter

AI-powered tool that automatically generates documentation for GitHub repositories.

## 🚀 Quick Start

```bash
# Clone or download this script
git clone https://github.com/vacationtube2024-droid/alita-repo-001.git
cd alita-repo-001/auto-doc-generator

# Run with AI (recommended)
python doc_generator_v2_ai.py /path/to/your/repo

# Run without AI (fallback mode)
python doc_generator_v2_ai.py /path/to/your/repo --no-ai
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
Open `doc_generator_v2_ai.py` and replace:
```python
OPENROUTER_API_KEY = "API_KEY"  # Replace with your key
```

## 📖 Usage Examples

### Basic Usage
```bash
# Generate docs for current directory
python doc_generator_v2_ai.py .

# Generate docs for specific repo
python doc_generator_v2_ai.py /path/to/repo

# Generate docs without AI (offline mode)
python doc_generator_v2_ai.py /path/to/repo --no-ai
```

### Output
- Generates `AUTO_GENERATED_README.md` in the target repository
- Shows file count, code structure, and analysis

## 🤖 AI Features (with API key)

With OpenRouter API key, you get:
- Intelligent README generation
- Code explanation
- Usage examples
- Professional documentation

### Supported Languages
| Language | Extension | Support |
|----------|-----------|---------|
| Python | .py | Full |
| JavaScript | .js | Full |
| TypeScript | .ts, .tsx | Full |
| Go | .go | Full |
| Rust | .rs | Full |
| Java | .java | Basic |
| C++ | .cpp, .c | Basic |
| Ruby | .rb | Basic |
| PHP | .php | Basic |

## 📁 Files

| File | Description |
|------|-------------|
| `doc_generator.py` | v1.0 - Basic documentation generator |
| `doc_generator_v2.py` | v2.0 - Enhanced with code analysis |
| `doc_generator_v2_ai.py` | v2.1 - AI-powered (recommended) |
| `DESIGN.md` | Technical design document |

## 🔒 Security Note

Never commit your API key to GitHub!
- Use environment variables
- Or keep keys in a separate `.env` file

## 📝 License

MIT License

---

*🤖 Built by Alita*
