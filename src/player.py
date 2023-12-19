from src.core.players_hand            import PlayersHand, PlayersHands
from src.core.context           import Context
from src.controller.player_sbj  import PlayerSbj, PlayersSbjs
from src.view.game_view         import GameView

class Player:
    def __init__(self, name: str, id: int) -> None:
        self.hand = PlayersHand()
        # TODO: set after a deal form partial copy of general context
        # self.context = Context(stock, table, players, deck)
        self.sbj  = PlayerSbj(name, id)
        # TODO: set after meeting with rival (in Players constructor)
        # self.view = GameView(False, rival_name, name, id)
        