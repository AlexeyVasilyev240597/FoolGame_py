from abc import ABC
from copy import copy

from elems  import Deck, Stock, Table
from player import Player, Players

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

    def getPartialCopy(self, player_viewer_id: int):
        new_context = copy(self)
        # NOTE: valid for game with two players,
        #       if > 2 players:
        #           rivals_ids = list(range(NUM_OF_PLAYERS))
        #           rivals_ids.pop(player_viewer_id)
        rival_id = int(not player_viewer_id)
        new_context.stock.hideCards()
        new_context.players.getPlayerById(rival_id).hideCards()
        new_context.deck.hideCards()
        return new_context
