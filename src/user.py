import pygame
from elems  import Element
from player import Player, Status
from params import COLOR_CARD_WRONG
from rules  import isChoiceCorrect, canCardBeThrown

class User(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.clicked_card_indx = -1  
        self.wrong_choice = False

    def addCard(self, card):        
        Player.addCard(self, card)        

    def isCardChoosen(self, pos):
        clicked_cards = [c for c in self._cards if c.rect.collidepoint(pos)]
        if clicked_cards:
            self.clicked_card_indx = clicked_cards[-1].layer
            return True
        else:
            return False
    
    def move(self, stock_vol, rival):
        ans = []
        
        if self.clicked_card_indx >= 0:            
            card = self._showCard(self.clicked_card_indx)
            move_correct = (isChoiceCorrect(self.status, 
                                            self.table, 
                                            card, 
                                            self.trump) and
                            canCardBeThrown(self.status, 
                                            self.table, 
                                            rival.vol))
            if move_correct:
                card = self.getCard()
                ans = {'card': card}
            else:
                self.wrong_choice = True
 
        else:
            if self.table.vol() > 0:
                word = self.sayWord()                
                ans = {'word': word}
        
        return ans

    def getCard(self):
        if self.status == Status.FOOL:
            card = Element.getCard(self, True, 0)
        else:
            card = Element.getCard(self, False, self.clicked_card_indx)        
        self.updateCards()
        return card
    
    def sayWord(self):
        word = Player.sayWord(self)
        self.updateCards()
        return word
    
    def draw(self, screen):
        Player.draw(self, screen)
        if self.vol() > 0:
            if self.clicked_card_indx >= 0 and self.wrong_choice:
                rect = self._showCard(self.clicked_card_indx).rect                
                pygame.draw.rect(screen, COLOR_CARD_WRONG, rect, self.t)

    def updateCards(self):
        Player.updateCards(self)
        self.clicked_card_indx = -1
        