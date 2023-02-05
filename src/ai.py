from abc import abstractmethod

from card  import Rank, Card
from player import Status
from player_sbj import PlayerSbj
from context import Context
from rules  import doesCardFit, canCardBeThrown, MoveType

# Artificial Intelligence 
class ArtInt(PlayerSbj):
    def __init__(self):
        name = str(self.__class__.__name__)
        super().__init__(name)
    
    def getFitCards(self, context: Context):
        fit_cards = []
        for card in context.players.actv.cards:
            if (doesCardFit(card, context) == MoveType.CORRECT_MOVE and 
                canCardBeThrown(context) == MoveType.CORRECT_MOVE):
                fit_cards.append(card)
        return fit_cards
    
    @abstractmethod
    def chooseCard(self, context: Context) -> Card:
        pass
    
    
    
    # def getWeightOfSet(self, cards):        
    #     sw = 0
    #     for c in cards:
    #         sw += self.__get_weight(c)
    #     return sw
    
    # def getMeanWeight(self, cards = []):  
    #     mw = 0
    #     if cards == []:
    #         cards = self.cards
    #     sw = self.getWeightOfSet(self, cards)
    #     vol = len(cards)
    #     if vol > 0:
    #         mw = sw/vol
    #     return mw

class Nikita_A(ArtInt): 
    def chooseCard(self, context: Context) -> Card:
        fit_cards = self.getFitCards(context)
        if fit_cards:
            return fit_cards[0]
        else:
            return None

class Sergey_C(ArtInt):
    # if no cards on table I throw least by weight card,
    # else I throw greatest one 
    def chooseCard(self, context: Context) -> Card:
        fit_cards = self.getFitCards(context)
        if fit_cards:
            if (context.table.vol > 0 and 
                not context.players.actv.status == Status.DEFENDING):
                return fit_cards[-1]
            return fit_cards[0]
        else:
            return None
       
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
    
    def chooseCard(self, indxs, stock_vol, rival):
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
        
    def chooseCard(self, indxs, stock_vol, rival):
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
     
    def chooseCard(self, indxs,  stock_vol, rival):
        return indxs[0]

# class Sergey_C(ArtInt):
#     def makeDecision(self, indxs, stock_vol, rival): 
#         if len(indxs) > 0:
#             return True
#         else:
#             return False
        
#     # if no cards on table I throw least by weight card,
#     # else I throw greatest one 
#     def getCardIndx(self, indxs, stock_vol, rival):
#         if self.table.vol() > 0 and not self.status == Status.DEFENDING:
#             return indxs[-1]
#         return indxs[0]


AI_list = [Nikita_A, Alexander_P, George_P, Sergey_C, Gregory_P]
def AIGenerator(ai_name):
    for ai_c in AI_list:
        ai_o = ai_c()
        if ai_name == ai_o.name:
            return ai_o
    else:
        print(f'WARNING: no such AI with name {ai_name}')
        return None
