# Auto-Code Documenter - Design Document

## 1. Project Overview

**Project Name:** Auto-Code Documenter  
**Type:** AI-Powered Code Documentation Generator  
**Core Functionality:** Automatically analyze code repositories and generate comprehensive documentation using AI

## 2. Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Code Scanner   │ --> │  Code Analyzer   │ --> │  AI Generator   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                       │                        │
        v                       v                        v
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ File Discovery  │     │ AST/Regex Parse  │     │ LLM API Call    │
│ Language Detect │     │ Imports/Classes  │     │ (OpenRouter)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        |
                                                        v
                                              ┌─────────────────┐
                                              │  README/Output  │
                                              └─────────────────┘
```

## 3. Components

### 3.1 CodeScanner
- **Purpose:** Discover all files in repository
- **Input:** Repository path
- **Output:** List of files with extensions
- **Supported Languages:** Python, JavaScript, TypeScript, Go, Rust, Java, C++, Ruby, PHP, Shell

### 3.2 CodeAnalyzer
- **Purpose:** Extract code structure
- **Features:**
  - Parse imports
  - Find classes and functions
  - Extract docstrings
  - Analyze dependencies

### 3.3 AIGenerator
- **Purpose:** Generate documentation using LLM
- **API:** OpenRouter (or similar)
- **Input:** Code analysis results
- **Output:** Formatted markdown documentation

## 4. API Integration

### OpenRouter Configuration
```python
API_KEY = "API_KEY"  # Replace with actual key
MODEL = "openrouter/auto"  # or specific model
```

### Request Format
```json
{
  "model": "openrouter/auto",
  "messages": [
    {"role": "system", "content": "You are a code documentation expert"},
    {"role": "user", "content": "Generate documentation for this code..."}
  ]
}
```

## 5. Output Formats

- README.md with project overview
- Inline code comments
- API documentation
- Usage examples

## 6. Testing Strategy

- Unit tests for each component
- Integration tests with sample repos
- AI response validation
- Edge case handling

## 7. Future Enhancements

- Support more languages
- Generate API docs (OpenAPI/Swagger)
- Add diagram generation
- Multi-file context analysis
