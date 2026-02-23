#!/usr/bin/env python3
"""
Auto-Code Documenter - AI-Powered Documentation Generator
Version: 2.1 (AI-Enhanced)

This version uses OpenRouter API for intelligent documentation generation.
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================

# Replace with your OpenRouter API key, or set via environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openrouter/auto"

# Language support
SUPPORTED_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React',
    '.tsx': 'React',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.cpp': 'C++',
    '.c': 'C',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.sh': 'Shell',
    '.sql': 'SQL',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
}


# ============================================================================
# CODE SCANNER
# ============================================================================

class CodeScanner:
    """Scan repository and discover code files."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 
                           '.venv', 'dist', 'build', '.venv', 'vendor'}
    
    def scan(self) -> List[Dict]:
        """Scan repository and return file list."""
        files = []
        
        for root, dirs, filenames in os.walk(self.repo_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                    
                file_path = Path(root) / filename
                ext = file_path.suffix
                
                if ext in SUPPORTED_EXTENSIONS:
                    files.append({
                        'path': str(file_path),
                        'name': filename,
                        'extension': ext,
                        'language': SUPPORTED_EXTENSIONS.get(ext, 'Unknown'),
                        'relative_path': str(file_path.relative_to(self.repo_path))
                    })
        
        return files


# ============================================================================
# CODE ANALYZER
# ============================================================================

class CodeAnalyzer:
    """Analyze code files to extract structure."""
    
    def __init__(self):
        pass
    
    def analyze(self, file_path: str) -> Dict:
        """Analyze a single code file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        ext = Path(file_path).suffix
        
        if ext == '.py':
            return self._analyze_python(content)
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            return self._analyze_javascript(content)
        elif ext == '.go':
            return self._analyze_go(content)
        elif ext == '.rs':
            return self._analyze_rust(content)
        else:
            return self._analyze_generic(content)
    
    def _analyze_python(self, content: str) -> Dict:
        """Analyze Python code."""
        analysis = {
            'language': 'Python',
            'imports': [],
            'classes': [],
            'functions': [],
            'docstring': '',
            'top_level_vars': []
        }
        
        # Extract imports
        for match in re.finditer(r'^(?:from\s+(\S+)|import\s+(\S+))', content, re.MULTILINE):
            imp = match.group(1) or match.group(2)
            analysis['imports'].append(imp)
        
        # Extract classes
        for match in re.finditer(r'^class\s+(\w+)(?:\(([^)]+)\))?:', content, re.MULTILINE):
            analysis['classes'].append({
                'name': match.group(1),
                'bases': match.group(2).split(', ') if match.group(2) else []
            })
        
        # Extract functions
        for match in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\):', content, re.MULTILINE):
            analysis['functions'].append({
                'name': match.group(1),
                'params': match.group(2)
            })
        
        # Extract module docstring
        match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if match:
            analysis['docstring'] = match.group(1).strip()[:300]
        
        return analysis
    
    def _analyze_javascript(self, content: str) -> Dict:
        """Analyze JavaScript/TypeScript code."""
        analysis = {
            'language': 'JavaScript/TypeScript',
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'docstring': ''
        }
        
        # ES6 imports
        for match in re.finditer(r"import\s+(?:{[^}]+}|[\w*]+)\s+from\s+['\"]([^'\"]+)['\"]", content):
            analysis['imports'].append(match.group(1))
        
        # require statements
        for match in re.finditer(r"const\s+(\w+)\s+=\s+require\(['\"]([^'\"]+)['\"]\)", content):
            analysis['imports'].append(match.group(2))
        
        # Function declarations
        for match in re.finditer(r'(?:function\s+(\w+)|const\s+(\w+)\s+=\s*(?:\([^)]*\)|[^=])\s*=>)', content):
            func_name = match.group(1) or match.group(2)
            if func_name:
                analysis['functions'].append(func_name)
        
        # Classes
        for match in re.finditer(r'class\s+(\w+)', content):
            analysis['classes'].append(match.group(1))
        
        return analysis
    
    def _analyze_go(self, content: str) -> Dict:
        """Analyze Go code."""
        analysis = {
            'language': 'Go',
            'imports': [],
            'functions': [],
            'types': []
        }
        
        # Imports
        for match in re.finditer(r'import\s+"(.*?)"', content):
            analysis['imports'].append(match.group(1))
        
        # Functions
        for match in re.finditer(r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(', content):
            analysis['functions'].append(match.group(1))
        
        # Types
        for match in re.finditer(r'type\s+(\w+)\s+struct', content):
            analysis['types'].append(match.group(1))
        
        return analysis
    
    def _analyze_rust(self, content: str) -> Dict:
        """Analyze Rust code."""
        analysis = {
            'language': 'Rust',
            'uses': [],
            'structs': [],
            'functions': [],
            'impls': []
        }
        
        # Use statements
        for match in re.finditer(r'use\s+([\w:]+)', content):
            analysis['uses'].append(match.group(1))
        
        # Structs
        for match in re.finditer(r'struct\s+(\w+)', content):
            analysis['structs'].append(match.group(1))
        
        # Functions
        for match in re.finditer(r'fn\s+(\w+)', content):
            analysis['functions'].append(match.group(1))
        
        # Impl blocks
        for match in re.finditer(r'impl(?:\s+<[^>]+>)?\s+(\w+)', content):
            analysis['impls'].append(match.group(1))
        
        return analysis
    
    def _analyze_generic(self, content: str) -> Dict:
        """Generic analysis for other languages."""
        return {
            'language': 'Unknown',
            'lines': len(content.split('\n')),
            'size': len(content)
        }


# ============================================================================
# AI GENERATOR (OpenRouter Integration)
# ============================================================================

class AIGenerator:
    """Generate documentation using OpenRouter API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.model = DEFAULT_MODEL
    
    def generate_documentation(self, analysis_results: List[Dict]) -> str:
        """Generate documentation using AI."""
        if self.api_key == "API_KEY" or not self.api_key:
            return self._generate_fallback(analysis_results)
        
        # Prepare code summary for AI
        code_summary = self._prepare_summary(analysis_results)
        
        # Call OpenRouter API
        try:
            response = self._call_api(code_summary)
            return response
        except Exception as e:
            return f"# Documentation\n\n*AI generation failed: {e}*\n\n" + self._generate_fallback(analysis_results)
    
    def _prepare_summary(self, results: List[Dict]) -> str:
        """Prepare code summary for AI."""
        summary = []
        for r in results:
            if 'error' in r:
                continue
            summary.append(f"## {r.get('name', 'Unknown')}")
            if r.get('docstring'):
                summary.append(f"Docstring: {r['docstring']}")
            if r.get('classes'):
                summary.append(f"Classes: {', '.join([c['name'] for c in r['classes']])}")
            if r.get('functions'):
                summary.append(f"Functions: {', '.join([f['name'] for f in r['functions']])}")
            if r.get('imports'):
                summary.append(f"Imports: {', '.join(r['imports'][:5])}")
            summary.append("")
        return "\n".join(summary)
    
    def _call_api(self, code_summary: str) -> str:
        """Call OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/vacationtube2024-droid/alita-repo-001",
            "X-Title": "Alita Auto-Doc Generator"
        }
        
        prompt = f"""You are a code documentation expert. Analyze the following code structure and generate a comprehensive README.md for this project.

Code Structure:
{code_summary}

Generate a professional README.md with:
1. Project title and description
2. Installation instructions
3. Usage examples
4. API/Function reference
5. Any other relevant documentation

Write in markdown format."""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert code documentation generator."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
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
            raise Exception(f"API error: {response.status_code} - {response.text}")
    
    def _generate_fallback(self, results: List[Dict]) -> str:
        """Generate basic documentation without AI."""
        readme = "# Project Documentation\n\n"
        readme += f"**Total Files:** {len(results)}\n\n"
        
        # Group by language
        by_lang = {}
        for r in results:
            lang = r.get('language', 'Unknown')
            if lang not in by_lang:
                by_lang[lang] = []
            by_lang[lang].append(r)
        
        readme += "## Files by Language\n\n"
        for lang, files in sorted(by_lang.items()):
            readme += f"- **{lang}**: {len(files)} files\n"
        
        readme += "\n## Code Structure\n\n"
        for r in results:
            if 'error' in r:
                continue
            readme += f"### {r.get('name', 'Unknown')}\n"
            if r.get('docstring'):
                readme += f"_{r['docstring']}_\n\n"
            if r.get('classes'):
                readme += f"**Classes:** {', '.join([c['name'] for c in r['classes']])}\n"
            if r.get('functions'):
                readme += f"**Functions:** {', '.join([f['name'] for f in r['functions']])}\n"
            readme += "\n"
        
        readme += "---\n*Generated by Alita Auto-Code Documenter*\n"
        return readme


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class AutoDocGenerator:
    """Main orchestrator for auto-documentation."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.scanner = CodeScanner(repo_path)
        self.analyzer = CodeAnalyzer()
        self.ai_generator = AIGenerator()
    
    def run(self, use_ai: bool = True) -> Dict:
        """Run the documentation generation pipeline."""
        print(f"🔍 Scanning repository: {self.repo_path}")
        
        # Step 1: Scan files
        files = self.scanner.scan()
        print(f"📊 Found {len(files)} code files")
        
        # Step 2: Analyze each file
        analysis_results = []
        for f in files:
            print(f"  Analyzing: {f['name']}")
            analysis = self.analyzer.analyze(f['path'])
            analysis['file'] = f
            analysis_results.append(analysis)
        
        # Step 3: Generate documentation
        if use_ai:
            print("🤖 Generating AI-powered documentation...")
            documentation = self.ai_generator.generate_documentation(analysis_results)
        else:
            print("📝 Generating basic documentation...")
            documentation = self.ai_generator._generate_fallback(analysis_results)
        
        return {
            'files': files,
            'analysis': analysis_results,
            'documentation': documentation,
            'file_count': len(files)
        }


# ============================================================================
# CLI
# ============================================================================

def main():
    import sys
    
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    use_ai = '--no-ai' not in sys.argv
    
    generator = AutoDocGenerator(repo_path)
    result = generator.run(use_ai=use_ai)
    
    print("\n" + "="*60)
    print("GENERATED DOCUMENTATION")
    print("="*60)
    print(result['documentation'])
    
    # Save to file
    output_path = Path(repo_path) / "AUTO_GENERATED_README.md"
    with open(output_path, 'w') as f:
        f.write(result['documentation'])
    print(f"\n💾 Saved to: {output_path}")


if __name__ == "__main__":
    main()
