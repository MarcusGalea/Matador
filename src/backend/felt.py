#Matador spil
import numpy as np
n_felter = 40

priser = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
          600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050,
          1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500,
          1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950,
          2000]

NAMES = ["START", 
        "Østerbrogade", "Grønningen", "Bredgade",
         "Kgs. Nytorv", "Østergade", "Amagertorv",
         "Fængsel",
            "Vesterbrogade", "H.C. Andersens Boulevard", "Rådhuspladsen",
            "Nørrebrogade",
            "Frederiksberg Allé", "Gammel Kongevej", "Valby Langgade",
            "Carlsberg", "Søndre Boulevard",
            "Vesterbro Torv", "Halmtorvet", "Enghave Plads",
            "Kødbyen", "Sydhavns Plads", "Sluseholmen",
            "Amager Strand", "Amager Landevej", "Ørestad",
            "Lufthavnen", "Ørestad Syd", "Ørestad Nord",
            "Refshaleøen", "Nordhavn", "Langelinie", "Kastellet",
            "Østerport", "Nørreport", "Vesterport", "Christianshavn", "Søerne",
            "Rådhuspladsen", "Kgs. Nytorv", "Nørrebrogade", "Frederiksberg Allé",
            ]
        
class Felt:
    def __init__(self, navn, pris):
        self.navn = navn
        self.pris = pris
        self.ejer = None
        self.huse = 0
    
    def __str__(self):
        return self.navn
    def __repr__(self):
        return self.navn

    