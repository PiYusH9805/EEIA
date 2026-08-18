from pathlib import Path


class FileSearch:

    def __init__(self, root="."):

        self.root = Path(root)

    def find(self, filename):

        for file in self.root.rglob(filename):

            if file.is_file():

                return str(file)

        return None