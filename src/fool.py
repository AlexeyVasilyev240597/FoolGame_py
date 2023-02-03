from elems  import Deck, Stock, Table
from player import Player, Players, PlayersSbjs
from context import Context
# from ai     import AIGenerator
from rules import GameStage, deal, isMoveCorrect, collect, whoIsFool, reactToMove
from display_console import display_field

class FoolGame:
    def __init__(self, pl_sbj: PlayersSbjs) -> None:
        self.pl_sbj = pl_sbj
        self.context = Context(Stock(), 
                               Table(), 
                               Players(Player(pl_sbj.getNameByID(0)),
                                       Player(pl_sbj.getNameByID(1))), 
                               Deck())
        # TODO: replace line by setting this value by argument of __init__
        self.user_id = 0

    def update_field(self, last_move):
        self.context.last_move = last_move
        self.pl_sbj.setActvID(self.context.players.getIdByRole('actv'))
        context_u = self.context.getPartialCopy(self.user_id)
        display_field(context_u)

    def playGameRound(self):
        deal(self.context)
        
        last_move = {'pl_id': None, 'move': None}
        self.update_field(last_move)
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            actv_id = self.context.players.getIdByRole('actv')
            context_p = self.context.getPartialCopy(actv_id)
            # TODO: 
            # notify player that his/her move is wrong (instead 'pass');
            # and break loop after several (3-6) trying
            while not isMoveCorrect(move := 
                                    self.pl_sbj.actv.move(context_p), 
                                    context_p):
                pass        
            last_move['pl_id'] = actv_id
            game_stage = reactToMove(move, self.context)
            last_move['move'] = move
            self.update_field(last_move)
            
        say = whoIsFool(self.context.players)
        self.update_field(say)
        
        collect(self.context)

    def playGameSeries(self, num_of_wins: int):
        while max(self.context.players.score) < num_of_wins:
            self.playGameRound()