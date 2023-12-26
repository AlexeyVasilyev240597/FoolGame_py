from abc import ABC
from copy import deepcopy

from src.core.elems  import Pile, Stock, Table
from src.core.players_hand import PlayersHand, PlayersHands

class Context(ABC):
    def __init__(self,
                 stock: Stock,
                 table: Table,
                 players: PlayersHands,
                 pile: Pile) -> None:
        self.stock   = stock
        self.table   = table
        self.players = players
        self.pile    = pile
        
        self.last_move = {}

    def getPartialCopy(self, player_viewer_id: int):
        new_context = deepcopy(self)
        # NOTE: valid for game with two players,
        #       if > 2 players:
        #           rivals_ids = list(range(NUM_OF_PLAYERS))
        #           rivals_ids.pop(player_viewer_id)
        rival_id = int(not player_viewer_id)
        new_context.stock.hideCards()
        new_context.players.getPlayerById(rival_id).hideCards()
        new_context.pile.hideCards()
        return new_context
