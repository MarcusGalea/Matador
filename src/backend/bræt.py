from backend.spiller import Spiller
from backend.felt import Felt, NAMES, priser
class Bræt:
    def __init__(self, antal_spillere = 4, antal_felter = 40):
        self.spillere = [Spiller(f"Spiller {i+1}", 0) for i in range(antal_spillere)]
        self.brikker = [Felt(NAMES[i], priser[i]) for i in range(antal_felter)]
