from pathlib import Path


class FileReader:
    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()

    def read(self, file_path):
        path = Path(file_path)
        path = path.resolve() if path.is_absolute() else (self.root / path).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('File must be inside the configured repository.')
        if any(part in {'.git', '.aws', 'myenv', '.venv', 'venv', 'node_modules'} for part in path.relative_to(self.root).parts):
            raise ValueError('This path is excluded from source access.')
        if path.name.startswith('.env') or path.suffix.lower() in {'.pem', '.key', '.pfx'} or path.name == 'secrets.toml':
            raise ValueError('Secret files cannot be read as source context.')
        if not path.is_file():
            return None
        if path.stat().st_size > 512000:
            raise ValueError('Source file exceeds the 500 KB analysis limit.')
        return path.read_text(encoding='utf-8', errors='replace')
