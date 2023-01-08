# import pygame
from card  import Rank
from player import Player, Status
from rules  import isChoiceCorrect, canCardBeThrown

# Artificial Intelligence 
class ArtInt(Player):
    def __init__(self):
        name = str(self.__class__.__name__)
        Player.__init__(self, name, False)
    
    def move(self, stock_vol, rival):
        indxs = self.getAvailableCards(stock_vol, rival.vol)
        dcsn  = self.makeDecision(indxs, stock_vol, rival)
        
        if dcsn:
            indx = self.getCardIndx(indxs, stock_vol, rival)
            card = self.getCard(indx)
            mv = {'card': card}
        else:
            word = self.sayWord()
            mv = {'word': word}
        return mv
    
    # decision "do I throw any card?"
    def makeDecision(self, indxs, stock_vol, rival):
        print('WARNING: abstract method of ArtInt does nothing')
    
    def getCardIndx(self, indxs, table, stock_vol, rival):
        print('WARNING: abstract method of ArtInt does nothing')
    
    # PARAM IN: stock_vol for detecting of Endspiel
    def getAvailableCards(self, stock_vol, rival_vol):
        indxs = []
        if canCardBeThrown(self.status, self.table, rival_vol):
            for i in range(self.vol()):
                card = self._showCard(i)
                move_correct = (isChoiceCorrect(self.status, 
                                                self.table, 
                                                card, 
                                                self.trump))
                if move_correct:
                    indxs.append(i)
        return indxs
    
    def getWeightOfSet(self, cards):        
        sw = 0
        for c in cards:
            sw += self.get_weight(c)
        return sw
    
    def getMeanWeight(self, cards = []):  
        mw = 0
        if cards == []:
            cards = self._cards
        sw = self.getWeightOfSet(self, cards)
        vol = len(cards)
        if vol > 0:
            mw = sw/vol
        return mw


class Nikita_A(ArtInt): 
    def makeDecision(self, indxs, stock_vol, rival):
        if len(indxs) > 0:
            return True            
        else:
            return False
        
    def getCardIndx(self, indxs, stock_vol, rival):
        return indxs[0]
        
       
class Alexander_P(ArtInt):
    def makeDecision(self, indxs, stock_vol, rival):
        if len(indxs) > 0:
            if self.status == Status.DEFENDING:
                w = self.get_weight(self._showCard(indxs[0]))
                if w <= Rank.TEN.value:
                    return True
            else:
                return True
        return False
    
    def getCardIndx(self, indxs, stock_vol, rival):
        return indxs[0]


class George_P(ArtInt):
    def makeDecision(self, indxs, stock_vol, rival): 
        if len(indxs) > 0:
            if (self.status == Status.ATTACKER and self.table.vol() > 0 or
                self.status == Status.ADDING):
                w = self.get_weight(self._showCard(indxs[0]))
                if w <= Rank.TEN.value:
                    return True
            else:
                return True   
        return False
        
    def getCardIndx(self, indxs, stock_vol, rival):
        return indxs[0]


class Gregory_P(ArtInt):
    def makeDecision(self, indxs, stock_vol, rival): 
        if len(indxs) > 0:
            # if it is not 1st move in party and
            # it is not endspiel yet then 
            # I am weighting card
            if self.table.vol() > 0 and stock_vol > 0:
                w = self.get_weight(self._showCard(indxs[0]))
                if w <= Rank.ACE.value:#Rank.TEN.value:
                    return True
            else:
                return True   
        return False
     
    def getCardIndx(self, indxs,  stock_vol, rival):
        return indxs[0]

class Sergey_C(ArtInt):
    def makeDecision(self, indxs, stock_vol, rival): 
        if len(indxs) > 0:
            return True
        else:
            return False
        
    # if no cards on table I throw least by weight card,
    # else I throw greatest one 
    def getCardIndx(self, indxs, stock_vol, rival):
        if self.table.vol() > 0 and not self.status == Status.DEFENDING:
            return indxs[-1]
        return indxs[0]


AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C, Gregory_P]
def AIGenerator(ai_name):
    for ai_c in AI_list:
        ai_o = ai_c()
        if ai_name == ai_o.name:
            return ai_o
