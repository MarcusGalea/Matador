from src.backend.felt import Felt, Grund
import random
#set seed
random.seed(42)

class Spiller:
    """
    En spiller i Matador. Har et navn, en position på brættet, en mængde penge og en liste af ejendomme.
    """

    def __init__(self, navn, start_pos = 0):
        self.navn = navn
        self.pos = start_pos
        self.penge = 30000
        self.ejendomme = []
        
        self.konkurs = False

    def __str__(self):
        return f"{self.navn} er på position {self.pos} og har {self.penge} kr. og ejendomme: {[e.navn for e in self.ejendomme]}"

    def __repr__(self):
        return self.navn
    
    def _konkurs(self) -> bool:
        return self.penge < 0
    
    def nettoformue(self) -> int:
        ejendomsværdi = sum(grund.pris + grund.huse * grund.hus_pris for grund in self.ejendomme)
        print(f"{self.navn} har en nettoformue på {self.penge} kr. i kontanter og {ejendomsværdi} kr. i ejendomme, for en samlet nettoformue på {self.penge + ejendomsværdi} kr.")
        return self.penge + ejendomsværdi

    ### BEVÆGELSESMETODER ###

    def _slå_terning_og_flyt(self, bræt_længde = 40):
        antal_felter = self._slå_terning()
        self._flyt(antal_felter, bræt_længde)


    def _slå_terning(self) -> int:
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
        print(f"{self.navn} flytter til position {self.pos}.")



    ### PENGE METODER ###
    def _betal(self,beløb: int) -> bool:
        
        if self.penge >= beløb:
            self.penge -= beløb
            print(f"{self.navn} betaler {beløb} kr. og har nu {self.penge} kr. tilbage.")
            return True
        else:
            print(f"{self.navn} har ikke nok penge til at betale {beløb} kr. og har kun {self.penge} kr. tilbage.")
            nettoformue = self.nettoformue()
            if nettoformue >= beløb:
                print(f"{self.navn} har en nettoformue på {nettoformue} kr. og kan derfor betale {beløb} kr. ved at sælge ejendomme.")
            else:
                print(f"{self.navn} har en nettoformue på {nettoformue} kr. og kan derfor ikke betale {beløb} kr. og går konkurs.")
                self.konkurs = True
            return False
    
    def _modtag(self, beløb: int):
        print(f"{self.navn} modtager {beløb} kr.")
        self.penge += beløb


    def betal_leje(self, grund: Grund) -> bool:
        if grund.ejer is not None and grund.ejer != self:
            leje = grund.lejebeløb()
            if self._betal(leje):
                print(f"{self.navn} betaler {leje} kr. i leje til {grund.ejer.navn} for at lande på {grund.navn}.")
                grund.ejer._modtag(leje)
                return True
            else:
                print(f"{self.navn} har ikke nok penge til at betale leje på {grund.navn}.")
                return False
        else:
            print(f"{self.navn} lander på {grund.navn}, som ikke har en ejer eller ejes af spilleren selv, så der skal ikke betales leje.")
            return True


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
                print(f"{self.navn} køber {grund.navn} af banken for {grund.pris} kr.")
                return True
        print(f"{self.navn} kan ikke købe {grund.navn} af banken.")
        return False
    
    def køb_grund_af_spiller(self, grund: Grund,pris: int) -> bool:
        sælger = grund.ejer
        if sælger is not None and self.penge >= pris:
            if self._betal(pris):
                print(f"{self.navn} køber {grund.navn} af {sælger.navn} for {pris} kr.")
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
                print(f"{self.navn} sælger {grund.navn} til {køber.navn} for {pris} kr.")
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
                print(f"{self.navn} køber hus på {grund.navn} for {grund.hus_pris} kr.")
                return self._betal(grund.hus_pris)
        print(f"{self.navn} kan ikke købe hus på {grund.navn}.")
        return False
    
    def sælg_hus(self, grund: Grund) -> bool:
        if grund.ejer == self and grund.huse > 0:
            if grund.sælg_hus():
                print(f"{self.navn} sælger hus på {grund.navn} for {grund.hus_pris//2} kr.")
                return self._modtag(grund.hus_pris//2)
        print(f"{self.navn} kan ikke sælge hus på {grund.navn}.")
        return False
    
    ### PANT METODER ##
    def pantsæt(self, grund: Grund) -> bool:
        if grund.ejer == self and not grund.pantsat and grund.huse == 0:
            if grund.pantsæt():
                print(f"{self.navn} pantsætter {grund.navn} for {grund.pris} kr.")
                return self._modtag(grund.pris // 2)
        print(f"{self.navn} kan ikke pantsætte {grund.navn}.")
        return False

    def frigiv_pant(self, grund: Grund) -> bool:
        if grund.ejer == self and grund.pantsat:
            if grund.frigiv_pant():
                print(f"{self.navn} frigiver pant på {grund.navn} for {grund.pris} kr.")
                return self._betal(grund.pris // 2)
        print(f"{self.navn} kan ikke frigive pant på {grund.navn}.")
        return False
    
    def færdig(self):
        print(f"{self.navn} er færdig med sin tur.")
        return True