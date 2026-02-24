#Matador spil
import numpy as np
n_brikker = 40

priser = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
          600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050,
          1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500,
          1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950,
          2000]

brikker = [" Start", "Rødovrevej", "Fælles", "Hvidovrevej", "Roskildevej", "Valby Langgade", 
           "Fælles", "Allégade", "Østerbrogade", "Grønningen", "Bredgade", 
           "Købmagergade", "Fælles", "Nørregade", "Frederiksberggade", "Rådhuspladsen",
           "Østergade", "Amagertorv", "Vimmelskaftet", "Nygade", "Fælles",
           "Frederiksberg Allé", "Trøjborggade", "Gammel Kongevej", "Bernstorffsgade",
           "Vesterbrogade", "Fælles", "Istedgade", "Helgolandsgade", "Flensborggade",
           "Amerika Plads", "Langelinie Alle", "Fælles", "Nordre Toldbod",
           "Østbanegade", "Svanemøllen", "Strandpromenaden", "Fælles", "Trianglen", "Østerbrogade"]

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
        self.pos = (self.pos + afstand) % n_brikker
        
    def køb(self, brik):
        if self.penge >= brik.pris:
            self.penge -= brik.pris
            self.ejendomme.append(brik)
            brik.ejer = self
        else:
            print(f"{self.navn} har ikke nok penge til at købe {brik.navn}")
        
class Brik:
    def __init__(self, navn, pris):
        self.navn = navn
        self.pris = pris
        self.ejer = None
        
class Bræt:
    def __init__(self, antal_spillere = 4, antal_brikker = 40):
        self.spillere = [Spiller(f"Spiller {i+1}", 0) for i in range(antal_spillere)]
        self.brikker = [Brik(brikker[i], priser[i]) for i in range(antal_brikker)]
    
class Terninger:
    def kast(self):
        return np.random.randint(1, 7) + np.random.randint(1, 7)
    