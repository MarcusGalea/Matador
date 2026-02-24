#Matador spil
from enum import Enum
import numpy as np
#import defaultdict
n_felter = 40
leje_procent_af_pris = 0.125
leje_procent_pr_hus = 0.5
        
class COLOR(Enum):
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

    def __init__(self, grunde = []):
        self.grunde = grunde
    

class Felt:
    def __init__(self, 
                 navn: str,
                 farve: str | None = None
                 ):
        self.navn = navn
        self.farve = farve

    def __str__(self):
        return self.navn
    def __repr__(self):
        return self.navn
    
class Chance(Felt):
    def __init__(self, navn: str):
        super().__init__(navn)


class Grund(Felt):
    def __init__(self, 
                 navn: str, 
                 pris: int, 
                 farve: str | None = None,
                 huspris: int | None = None,
                 alle_lejebeløb: list[int] | None = None
                 ):
        super().__init__(navn, farve=farve)

        self.ejer = None
        self.huse = 0
        self.pantsat = False
        self.hus_pris = huspris if huspris is not None else int(0.5*pris)
        self.alle_lejebeløb = [pris * leje_procent_af_pris * ((1+ leje_procent_pr_hus) ** i) for i in range(6)] if alle_lejebeløb is None else alle_lejebeløb
    

    def lejebeløb(self) -> int:
        if self.ejer is not None:
            return self.alle_lejebeløb[self.huse]
        else:
            return 0
        
    def køb_hus(self) -> bool:
        if self.huse < 5:
            self.huse += 1
            return True
        else:
            print(f"Der kan ikke købes flere huse på {self.navn}.")
            return False

    def sælg_hus(self) -> bool:
        if self.huse > 0:
            self.huse -= 1
            return True
        else:
            print(f"Der er ingen huse at sælge på {self.navn}.")
            return False
        
    def pantsæt(self) -> bool:
        if self.ejer is not None and not self.pantsat and self.huse == 0:
            self.pantsat = True
            self.pris //= 2
            return True
        else:
            print(f"{self.navn} kan ikke pantsættes.")
            return False
    
    def frigiv_pant(self) -> bool:
        if self.pantsat:
            self.pantsat = False
            self.pris *= 2
            return True
        else:
            print(f"{self.navn} er ikke pantsat.")
            return False
        
    
    
