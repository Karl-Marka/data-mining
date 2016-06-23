
import random

class Blackjack():
    
    cards = {"Risti kolm" : 3,
            "Risti neli" : 4,
            "Risti viis": 5,
            "Risti kuus" : 6,
            "Risti seitse" : 7,
            "Risti kaheksa" : 8,
            "Risti uheksa" : 9,
            "Risti kumme" : 10,
            "Risti poiss" : 10,
            "Risti emand" : 10,
            "Risti kuningas" : 10,
            "Risti ass" : 11,
            "Ruutu kolm" : 3,
            "Ruutu neli" : 4,
            "Ruutu viis": 5,
            "Ruutu kuus" : 6,
            "Ruutu seitse" : 7,
            "Ruutu kaheksa" : 8,
            "Ruutu uheksa" : 9,
            "Ruutu kumme" : 10,
            "Ruutu poiss" : 10,
            "Ruutu emand" : 10,
            "Ruutu kuningas" : 10,
            "Ruutu ass" : 11,
            "Artu kolm" : 3,
            "Artu neli" : 4,
            "Artu viis": 5,
            "Artu kuus" : 6,
            "Artu seitse" : 7,
            "Artu kaheksa" : 8,
            "Artu uheksa" : 9,
            "Artu kumme" : 10,
            "Artu poiss" : 10,
            "Artu emand" : 10,
            "Artu kuningas" : 10,
            "Artu ass" : 11,
            "Poti kolm" : 3,
            "Poti neli" : 4,
            "Poti viis": 5,
            "Poti kuus" : 6,
            "Poti seitse" : 7,
            "Poti kaheksa" : 8,
            "Poti uheksa" : 9,
            "Poti kumme" : 10,
            "Poti poiss" : 10,
            "Poti emand" : 10,
            "Poti kuningas" : 10,
            "Poti ass" : 11,}
           
    move = 0
    sumCards = 0
    
    def __init__(self):
        self.dealer = random.sample(list(self.cards), len(self.cards))
        self.currentCardValue = int(self.cards.get(self.dealer[self.move]))
        self.sumCards += self.currentCardValue
        print("Sinu kaart on: %s" % self.dealer[self.move])
        
    def closeFunc(self):
        answer = input("Uus katse? (jah/ei):")
        if answer == "jah":
            self.move = 0
            self.sumCards = 0
            self.__init__()
            self.dealerFunc()
        elif answer == "ei":
            quit()
        else:
            self.closeFunc()
      
    
    def dealerFunc(self):
        if self.sumCards == 21:
            print('Palju onne, sa voitsid!')
            self.closeFunc()
        elif self.sumCards == 20 and "ass" in self.dealer[self.move+1]:
            answer = input('Annan veel uhe kaardi? (jah/ei):')
            if answer == "jah":
                print("Sinu kaart on: %s" % self.dealer[self.move+1])
                print('Palju onne, sa voitsid!')
                self.closeFunc()
            else:
                self.closeFunc()
        elif self.sumCards < 21:
            answer = input('Annan veel uhe kaardi? (jah/ei):')
            if answer == "jah":
                self.move += 1
                self.currentCardValue = int(self.cards.get(self.dealer[self.move]))
                print("Sinu kaart on: %s" % self.dealer[self.move])
                self.sumCards += self.currentCardValue
                self.dealerFunc()
            else:
                self.closeFunc()			
        else:
            print('Punktid lohki!')
            self.closeFunc()
			

                
    
game = Blackjack()
game.dealerFunc()


