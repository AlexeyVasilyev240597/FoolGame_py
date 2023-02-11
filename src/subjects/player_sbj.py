from abc import ABC, abstractmethod

from src.core.card import Card
from src.core.player import Status, Word
from src.core.context import Context


class PlayerSbj(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
    
    def move(self, context: Context):
        my_id = context.players.getIdByRole('actv')
        move = {'pl_id': my_id}
        card = self.chooseCard(context)
        if card:
            move['card'] = card
        else:
            word = self.sayWord(context.players.actv.status)
            move['word'] = word
        
        return move

    def sayWord(self, status: Status):
        if status == Status.ATTACKER:
            word = Word.BEATEN
        elif status == Status.DEFENDING:
            word = Word.TAKE
        elif status == Status.ADDING:
            word = Word.TAKE_AWAY
        elif status == Status.FOOL:
            word = Word.LOST
        return word
        

    @abstractmethod
    def chooseCard(self, context: Context) -> Card:
        pass

class PlayersSbjs(ABC):
    def __init__(self, pl_1: PlayerSbj, pl_2: PlayerSbj) -> None:
        self._players = [pl_1, pl_2]
        self._actv_id = 0
        self.last_move = {'pl_id': None, 'move': None}
        self.score = [0, 0]
        if pl_1.name == pl_2.name:
            name = pl_1.name
            pl_1.name = name + '#1'
            pl_2.name = name + '#2'

    @property
    def actv(self):
        return self._players[self._actv_id]
    
    def setActvID(self, a_id: int) -> None:
        self._actv_id = a_id
    
    def getNameByID(self, id: int) -> str:
        if id == 0 or id == 1:
            return self._players[id].name
        else:
            print("WARNING: wrong player id")
            return None
    
    
    def setFoolStatus(self, fool_id: int) -> Word:
        if fool_id == 0 or fool_id == 1:
            self.score[fool_id] += 1
            fool = self._players[fool_id]
            say = {'pl_id': fool_id, 
                   'move': {'word': fool.sayWord(Status.FOOL)}}
            return say
