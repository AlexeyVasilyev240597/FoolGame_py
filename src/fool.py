from elems  import Deck, Stock, Table
from player import Player, Players
from context import Context
# from ai     import AIGenerator
from rules import GameStage, deal, isMoveCorrect, collect, whoIsFool, reactToMove

class FoolGame:
    def __init__(self, pl_1: Player, pl_2: Player) -> None:
        players = Players(pl_1, pl_2)
        self.context = Context(Stock(), Table(), players, Deck())

    def playGameRound(self):

        game_stage = GameStage.START
        deal(self.context)
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            context_p = self.context.getPartialCopy(self.context.players.getIdByRole('actv'))
            # TODO: 
            # notify player that his/her move is wrong (instead 'pass');
            # and break loop after several (3-6) trying
            while not isMoveCorrect(move := 
                                    self.context.players.actv.move(context_p), 
                                    self.context):
                pass        
            game_stage = reactToMove(move, self.context)
        collect(self.context)
        
        whoIsFool(self.context)

    def playGameSeries(self, num_of_wins: int):
        while max(self.context.players.score) < num_of_wins:
            self.playGameRound()