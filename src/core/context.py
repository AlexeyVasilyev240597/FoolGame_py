from abc import ABC
from copy import deepcopy

from src.core.elems  import Deck, Stock, Table
from src.core.player import Players

class Context(ABC):
    def __init__(self,
                 stock: Stock,
                 table: Table,
                 players: Players,
                 deck: Deck) -> None:
        self.stock   = stock
        self.table   = table
        self.players = players
        self.deck    = deck
        
        self.last_move = {}

    def getPartialCopy(self, player_viewer_id: int):
        new_context = deepcopy(self)
        # NOTE: valid for game with two players,
        #       if > 2 players:
        #           rivals_ids = list(range(NUM_OF_PLAYERS))
        #           rivals_ids.pop(player_viewer_id)
        rival_id = int(not player_viewer_id)
        # new_context.stock.hideCards()
        new_context.players.getPlayerById(rival_id).hidCards()
        # new_context.deck.hideCards()
        return new_context
