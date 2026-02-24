from src.backend.bræt import Bræt,  Spiller
from src.backend.felt import Felt, Grund, NABOER

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
        
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
#CREATE MORE COLORS
MAGENTA = (255, 0, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_BROWN = (210, 180, 140)

COLORS = [  RED, LIGHT_BROWN, LIGHT_BROWN, LIGHT_BROWN,
            YELLOW, YELLOW, YELLOW,
            BLACK,
            GRAY, GRAY, GRAY,
            WHITE,
            BLUE, BLUE, BLUE,
            PURPLE, PURPLE, PURPLE,
            RED, RED, RED,
            LIGHT_GREEN,
            WHITE, 
            GREEN, GREEN, GREEN,
            BROWN, BROWN, BROWN,
            PINK, PINK, PINK,
            WHITE,
            MAGENTA, MAGENTA, MAGENTA,
            LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE,
            LIGHT_YELLOW, LIGHT_YELLOW,
        ]

felter = [Grund(name, color, price) for name, price, color in zip(NAMES, priser, COLORS)]
spillere = [Spiller(f"Spiller {i+1}", 0) for i in range(4)]

bræt = Bræt(felter, spillere)
bræt.spil()
