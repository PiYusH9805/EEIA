from pathlib import Path
from app.tools.symbol_search import SymbolSearch


class SymbolService:

    def __init__(self):

        self.search = SymbolSearch(Path(__file__).resolve().parents[2])

    def find(self, symbol):

        return self.search.find_symbol(symbol)