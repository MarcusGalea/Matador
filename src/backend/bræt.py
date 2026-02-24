from src.backend.spiller import Spiller
from src.backend.felt import Felt
class Bræt:
    def __init__(self, 
                 felter: list[Felt], 
                 spillere: list[Spiller]
                 ):
        self.nuværende_spiller_index = 0
        self.felter = felter
        self.spillere = spillere

    def __str__(self):
        return f"Bræt med felter: {[f.navn for f in self.felter]} og spillere: {[s.navn for s in self.spillere]}"
    

    def nuværende_spiller(self):
        return self.spillere[self.nuværende_spiller_index]
    
    def næste_spiller(self):
        self.nuværende_spiller_index = (self.nuværende_spiller_index + 1) % len(self.spillere)

    def flyt_spiller(self, spiller: Spiller, antal_felter: int):
        spiller.pos = (spiller.pos + antal_felter) % len(self.felter)

    def spiller_landede_på_felt(self, spiller: Spiller):
        felt = self.felter[spiller.pos]
        if felt.ejer is not None and felt.ejer != spiller:
            leje = felt.lejebetaling()
            spiller.penge -= leje
            felt.ejer.penge += leje