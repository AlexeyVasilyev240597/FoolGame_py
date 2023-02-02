from elems  import Deck, Stock, Table
from player import Player, Players
from context import Context
# from ai     import AIGenerator
from rules import GameStage, deal, isMoveCorrect, collect, whoIsFool, reactToMove
from display_console import display_field

class FoolGame:
    def __init__(self, pl_sbj) -> None:
        self.pl_sbj = pl_sbj
        players = Players(Player(pl_sbj[0].id, pl_sbj[0].name), 
                          Player(pl_sbj[1].id, pl_sbj[1].name))
        self.context = Context(Stock(), Table(), players, Deck())
        # TODO: replace line by setting this value by argument of __init__
        self.user_id = 0

    def update_field(self):
        context_u = self.context.getPartialCopy(self.user_id)
        display_field(context_u)

    def playGameRound(self):
        
        game_stage = GameStage.START
        deal(self.context)
        self.update_field()
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            actv_id = self.context.players.getIdByRole('actv')
            context_p = self.context.getPartialCopy(actv_id)
            # TODO: 
            # notify player that his/her move is wrong (instead 'pass');
            # and break loop after several (3-6) trying
            while not isMoveCorrect(move := 
                                    self.pl_sbj[actv_id].move(context_p), 
                                    context_p):
                pass        
            self.context.last_move['pl_id'] = actv_id
            self.context.last_move['move'] = move
            game_stage = reactToMove(move, self.context)
            self.update_field()
            
        say = whoIsFool(self.context.players)
        self.context.last_move = say
        self.update_field()
        
        collect(self.context)

    def playGameSeries(self, num_of_wins: int):
        while max(self.context.players.score) < num_of_wins:
            self.playGameRound()