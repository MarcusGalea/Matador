from backend.felt import Felt, NAMES, priser

class Spiller:
    def __init__(self, navn, start_pos = 0):
        self.navn = navn
        self.pos = start_pos
        self.penge = 1500
        self.ejendomme = []

    def __str__(self):
        return f"{self.navn} er på {NAMES[self.pos]} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"
    def __repr__(self):
        return self.navn
    

    def flyt(self, afstand):
        self.pos = (self.pos + afstand) % len(NAMES)
        
    def køb(self, felt):
        if self.penge >= felt.pris:
            self.penge -= felt.pris
            self.ejendomme.append(felt)
            felt.ejer = self
        else:
            print(f"{self.navn} har ikke nok penge til at købe {felt.navn}.")