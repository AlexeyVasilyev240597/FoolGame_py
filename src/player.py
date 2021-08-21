from enum import IntEnum

from params import MAGIC_CONST, FLAG_DEBUG
from items  import Rank
from elems  import Pile


class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3       

class PlayerAsRival:
    def __init__(self, name, vol, status, last_move):
        self.name      = name
        self.vol       = vol
        self.status    = status
        self.last_move = last_move

class Player(Pile):
    # counter of players
    counter = 0
    def __init__(self, name, is_user = True):
        Player.counter += 1
        
        Pile.__init__(self)
        
        # main params        
        self.name = name#str(Player.counter) + ': ' + name
        self.status = []
        self.is_user = is_user
                
        # game params
        self.trump = []
        self.table = []
        self.get_weight = lambda card : ((card.suit == self.trump)*
                                         Rank.ACE.value +
                                         card.rank.value)
        self.losing_counter = 0
        self.last_move = {}
        
    def addCard(self, card):
        Pile.addCard(self, card)
        self.cards.sort(key = self.get_weight)
        
    def getCard(self, indx = 0):
        flip_flag = not (FLAG_DEBUG ^ (self.status == Status.FOOL))
        card = Pile.getCard(self, flip_flag, indx)
        self.cards.sort(key = self.get_weight)
        self.last_move = {'card': card}
        return card
        
    def showCard(self, indx):
        pass
    
    def _showCard(self, indx):
        return self.cards[indx]
        
    def sayWord(self):
        if self.status == Status.ATTACKER:
            word = Word.BEATEN
        if self.status == Status.DEFENDING:
            word = Word.TAKE
        if self.status == Status.ADDING:
            word = Word.TAKE_AWAY
        self.last_move = {'word': word}
        return word
        
    def setNewGameParams(self, trump, table, status):
        self.trump  = trump        
        self.table  = table
        self.status = status
        self.cards.sort(key = self.get_weight)
    
    def iAmFool(self):
        self.status = Status.FOOL
        self.losing_counter += 1
        
    def getMeAsRival(self):
        return PlayerAsRival(self.name, 
                             self.vol(), 
                             self.status, 
                             self.last_move)
        
# class PlayersFaceToFace:
#     def __init__(self, pl_1, pl_2):
#         self.plrs = [pl_1, pl_2]
#         self.actv = pl_1
#         self.pssv = pl_2

#     def swapRole(self):
#         self.actv, self.pssv = self.pssv, self.actv

#     # now first move is given
#     #   to first by order player in first game,
#     #   to winner if he is,
#     #   to player which throws last card if dead heat
#     def setStatusInNewGame(self):
#         self.actv.status = Status.ATTACKER
#         self.pssv.status = Status.DEFENDING

#     def getNumToAdd(self, stock_vol):
#         pv = {'actv': self.actv.vol(), 'pssv': self.pssv.vol()}
#         dv = {'actv': 0, 'pssv': 0}
#         s  = stock_vol
#         while (s > 0 and (pv['actv'] < MAGIC_CONST or
#                           pv['pssv'] < MAGIC_CONST)):
#             if pv['actv'] < pv['pssv']:
#                 dv['actv'] += 1
#                 pv['actv'] += 1
#             else:
#                 dv['pssv'] += 1
#                 pv['pssv'] += 1
#             s -= 1
#         return dv

# #    def changeStatus(self):
# #        ...

# # TODO: class for playing with 3 players
# #class PlayersThreesome
