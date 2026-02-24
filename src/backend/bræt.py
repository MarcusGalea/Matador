from spiller import Spiller
from brik import Brik, priser, brikker

class Bræt:
    def __init__(self, antal_spillere = 4, antal_brikker = 40):
        self.spillere = [Spiller(f"Spiller {i+1}", 0) for i in range(antal_spillere)]
        self.brikker = [Brik(brikker[i], priser[i]) for i in range(antal_brikker)]