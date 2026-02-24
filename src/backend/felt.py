#Matador spil
from enum import Enum
import numpy as np
#import defaultdict
from collections import defaultdict

n_felter = 40
leje_procent_af_pris = 0.125
leje_procent_pr_hus = 0.5



class Felt:
    """
    Et felt på brættet. Har et navn og en farve (for at kunne tegne det senere).
    """
    naboer = defaultdict(list) #en dictionary der holder styr på felter af samme farve
    def __init__(self, 
                 navn: str,
                 farve: tuple,
                 ):
        self.navn = navn
        self.farve = farve #rgb tuple 
        Felt.naboer[self.farve].append(self) #liste over felter med samme farve

    def __str__(self):
        return self.navn
    def __repr__(self):
        return self.navn

        
    


class Grund(Felt):
    """
    En grund, som kan købes af en spiller. Den har en pris, og hvis en anden spiller lander på den, skal de betale leje til ejeren.
    """
    def __init__(self, 
                 navn: str, 
                 farve: tuple = (255, 255, 255),
                 pris: int = 0,  
                 huspris: int | None = None,
                 alle_lejebeløb: list[int] | None = None,
                 ):
        super().__init__(navn, farve)
        
        self.pris = pris #prisen for at købe grunden
        self.ejer = None # ingen ejer i starten
        self.huse = 0 # antal huse på grunden, starter med 0
        self.pantsat = False # om grunden er pantsat eller ej

        self.hus_pris = huspris if huspris is not None else int(0.5*pris)
        self.alle_lejebeløb = [pris * leje_procent_af_pris * ((1+ leje_procent_pr_hus) ** i) for i in range(6)] if alle_lejebeløb is None else alle_lejebeløb
    

    def lejebeløb(self) -> int:
        if self.ejer is not None:
            return self.alle_lejebeløb[self.huse]
        else:
            return 0
        
    def køb_hus(self) -> bool:
        same_owner = all(felt.ejer == self.ejer for felt in Felt.naboer[self.farve])
        if not same_owner:
            print(f"Alle grunde i farven {self.farve} skal ejes af samme spiller for at kunne købe hus.")
            return False
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
        
    
    

class Chance(Felt):
    """
    Chance feltet, hvor spilleren trækker et chancekort."""
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO


class Fængsel(Felt):
    """
    Fængselsfeltet, hvor spilleren kommer i fængsel, hvis de lander på det. Spilleren kan komme ud af fængslet ved at betale en bøde eller ved at bruge et "kom ud af fængsel gratis" kort.
    """
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO

class MolsLinjen(Felt):
    """
    Mols Linjen feltet, hvor spilleren skal betale for at køre med Mols Linjen, hvis de lander på det.
    """
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO

class Scandlines(Felt):
    """
    Scandlines feltet, hvor spilleren skal betale for at køre med Scandlines, hvis de lander på det.
    """
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO

class Skat(Felt):
    """
    Skat feltet, hvor spilleren skal betale skat til parkering, hvis de lander på det.
    """
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO

class Parkering(Felt):
    """
    Gratis parkeringsfeltet, hvor spilleren kan samle alle de penge, der er betalt i skat, hvis de lander på det.
    """
    def __init__(self, navn: str, farve = (0,0,0)):
        super().__init__(navn, farve)
    #TODO
