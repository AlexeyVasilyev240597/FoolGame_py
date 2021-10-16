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

    def isClicked(self, pos):
        clicked_cards = [c for c in self._cards if c.rect.collidepoint(pos)]
        does_word_been_said = self.mess_box.rect.collidepoint(pos)
        if clicked_cards:
            self.cur_move = {'card' : clicked_cards[-1].layer}
            return True
        elif does_word_been_said:
            self.cur_move = {'word': 'word'}
            return True
        else:
            return False
    
    def move(self, stock_vol, rival):
        ans = []
        
        if 'card' in self.cur_move:            
            card = self._showCard(self.cur_move['card'])
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
 
        elif 'word' in self.cur_move:
            if self.table.vol() > 0:
                word = self.sayWord()                
                ans = {'word': word}
            else:
                self.wrong_choice = True
        
        return ans

    def getCard(self):
        if self.status == Status.FOOL:
            card = Element.getCard(self, True, 0)
        else:
            card = Element.getCard(self, False, self.cur_move['card'])        
        self.updateCards()
        return card
    
    def sayWord(self):
        word = Player.sayWord(self)
        self.updateCards()
        return word
    
    def draw(self, screen):
        Player.draw(self, screen)
        if self.vol() > 0:
            if self.wrong_choice:
                if 'card' in self.cur_move:
                    rect = self._showCard(self.cur_move['card']).rect
                elif 'word' in self.cur_move:
                    rect = self.mess_box.rect
                pygame.draw.rect(screen, COLOR_CARD_WRONG, rect, self.t)
        if self.status == Status.ATTACKER:
            self.mess_box.setText('Бито!')
        elif self.status == Status.DEFENDING:
            self.mess_box.setText('Беру!')
        elif self.status == Status.ADDING:
            self.mess_box.setText('Бери!')
        elif self.status == Status.FOOL:
            self.mess_box.setText('')
        

    def updateCards(self):
        Player.updateCards(self)
        self.cur_move = []
        self.wrong_choice = False
        