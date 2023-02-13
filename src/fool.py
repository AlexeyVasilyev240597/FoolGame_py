from .core.elems  import Deck, Stock, Table
from .core.player import Player, Players
from .subjects.player_sbj import PlayersSbjs
from .core.context import Context
from .core.rules import (GameStage, deal, collect, isMoveCorrect,
                   whoIsFool, reactToMove, MoveType)
from .subjects.display_console import display_field

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
        if last_move:
            self.pl_sbj.last_move = last_move
        context_u = self.context.getPartialCopy(self.user_id)
        display_field(context_u, self.pl_sbj.last_move)

    def playGameRound(self):
        print('-----------start of round-----------')
        deal(self.context)
        
        self.update_field(None)
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            print('------------------------------------')
            actv_id = self.context.players.getIdByRole('actv')

            context_p = self.context.getPartialCopy(actv_id)
            
            while (wrong_move := isMoveCorrect(
                    (move := self.pl_sbj.ask2move(context_p, actv_id)), 
                    context_p)):
                print(wrong_move)
            
            game_stage = reactToMove(move, self.context)
            self.update_field(move)
            print('------------------------------------')
            
        fool_id = whoIsFool(self.context.players)
        say = self.pl_sbj.setFoolStatus(fool_id)
        self.update_field(say)
        
        collect(self.context)
        print('------------end of round------------')

    def playGameSeries(self, num_of_wins: int):
        while max(self.pl_sbj.score) < num_of_wins:
            self.playGameRound()
    

    
    
              