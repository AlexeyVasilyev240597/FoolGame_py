import pygame
from elems  import Element
from player import Player, Type, Status
from params import COLOR_CARD_ACTIVE, COLOR_CARD_WRONG
from rules  import isChoiceCorrect, canCardBeThrown

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
        if self.active_card == self.num:
            self.active_card = self.num-1

    def shiftLeft(self):
        if not self.chosen_card == -1:
            self.chosen_card = -1
        self.active_card -= 1
        if self.active_card < 0:
            self.active_card = 0

class User(Player):
    def __init__(self, name, id):
        Player.__init__(self, name, id, Type.USER)
        self.joystick = Joystick()        

    def addCard(self, card):        
        Player.addCard(self, card)
        self.joystick.num += 1

    def move(self, event, table, stock_vol, rival_vol):
        # print('i am in move of user')
        ans = []
        if event.key == pygame.K_a:
            self.joystick.shiftLeft()
            
        if event.key == pygame.K_d:
            self.joystick.shiftRight()
            
        if event.key == pygame.K_s:
            if self.joystick.active_card >= 0:
                self.joystick.chosen_card = self.joystick.active_card
            card = self.showChosenCard()
            if not card == []:
                right_card = isChoiceCorrect(self.status, table, card, self.trump)
                enough_space = canCardBeThrown(self.status, table, rival_vol)
                move_correct = right_card and enough_space
                if move_correct:
                    card = self.getCard()
                    self.updateCards()
                    ans = {'card': card}
                else:
                    self.joystick.wrong_choice = True
 
        if event.key == pygame.K_w:
            if table.vol() > 0:
                word = self.sayWord()                
                ans = {'word': word}
        
        return ans

    def showChosenCard(self):
        # chosen card index
        cci = self.joystick.chosen_card
        if cci >= 0:
            card = self.cards.sprites()[cci]
        else:
            card = []
        return card

    def getCard(self):
        if self.status == Status.FOOL:
            card = Element.getCard(self, True, 0)
        else:
            cci = self.joystick.chosen_card
            if cci >= 0:
                card = Element.getCard(self, False, cci)        
                self.joystick.num -= 1
                self.updateCards()
            else:
                card = []
        return card
    
    def sayWord(self):
        word = Player.sayWord(self)
        self.updateCards()
        return word
    
    def draw(self, screen):
        Player.draw(self, screen)
        if self.joystick.active_card >= 0:
            rect = self.cards.sprites()[self.joystick.active_card].rect
            pygame.draw.rect(screen, COLOR_CARD_ACTIVE, rect, self.t)
        if self.joystick.chosen_card >= 0 and self.joystick.wrong_choice:
            rect = self.cards.sprites()[self.joystick.chosen_card].rect                
            pygame.draw.rect(screen, COLOR_CARD_WRONG, rect, self.t)

    def updateCards(self):
        Player.updateCards(self)
        self.joystick.active_card = -1
        self.joystick.chosen_card = -1
        