import pygame
from elems import Element
from player import Player
from rules import isChoiceCorrect, canCardBeThrown

# Artificial Intelligence 
class ArtInt(Player):
    def __init__(self, name, id):
        Player.__init__(self, name, id, 'ai')
    
    def move(self, table, stock_vol, rival_vol):
        print('WARNING: abstract method of ArtInt does nothing')
        
    def getAvailableCards(self, table, stock_vol, rival_vol):
        indxs = []
        cards = self.cards.sprites()
        for i in range(self.vol()):
            if isChoiceCorrect(self.status, table, cards[i], self.trump) and canCardBeThrown(self.status, table, rival_vol):
                indxs.append(i)
        return indxs
        
# TODO: write factory of AI that creates object by name of AI

class NikitaA(ArtInt):
    def __init__(self, id):
        Player.__init__(self, 'Nikita A', id, 'ai')
    
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        if len(indxs) == 0:
            word = self.sayWord()
            ans = {'word': word}
        else:
            # DEBUG            
            card = Element.getCard(self, False, indxs[0])
            self.updateCards()
            ans = {'card': card}
        return ans
      