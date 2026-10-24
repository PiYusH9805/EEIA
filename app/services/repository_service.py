import json
import re
from pathlib import Path
from app.tools.code_parser import CodeParser
from app.services.dependency_service import DependencyService
from app.services.call_graph_service import CallGraphService
from app.tools.file_reader import FileReader
from app.tools.file_search import source_files


class RepositoryService:
    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()
        self.parser = CodeParser(self.root)
        self.dependency = DependencyService(self.root)
        self.call_graph = CallGraphService(self.root)

    def get_repository_context(self):
        # Each analysis runs once, not once per file.
        return json.dumps({'files': self.parser.parse(), 'dependencies': self.dependency.analyze(),
                           'calls': self.call_graph.analyze()}, ensure_ascii=False)[:24000]

    def get_source_context(self, question, budget=18000):
        reader = FileReader(self.root)
        terms = set(re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*', question.lower()))
        ranked = []
        for path in source_files(self.root):
            if path.suffix.lower() not in {'.py', '.js', '.ts', '.tsx', '.java', '.cpp', '.md', '.yaml', '.yml', '.toml'}:
                continue
            try:
                text = reader.read(path)
            except (ValueError, OSError):
                continue
            if not text:
                continue
            relative = path.relative_to(self.root).as_posix()
            score = 100 if path.name.lower() in question.lower() or relative.lower() in question.lower() else 0
            score += len(terms & set(re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*', text.lower())))
            ranked.append((score, relative, text))
        sections = []
        for _, relative, text in sorted(ranked, key=lambda item: (-item[0], item[1]))[:5]:
            lines = text.splitlines()
            numbered = '\n'.join(f'{i+1}: {line}' for i, line in enumerate(lines))
            section = f'FILE {relative}\n' + numbered[:min(6000, budget)]
            sections.append(section)
            budget -= len(section)
            if budget <= 0:
                break
        return '\n\n'.join(sections)
