from elems  import Element
from player import Player, Status
from rules  import isChoiceCorrect, canCardBeThrown

class User(Player):
    def move(self, event, table, stock_vol, rival_vol):
        # print('i am in move of user')
        ans = []
        if event.key == pygame.K_a:
            self.joystick.shiftLeft()
            
        if event.key == pygame.K_d:
            self.joystick.shiftRight()
            
        if event.key == pygame.K_s:
            if self.joystick.chooseCard():
                card = self.cards.sprites()[self.joystick.chosen_card]
                move_correct = (isChoiceCorrect(self.status, 
                                                table, 
                                                card, 
                                                self.trump) and
                                canCardBeThrown(self.status, 
                                                table, 
                                                rival_vol))
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

    def getCard(self):
        if self.status == Status.FOOL:
            card = Element.getCard(self, True, 0)
        else:
            cci = self.joystick.chosen_card
            card = Element.getCard(self, False, cci)        
            self.joystick.num -= 1
            self.updateCards()
        return card
    
    
 