import pygame
from player import Player
from params import COLOR_CARD_WRONG
from rules  import isChoiceCorrect, canCardBeThrown

class User(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.wrong_choice = False   

    def isClicked(self, pos):
        clicked_cards = [c for c in self._cards if c.rect.collidepoint(pos)]
        is_word_said = self.mess_box.rect.collidepoint(pos)
        if clicked_cards:
            self.cur_move = {'card' : clicked_cards[-1].layer}
            return True
        elif is_word_said:
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
                card = self.getCard(self.cur_move['card'])
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
    
    def draw(self, screen):
        Player.draw(self, screen)
        if self.vol() > 0:
            if self.wrong_choice:
                if 'card' in self.cur_move:
                    rect = self._showCard(self.cur_move['card']).rect
                elif 'word' in self.cur_move:
                    rect = self.mess_box.rect
                pygame.draw.rect(screen, COLOR_CARD_WRONG, rect, self.t)        
