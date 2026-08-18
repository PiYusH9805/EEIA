from pathlib import Path


class FileReader:

    def __init__(self, root="."):

        self.root = Path(root)

    def read(self, file_path):

        path = self.root / file_path

        if not path.exists():
            return None

        try:
            return path.read_text(
                encoding="utf-8"
            )
        except Exception:
            return None