from src.core.card              import Card
from src.core.players_hand      import Word, PlayersHand, PlayersHands
from src.core.context           import Context
from src.core.rules             import react2Move
from src.controller.player_sbj  import PlayerSbj, PlayersSbjs
from src.view.game_view         import GameView


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = PlayersHand()
        # TODO: set after a deal form partial copy of general context
        self.context = None
        
    def updateContext(self, new_context: Context):
        self.context = new_context
        
        rival_id = not self.sbj.id
        last_move = new_context.last_move
      
        if last_move['pl_id'] == rival_id:
            if 'card' in last_move:
                self._flipRivalCards(rival_id, last_move['card'])
        elif last_move['pl_id'] == self.sbj.id:
            if 'word' in last_move and last_move['word'] == Word.TAKE_AWAY:
                self._flipRivalCards(rival_id)
        else:
            print('ERROR: pl_id is not in last_move')
        
        react2Move(last_move, self.view)
        
        #  TODO:
        #   find closed cards in self.hand, 
        #   find diff between self.hand and new_context.players.getById(self.sbj.id)
        #   replace closed dummy cards by found in diff
        if 'word' in last_move and last_move['word'] == Word.BEATEN:
            return
        
            
            
            
    def _flipRivalCards(self, rival_id: int, card: Card = None):
        rivals_hand = self.view.players.getPlayerById(rival_id)
        if card and rivals_hand:
            rivals_hand[0] = card
        else:        
            self.rival_id.flipCards()
                
        

class Players:
    def __init__(self, pl_1: Player, pl_2: Player) -> None:
        self._players = [pl_1, pl_2]
        # TODO: make meeting with rival better
        for id, pl in zip(range(len(self._players)), self._players):
            pl.sbj = PlayerSbj(pl.name, id)
            pl.view = GameView(False, self._players[(not id)], pl.name, id)
        
        # self._players = PlayersSbj()
    