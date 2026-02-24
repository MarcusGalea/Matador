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
        self.fængsel = False
        self.fri_fængsel_kort = 0

    def __str__(self):
        return f"{self.navn} er på position {self.pos} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"

    def __repr__(self):
        return self.navn
    
    def _konkurs(self) -> bool:
        return self.penge < 0
    

    ### BEVÆGELSESMETODER ###

    def slå_terning(self) -> int:
        import random
        terning1 = random.randint(1, 6)
        terning2 = random.randint(1, 6)
        total = terning1 + terning2
        print(f"{self.navn} slog {terning1} og {terning2} og skal flytte {total} felter.")
        return total

    def _flyt(self, antal_felter: int, bræt_længde = 40):
        #modtag startbonus hvis spilleren passerer start
        if (self.pos + antal_felter) >= bræt_længde:
            self.penge += 4000
        self.pos = (self.pos + antal_felter) % bræt_længde

    def nettoformue(self) -> int:
        formue = self.penge
        for grund in self.ejendomme:
            formue += grund.pris + grund.huse * grund.hus_pris
        return formue

    ### PENGE METODER ###
    def _betal(self,beløb: int) -> bool:
        
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
        
        print(f"{self.navn} kan ikke betale leje på {grund.navn}.")
        return False


    ### KØB OG SALG METODER ###    
    def køb_grund(self, grund: Grund,pris: int = None) -> bool:
        
        if grund.ejer is None:
            return self.køb_grund_af_bank(grund)
        else:
            return self.køb_grund_af_spiller(grund, grund.ejer, pris if pris is not None else grund.pris)
        

    def køb_grund_af_bank(self, grund: Grund) -> bool:

        if grund.ejer is None and self.penge >= grund.pris:
            if self._betal(grund.pris):
                grund.ejer = self
                self.ejendomme.append(grund)
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af banken.")
        return False
    
    def køb_grund_af_spiller(self, grund: Grund, sælger: "Spiller",pris: int) -> bool:
        
        if grund.ejer == sælger and self.penge >= pris:
            if self._betal(pris):
                grund.ejer = self
                self.ejendomme.append(grund)
                sælger.ejendomme.remove(grund)
                sælger._modtag(pris)
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af {sælger.navn}.")
        return False

    def sælg_grund_til_spiller(self, grund: Grund, køber: "Spiller", pris: int) -> bool:
        if grund.ejer == self and køber.penge >= pris:
            if køber._betal(pris):
                grund.ejer = køber
                køber.ejendomme.append(grund)
                self.ejendomme.remove(grund)
                self._modtag(pris)
                return True
        print(f"{self.navn} kan ikke sælge {grund.navn} til {køber.navn}.")
        return False
    

    #### HUS KØB OG SALG METODER ####
    def køb_hus(self, grund: Grund) -> bool:
        if grund.ejer == self and self.penge >= grund.hus_pris:
            if grund.køb_hus():
                return self._betal(grund.hus_pris)
        print(f"{self.navn} kan ikke købe hus på {grund.navn}.")
        return False
    
    def sælg_hus(self, grund: Grund) -> bool:
        if grund.ejer == self and grund.huse > 0:
            if grund.sælg_hus():
                return self._modtag(grund.hus_pris)
        print(f"{self.navn} kan ikke sælge hus på {grund.navn}.")
        return False
    
    ### PANT METODER ##
    def pantsæt(self, grund: Grund) -> bool:
        if grund.ejer == self and not grund.pantsat and grund.huse == 0:
            if grund.pantsæt():
                return self._modtag(grund.pris // 2)
        print(f"{self.navn} kan ikke pantsætte {grund.navn}.")
        return False

    def frigiv_pant(self, grund: Grund) -> bool:
        if grund.ejer == self and grund.pantsat:
            if grund.frigiv_pant():
                return self._betal(grund.pris // 2)
        print(f"{self.navn} kan ikke frigive pant på {grund.navn}.")
        return False
    