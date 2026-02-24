from src.backend.felt import Felt, Grund

class Spiller:
    def __init__(self, navn, start_pos = 0):
        self.navn = navn
        self.pos = start_pos
        self.penge = 30000
        self.ejendomme = []

    def __str__(self):
        return f"{self.navn} er på position {self.pos} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"

    def __repr__(self):
        return self.navn
    
    def konkurs(self) -> bool:
        return self.penge < 0
    
    def betal(self,
              beløb: int) -> bool:
        
        self.penge -= beløb
        if self.konkurs():
            print(f"{self.navn} er gået konkurs!")
            return False
        return True
    
    def modtag(self, beløb: int):
        self.penge += beløb

    def betal_leje(self, grund: Grund) -> bool:
        if grund.ejer is not None and grund.ejer != self:
            leje = grund.beløb()
            return self.betal(leje) and grund.ejer.modtag(leje)
        return True
    
    def køb_grund_af_bank(self, grund: Grund) -> bool:
        if grund.ejer is None and self.penge >= grund.pris:
            if self.betal(grund.pris):
                grund.ejer = self
                self.ejendomme.append(grund)
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af banken.")
        return False
