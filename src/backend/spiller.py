from src.backend.felt import Felt, Grund

class Spiller:
    """
    En spiller i Matador. Har et navn, en position på brættet, en mængde penge og en liste af ejendomme.
    """
    
    def __init__(self, navn, start_pos = 0):
        self.navn = navn
        self.pos = start_pos
        self.penge = 30000
        self.ejendomme = []

    def __str__(self):
        return f"{self.navn} er på position {self.pos} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"

    def __repr__(self):
        return self.navn
    
    def _konkurs(self) -> bool:
        return self.penge < 0
    

    ### BEVÆGELSESMETODER ###

    def _flyt(self, antal_felter: int, bræt_længde = 40):
        #modtag startbonus hvis spilleren passerer start
        if (self.pos + antal_felter) >= bræt_længde:
            self.penge += 4000
        self.pos = (self.pos + antal_felter) % bræt_længde



    ### PENGE METODER ###
    def _betal(self,
              beløb: int) -> bool:
        
        self.penge -= beløb
        if self._konkurs():
            print(f"{self.navn} er gået konkurs!")
            return False
        return True
    
    def _modtag(self, beløb: int):
        self.penge += beløb


    def betal_leje(self, grund: Grund) -> bool:
        if grund.ejer is not None and grund.ejer != self:
            leje = grund.lejebeløb()
            return self._betal(leje) and grund.ejer._modtag(leje)
        return True
    
    def køb_grund_af_bank(self, grund: Grund) -> bool:
        if grund.ejer is None and self.penge >= grund.pris:
            if self._betal(grund.pris):
                grund.ejer = self
                self.ejendomme.append(grund)
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af banken.")
        return False
    
    def køb_grund_af_spiller(self, grund: Grund, 
                             sælger: "Spiller",
                             pris: int) -> bool:
        if grund.ejer == sælger and self.penge >= pris:
            if self._betal(pris):
                grund.ejer = self
                self.ejendomme.append(grund)
                sælger.ejendomme.remove(grund)
                sælger._modtag(pris)
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af {sælger.navn}.")
        return False
    