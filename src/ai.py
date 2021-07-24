# import pygame
from params import FLAG_DEBUG
from items  import Rank
from elems  import Element
from player import Player, Status
from rules  import isChoiceCorrect, canCardBeThrown

# Artificial Intelligence 
class ArtInt(Player):
    def __init__(self, name):
        Player.__init__(self, name, False)
    
    def getCard(self, indx = 0):
        flip_flag = not (FLAG_DEBUG ^ (self.status == Status.FOOL))
        card = Element.getCard(self, flip_flag, indx)
        self.updateCards()
        return card
    
    def move(self, table, stock_vol, rival_vol):
        print('WARNING: abstract method of ArtInt does nothing')
        
    def getAvailableCards(self, table, stock_vol, rival_vol):
        indxs = []
        cards = self.cards.sprites()
        for i in range(self.vol()):
            move_correct = (isChoiceCorrect(self.status, 
                                            table, 
                                            cards[i], 
                                            self.trump) and
                            canCardBeThrown(self.status, 
                                            table, 
                                            rival_vol))
            if move_correct:
                indxs.append(i)
        return indxs
        
# TODO: write factory of AI that creates object by name of AI

class NikitaA(ArtInt):
    def __init__(self):
        ArtInt.__init__(self, 'Nikita_A')
    
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        if len(indxs) > 0:
            card = self.getCard(indxs[0])
            ans = {'card': card}
        else:
            word = self.sayWord()
            ans = {'word': word}
        return ans
    
    
class AlexanderP(ArtInt):
    def __init__(self):
        ArtInt.__init__(self, 'Alexander_P')
    
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        decision = False
        if len(indxs) > 0:
            if self.status == Status.DEFENDING:
                w = self.get_weight(self.cards.sprites()[indxs[0]])
                if w <= Rank.TEN.value:
                    decision = True
            else:
                decision = True

        if decision:
            card = self.getCard(indxs[0])
            ans = {'card': card}
        else:
            word = self.sayWord()
            ans = {'word': word}
        return ans
    
    
class GeorgeP(ArtInt):
    def __init__(self):
        ArtInt.__init__(self, 'George_P')
    
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        decision = False
        if len(indxs) > 0:
            if (self.status == Status.ATTACKER and table.vol() > 0 or
                self.status == Status.ADDING):
                w = self.get_weight(self.cards.sprites()[indxs[0]])
                if w <= Rank.TEN.value:
                    decision = True
            else:
                decision = True
        
        if decision:
            card = self.getCard(indxs[0])
            ans = {'card': card}
        else:
            word = self.sayWord()
            ans = {'word': word}
        return ans

    
