from app.tools.symbol_search import SymbolSearch


class SymbolService:

    def __init__(self):

        self.search = SymbolSearch(".")

    def find(self, symbol):

        return self.search.find_symbol(symbol)