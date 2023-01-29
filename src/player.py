from abc  import ABC, abstractmethod
from enum import IntEnum

# from params import MAGIC_CONST, FLAG_DEBUG
from card    import Rank, Suit, Card
from elems   import Pile
from context import Context
from rules   import CARDS_KIT

class Status(IntEnum):
    ATTACKER  = 1
    DEFENDING = 2
    ADDING    = 3
    FOOL      = 4

class Word(IntEnum):
    BEATEN    = 1
    TAKE      = 2
    TAKE_AWAY = 3       


class Player(Pile):
    def __init__(self, name = 'John Doe'):
        # main params        
        self.name = name#str(Player.counter) + ': ' + name
        self.status = None
                
        # game params
        self.trump = None
        self.__get_weight = lambda card : ((card.suit == self.trump)*
                                         Rank.ACE.value +
                                         card.rank.value)
        self.losing_counter = 0
        
    def addCard(self, card):
        Pile.addCard(self, card)
        self.__cards.sort(key = self.__get_weight)
    
    # TODO: add decorators:
    #   - sort cards
    #   - if status is FOOL then get the first card
    @abstractmethod
    def getCard(self, context) -> Card:
        pass
        # indx = self.getCardIndex(context)
        # card = Pile.getCard(self, indx)
        # self.cards.sort(key = self.__get_weight)
        # return card
        
    def sayWord(self):
        if self.status == Status.ATTACKER:
            word = Word.BEATEN
            self.status = Status.DEFENDING
        if self.status == Status.DEFENDING:
            word = Word.TAKE
        if self.status == Status.ADDING:
            word = Word.TAKE_AWAY
            self.status = Status.ATTACKER
        return word
        
    def setNewGameParams(self, trump, status):
        self.trump  = trump        
        self.status = status
        self.__cards.sort(key = self.__get_weight)
    
    def move(self, context: Context):
        move = {}
        card = self.getCard(context)
        if card is None:
            word = self.sayWord()
            move = {'word': word}
        else:
            move = {'card': card}
        return move


# structure for working with two players
class Players(ABC):
    def __init__(self, pl_1: Player, pl_2: Player) -> None:
        self._players = [pl_1, pl_2]
        self._refs = {'actv': 0,
                      'pssv': 1}
        self.score = [0, 0]
        self.fool_id = -1

    @property
    def actv(self):
        return self._players[self._refs['actv']]
    
    @property
    def pssv(self):
        return self._players[self._refs['pssv']]

    def swapRoles(self):
        self._refs['actv'], self._refs['pssv'] = self._refs['pssv'], self._refs['actv']
    
    def getPlayerById(self, id: int) -> Player:
        if id == 0 or id == 1:
            return self._players[id]
        else:
            return None
    
    def getIdByRole(self, role: str):
        if role == 'actv' or role == 'pssv':
            return self._players[self._refs[role]]
        else:
            return None
    
    # if stock doesn't have enough cards then everyone will get equal amount
    def howManyToComplete(self, stock_vol: int):
        # players volume
        actv_vol = self.actv.vol
        pssv_vol = self.pssv.vol
        # need to add
        actv_add = 0
        pssv_add = 0
        while stock_vol > 0 and (actv_vol < CARDS_KIT or pssv_vol < CARDS_KIT):
            if actv_vol < pssv_vol:
                actv_add += 1
                actv_vol += 1
            else:
                pssv_add += 1
                pssv_vol += 1
            stock_vol -= 1
        return actv_add, pssv_add

    # now in first game first move is given to first player (by order),
    #     if dead heat then to player which throws last card 
    #     and to winner otherwise
    def setNewGameParams(self, trump: Suit, fool_id):
        if self._refs['actv'] == fool_id or fool_id == -1:
            self.swapRoles()
        self.actv.setNewGameParams(trump, Status.ATTACKER)
        self.pssv.setNewGameParams(trump, Status.DEFENDING)
    
    def setFoolStatus(self, fool_id:int):
        self.fool_id = fool_id
        if fool_id == 0 or fool_id == 1:
            self.getPlayerById(fool_id).status = Status.FOOL
            self.score[fool_id] += 1


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
