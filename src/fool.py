from elems  import Deck, Stock, Table
from player import Player, Players
from context import Context
# from ai     import AIGenerator
from rules import *

class FoolGame:
    def __init__(self, pl_1_name:str, pl_2_name: str) -> None:
        players = Players(Player(pl_1_name), Player(pl_2_name))
        self.context = Context(Stock(), Table(), players, Deck())

    def playGameRound(self):

        game_stage = GameStage.START
        deal(self.context)
        
        game_stage = GameStage.PLAYING      
        while game_stage == GameStage.PLAYING:
            # TODO: 
            # notify player that his/her move is wrong (instead 'pass');
            # and break loop after several (3-6) trying
            while not isMoveCorrect(move := 
                                    self.context.players.actv.move(self.context)):
                pass        
            game_stage = reactToMove(move, self.context)
        collect(self.context)
        
        whoIsFool(self.context)

    def playGameSeries(self, num_of_wins: int):
        while max(self.context.players.score) < num_of_wins:
            self.playGameRound()