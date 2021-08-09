# import pygame
from items  import Rank
from player import Player, Status
from rules  import isChoiceCorrect, canCardBeThrown

# Artificial Intelligence 
class ArtInt(Player):
    def __init__(self):
        name = str(self.__class__.__name__)
        Player.__init__(self, name, False)
    
    def move(self, table, stock_vol, rival_vol):
        indxs = self.getAvailableCards(table, stock_vol, rival_vol)
        dcsn = self.makeDecision(indxs, table, stock_vol, rival_vol)
        
        if dcsn:
            indx = self.getCardIndx(indxs, table, stock_vol, rival_vol)
            card = self.getCard(indx)
            mv = {'card': card}
        else:
            word = self.sayWord()
            mv = {'word': word}
        return mv
    
    # decision "do I throw any card?"
    def makeDecision(self, indxs, table, stock_vol, rival_vol):
        print('WARNING: abstract method of ArtInt does nothing')
    
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        print('WARNING: abstract method of ArtInt does nothing')
    
    # PARAM IN: stock_vol for detecting of Endspiel
    def getAvailableCards(self, table, stock_vol, rival_vol):
        indxs = []
        if canCardBeThrown(self.status, table, rival_vol):
            for i in range(self.vol()):
                card = self.showCard(i)
                move_correct = (isChoiceCorrect(self.status, 
                                                table, 
                                                card, 
                                                self.trump))
                if move_correct:
                    indxs.append(i)
        return indxs


class Nikita_A(ArtInt): 
    def makeDecision(self, indxs, table, stock_vol, rival_vol):
        if len(indxs) > 0:
            return True            
        else:
            return False
        
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        return indxs[0]
        
       
class Alexander_P(ArtInt):
    def makeDecision(self, indxs, table, stock_vol, rival_vol):
        if len(indxs) > 0:
            if self.status == Status.DEFENDING:
                w = self.get_weight(self.showCard(indxs[0]))
                if w <= Rank.TEN.value:
                    return True
            else:
                return True
        return False
    
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        return indxs[0]


class George_P(ArtInt):
    def makeDecision(self, indxs, table, stock_vol, rival_vol): 
        if len(indxs) > 0:
            if (self.status == Status.ATTACKER and table.vol() > 0 or
                self.status == Status.ADDING):
                w = self.get_weight(self.showCard(indxs[0]))
                if w <= Rank.TEN.value:
                    return True
            else:
                return True   
        return False
        
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        return indxs[0]


class Gregory_P(ArtInt):
    def makeDecision(self, indxs, table, stock_vol, rival_vol): 
        if len(indxs) > 0:
            # if it is not 1st move in party and
            # it is not endspiel yet then 
            # I am weighting card
            if table.vol() > 0 and stock_vol > 0:
                w = self.get_weight(self.showCard(indxs[0]))
                if w <= Rank.TEN.value:
                    return True
            else:
                return True   
        return False
     
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        return indxs[0]

class Sergey_C(ArtInt):
    def makeDecision(self, indxs, table, stock_vol, rival_vol): 
        if len(indxs) > 0:
            return True
        else:
            return False
        
    # if no cards on table he throws smallest by weight card,
    # else he throws biggest one 
    def getCardIndx(self, indxs, table, stock_vol, rival_vol):
        if table.vol() > 0 and not self.status == Status.DEFENDING:
            return indxs[-1]
        return indxs[0]


AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C, Gregory_P]
def AIGenerator(ai_name):
    for ai_c in AI_list:
        ai_o = ai_c()
        if ai_name == ai_o.name:
            return ai_o
