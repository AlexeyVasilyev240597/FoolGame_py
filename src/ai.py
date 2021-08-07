# import pygame
from items  import Rank
from player import Player, Status
from rules  import isChoiceCorrect, canCardBeThrown

# TODO: create abstract method
#       def makeDecision(...): ... return index
#       and rewrite method 'move' of ArtInt 

# Artificial Intelligence 
class ArtInt(Player):
    def __init__(self):
        name = str(self.__class__.__name__)
        Player.__init__(self, name, False)
    
    def move(self, table, stock_vol, rival_vol):
        print('WARNING: abstract method of ArtInt does nothing')
        
    # PARAM IN: stock_vol for detecting of Endspiel
    def getAvailableCards(self, table, stock_vol, rival_vol):
        indxs = []
        if canCardBeThrown(self.status, table, rival_vol):
            for i in range(self.vol()):
                move_correct = (isChoiceCorrect(self.status, 
                                                table, 
                                                self.cards[i], 
                                                self.trump))
                if move_correct:
                    indxs.append(i)
        return indxs


class Nikita_A(ArtInt): 
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        if len(indxs) > 0:
            card = self.getCard(indxs[0])
            ans = {'card': card}
        else:
            word = self.sayWord()
            ans = {'word': word}
        return ans
    
    
class Alexander_P(ArtInt):
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        decision = False
        if len(indxs) > 0:
            if self.status == Status.DEFENDING:
                w = self.get_weight(self.cards[indxs[0]])
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
    
    
class George_P(ArtInt):
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        decision = False
        if len(indxs) > 0:
            if (self.status == Status.ATTACKER and table.vol() > 0 or
                self.status == Status.ADDING):
                w = self.get_weight(self.cards[indxs[0]])
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


class Sergey_C(ArtInt):
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        decision = False
        if len(indxs) > 0:
            # if no cards on table he throws smallest by weight card
            if table.vol() > 0 and not self.status == Status.DEFENDING:
                indx = -1
            # else he throws biggest one (no matter what status)
            else:
                indx = 0
            decision = True
        
        if decision:
            card = self.getCard(indxs[indx])
            ans = {'card': card}
        else:
            word = self.sayWord()
            ans = {'word': word}
        return ans


AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C]
def AIGenerator(ai_name):
    for ai_c in AI_list:
        ai_o = ai_c()
        if ai_name == ai_o.name:
            return ai_o
