# from src.view.context_view import GameView


from src.core.elems import Deck, Stock, Table
from src.core.players_hand import PlayersHand, PlayersHands
from src.core.context import Context
from src.controller.bot.ai import Sergey_C
from src.controller.human.console.human_console import HumanConsole
# from src.controller.player_sbj import PlayersSbjs
from src.core.rules import deal
from src.view.game_view import GameView

deck = Deck()
context = Context(Stock(), 
                  Table(), 
                  PlayersHands(PlayersHand(),
                          PlayersHand()),
                  deck)

pl_1 = HumanConsole(0)
pl_2 = Sergey_C(1)

game_view = GameView(False, pl_2.name, pl_1.name, 0, True)

deal(context)
context_p = context.getPartialCopy(0)

game_view.update(context_p)



