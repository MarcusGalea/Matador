import random
import numpy as np

class lykkekort:
    def __init__(self):
        self.fængsel=False
        self.cards = [
            self.card1,
            self.card2,
            self.card3,
            self.card4,
            self.card5,
            self.card6,
            self.card7,
            self.card8,
            self.card9,
            self.card10,
            self.card11,
            self.card12,
            self.card13,
            self.card14,
            self.card15,
            self.card16
            self.card17,
            self.card18,
            self.card19,
            self.card20
        ]
        
        def card14(self,spiller):
            self.gentagelser=0
            spiller._modtag(200)
            print(f'{spiller.navn} har trukket et lykkekort og skal modtage 200 kr.')

        def card13(self,spiller):
            self.gentagelser=1
            spiller._betal(200)
            print(f'{spiller.navn} har trukket et lykkekort og skal betale 200 kr.')
        
        def card1(self,spiller):
            self.gentagelser=2
            spiller._modtag(500)
            print(f'{spiller.navn} har trukket et lykkekort og skal modtage 500 kr.')

        def card2(self,spiller):
            self.gentagelser=0
            spiller._betal(500)
            print(f'{spiller.navn} har trukket et lykkekort og skal betale 500 kr.')

        def card3(self,spiller):
            self.gentagelser=4
            spiller._modtag(1000)
            print(f'{spiller.navn} har trukket et lykkekort og skal modtage 1000 kr.')

        def card4(self,spiller):
            self.gentagelser=0
            spiller._betal(1000)
            print(f'{spiller.navn} har trukket et lykkekort og skal betale 1000 kr.')

        def card5(self,spiller):
            self.gentagelser=0
            spiller._modtag(2000)
            print(f'{spiller.navn} har trukket et lykkekort og skal modtage 2000 kr.')

        def card6(self,spiller):
            self.gentagelser=1
            spiller._betal(2000)
            print(f'{spiller.navn} har trukket et lykkekort og skal betale 2000 kr.')

        def card7(self,spiller):
            self.gentagelser=1
            spiller._betal(3000)

        def card8(self,spiller):
            self.gentagelser=1
            spiller._modtag(3000)
            print(f'{spiller.navn} har trukket et lykkekort og skal modtage 3000 kr.')

        def card9(self,spiller): #Fri fængsel kort
            self.gentagelser=2
            spiller.fri_fængsel_kort += 1
            print(f'{spiller.navn} har trukket et lykkekort og har nu {spiller.fri_fængsel_kort} fri fængsel kort.')

        def card12(self,spiller): #Sættes i fængsel
            self.gentagelser=1
            spiller.fængsel = True
            print(f'{spiller.navn} har trukket et lykkekort og er nu i fængsel. Get rekt')

        def card10(self,spiller): #Lykkekortet!
            self.gentagelser=1
            self.sum = 0
            self.sum+=spiller.nettoformue()
            if self.sum <= 15000:
                spiller._modtag(40000)
                print(f'spiller har trukket lykkekortet og har vunder 40000 kr, da nettoformuen var {self.sum} kr.')
            else:
                print(f'spiller har trukket lykkekortet og har ikke vundet noget, da nettoformuen er over 15000 kr. womp womp')

        def card11(self,spiller): #Færgekort
            self.gentagelser=1
            #TODO: Tilføj et færge kort 

        def card15(self,spiller,placering): #Random placering
            self.gentagelser=1
            placering=np.linspace(0,39,40)
            self.lokation=random.choice(placering)
            gamle_pos=spiller.pos
            spiller.pos=self.lokation
            print(f'{spiller.navn} har trukket et lykkekort og skal flytte til position {self.lokation}.')
            if self.lokation < gamle_pos:
                spiller._modtag(4000)
            