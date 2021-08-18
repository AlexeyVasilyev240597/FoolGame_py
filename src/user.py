import pygame
from elems  import Element
from player import Player, Status
from params import COLOR_CARD_ACTIVE, COLOR_CARD_WRONG
from rules  import isChoiceCorrect, canCardBeThrown

# BUG: во время попытки выбрать последнюю карту в наборе
#   line 94, in draw: rect = self.cards.sprites()[self.joystick.active_card].rect

class Joystick:
    def __init__(self):
        self.active_card = -1
        self.chosen_card = -1
        self.num = 0
        self.wrong_choice = False

    def shiftRight(self):
        if not self.chosen_card == -1:
            self.chosen_card = -1
        self.active_card += 1            
        if self.active_card >= self.num:
            self.active_card = self.num-1

    def shiftLeft(self):
        if not self.chosen_card == -1:
            self.chosen_card = -1
        self.active_card -= 1
        if self.active_card < 0:
            self.active_card = 0
            
    def chooseCard(self):
        if self.active_card >= 0:
            self.chosen_card = self.active_card
            return True
        return False


class User(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.joystick = Joystick()        

    def addCard(self, card):        
        Player.addCard(self, card)
        self.joystick.num += 1

    def move(self, event, stock_vol, rival):
        ans = []
        if event.key == pygame.K_a:
            self.joystick.shiftLeft()
            
        if event.key == pygame.K_d:
            self.joystick.shiftRight()
            
        if event.key == pygame.K_s:
            if self.joystick.chooseCard():
                card = self.showCard(self.joystick.chosen_card)
                move_correct = (isChoiceCorrect(self.status, 
                                                self.table, 
                                                card, 
                                                self.trump) and
                                canCardBeThrown(self.status, 
                                                self.table, 
                                                rival.vol))
                if move_correct:
                    card = self.getCard()
                    self.updateCards()
                    ans = {'card': card}
                else:
                    self.joystick.wrong_choice = True
 
        if event.key == pygame.K_w:
            if self.table.vol() > 0:
                word = self.sayWord()                
                ans = {'word': word}
        
        return ans

    def getCard(self):
        if self.status == Status.FOOL:
            card = Element.getCard(self, True, 0)
        else:
            cci = self.joystick.chosen_card
            card = Element.getCard(self, False, cci)        
            self.joystick.num -= 1
        self.updateCards()
        return card
    
    def sayWord(self):
        word = Player.sayWord(self)
        self.updateCards()
        return word
    
    def draw(self, screen):
        Player.draw(self, screen)
        if self.vol() > 0:
            if self.joystick.active_card >= 0:
                rect = self.showCard(self.joystick.active_card).rect
                pygame.draw.rect(screen, COLOR_CARD_ACTIVE, rect, self.t)
            if self.joystick.chosen_card >= 0 and self.joystick.wrong_choice:
                rect = self.showCard(self.joystick.chosen_card).rect                
                pygame.draw.rect(screen, COLOR_CARD_WRONG, rect, self.t)

    def updateCards(self):
        Player.updateCards(self)
        self.joystick.active_card = -1
        self.joystick.chosen_card = -1
        