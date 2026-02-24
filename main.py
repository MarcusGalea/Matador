from src.backend.bræt import Bræt, Felt, Spiller
from src.backend.felt import Felt, Grund

import numpy as np
priser = [0, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
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
        
felter = [Grund(name, price) for name, price in zip(NAMES, priser)]
spillere = [Spiller(f"Spiller {i+1}", 0) for i in range(4)]

bræt = Bræt(felter, spillere)

import matplotlib.pyplot as plt

antal_huse = np.arange(6)
# leje_beløb = [1000, 4000,12000, 28000, 34000, 40000]
leje_beløb = [50, 250, 750, 2250, 4000, 6000]
#plot leje_beløb
plt.plot(antal_huse, leje_beløb, marker='o')
plt.show()
