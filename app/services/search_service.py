from app.tools.file_search import FileSearch


class SearchService:

    def __init__(self):

        self.search = FileSearch(".")

    def find_file(self, filename):

        return self.search.find(filename)
    