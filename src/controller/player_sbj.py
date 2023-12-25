from abc import ABC, abstractmethod

from src.core.card import Card
from src.core.players_hand import Status, Word
from src.core.context import Context
# from src.view.game_view import GameView


class PlayerSbj(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = None
    
    def move(self, context: Context):
        move = {}
        if self.id == context.players.getIdByRole('actv'):
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
        # elif status == Status.FOOL:
        #     word = Word.LOST
        return word
        

    @abstractmethod
    def chooseCard(self, context: Context) -> Card:
        pass

class PlayersSbjs(ABC):
    # TODO: get two pairs of arguments: (Player's name, is human) 
    #       and call fabric, pass to it just id of each player
    def __init__(self, pl_1: PlayerSbj, pl_2: PlayerSbj) -> None:
        self._players = [pl_1, pl_2]
        pl_1.id = 0;
        pl_2.id = 1
        self.score = [0, 0]
        if pl_1.name == pl_2.name:
            pl_1.name += '#1'
            pl_2.name += '#2'


    def ask2move(self, context: Context, pl_id: int) -> dict:
        move = self._players[pl_id].move(context)
        move['pl_id'] = pl_id
        return move
        
    
    def getNameByID(self, id: int) -> str:
        if id == 0 or id == 1:
            return self._players[id].name
        else:
            print("WARNING: wrong player id")
            return None
    
    
    # TODO: need to test DEAD HEAT
    def setFoolStatus(self, fool_id: int) -> None:
        if fool_id == 0 or fool_id == 1:
            self.score[fool_id] += 1
            fool = self._players[fool_id]
            # say = {}
            # say['word'] = fool.sayWord(Status.FOOL)
            # say['pl_id'] = fool_id
            print(f'{fool.name} is a Fool')
        # return say
    
    def print_score(self):
        for i in range(2):
            print(f'score:{self._players[i].name} is a Fool '\
                  f'{self.score[i]} times')
