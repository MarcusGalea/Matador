from brik import brikker

class Spiller:
    def __init__(self, navn, start_pos = 0):
        self.navn = navn
        self.pos = start_pos
        self.penge = 1500
        self.ejendomme = []

    def __str__(self):
        return f"{self.navn} er på {brikker[self.pos]} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"
    def __repr__(self):
        return self.navn
    
    
    def flyt(self, afstand):
        self.pos = (self.pos + afstand) % len(brikker)
        
    def køb(self, brik):
        if self.penge >= brik.pris:
            self.penge -= brik.pris
            self.ejendomme.append(brik)
            brik.ejer = self
        else:
            print(f"{self.navn} har ikke nok penge til at købe {brik.navn}")