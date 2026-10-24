import os
from pathlib import Path


EXCLUDED = {'.git', '.aws', 'myenv', '.venv', 'venv', 'env', '__pycache__', 'node_modules', 'chroma_db', '.idea', '.vscode', 'tmp'}


def source_files(root):
    root = Path(root).resolve()
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(folder) / d).is_symlink())
        for name in sorted(files):
            path = Path(folder) / name
            if not path.is_symlink():
                yield path


class FileSearch:
    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()

    def find(self, filename):
        target = str(filename).replace('\\', '/')
        for file in source_files(self.root):
            relative = file.relative_to(self.root).as_posix()
            if relative == target or ('/' not in target and file.name == target):
                return str(file)
        return None
