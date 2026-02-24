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

        
class Brik:
    def __init__(self, navn, pris):
        self.navn = navn
        self.pris = pris
        self.ejer = None
        

    