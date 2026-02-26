from src.backend.spiller import Spiller
from src.backend.felt import Felt, Grund
class Bræt:
    def __init__(self, 
                 felter: list[Felt], 
                 spillere: list[Spiller]
                 ):
        self.nuværende_spiller_index = 0
        self.felter = felter
        self.spillere = spillere
        self.n_felter = len(felter)

    def __str__(self):
        return f"Bræt med felter: {[f.navn for f in self.felter]} og spillere: {[s.navn for s in self.spillere]}"
    def __repr__(self):
        return self.__str__()

    def nuværende_spiller(self):
        return self.spillere[self.nuværende_spiller_index]
    
    def næste_spiller(self):
        self.nuværende_spiller_index = (self.nuværende_spiller_index + 1) % len(self.spillere)

    def flyt_spiller(self, spiller: Spiller, antal_felter: int):
        spiller.pos = (spiller.pos + antal_felter) % len(self.felter)

    def spil_omgang(self):
        spiller = self.nuværende_spiller()
        print(f"Det er {spiller.navn}s tur.")
        if spiller.konkurs:
            print(f"{spiller.navn} er konkurs og kan ikke spille.")
            self.næste_spiller()
            return
        spiller._slå_terning_og_flyt(self.n_felter)
        nuværende_felt = self.felter[spiller.pos]
        betalt = spiller.betal_leje(nuværende_felt)
        while not betalt and not spiller.konkurs:
            print(f"{spiller.navn} skal sælge en ejendom (eller huse) for at betale leje på {nuværende_felt.navn}.")
            # Simulering af sælg ejendom
            #TODO # Implementer logik for at sælge ejendom eller huse. Indtil videre går man bare konkurs
            self.spiller.konkurs = True
            self.næste_spiller()
            return
        #user input
        if isinstance(nuværende_felt, Grund) and nuværende_felt.ejer is None:
            køb = self.bruger_input(f"Vil {spiller.navn} købe {nuværende_felt.navn} for {nuværende_felt.pris} kr? (ja/nej) ")
            if køb.lower() == "ja":
                spiller.køb_grund(nuværende_felt)
            
        self.næste_spiller()    
        return 
        
    def spil(self):
        while len([s for s in self.spillere if not s.konkurs]) > 1:
            self.spil_omgang()
        vinder = [s for s in self.spillere if not s.konkurs][0]
        print(f"{vinder.navn} har vundet spillet med en nettoformue på {vinder.nettoformue()} kr!")


    def bruger_input(self, prompt: str) -> str:
        return input(prompt)