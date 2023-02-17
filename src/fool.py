from .core.elems  import Deck, Stock, Table
from .core.player import Player, Players
from .subjects.player_sbj import PlayersSbjs
from .core.context import Context
from .core.rules import (deal, whoIsFool, whoseFirstMove, GameStage, isMoveCorrect,
                         react2Move, ResultOfRaund, collect)
from .view.console.display_console import display_field

class FoolGame:
    def __init__(self, deck: Deck, pl_sbj: PlayersSbjs, user_id) -> None:
        self.pl_sbj = pl_sbj
        self.context = Context(Stock(), 
                               Table(), 
                               Players(Player(),
                                       Player()), 
                               deck)
        self.user_id = user_id

    def setOrderOfMoving(self, prev_res) -> None:
        pl_1st = whoseFirstMove(prev_res)
        self.context.players.setNewGameParams(self.context.stock.trump, pl_1st)

    def update_field(self, last_move = None):
        if last_move:
            self.pl_sbj.last_move = last_move
        context_u = self.context.getPartialCopy(self.user_id)
        display_field(context_u, self.pl_sbj.last_move, self.user_id)
        
    def processingRoundResult(self, result):
        if result[0] == ResultOfRaund.FOOL_EXISTS:
            fool_id = result[1]
            self.context.players.setFoolStatus(fool_id)
            self.pl_sbj.setFoolStatus(fool_id)
            self.update_field()
        else:
            print(result[0].name)
        self.pl_sbj.print_score()
    
    def playGameRound(self, prev_res: dict) -> dict:
        print('\n\n')
        print('-----------start of round-----------')
        
        deal(self.context)
        self.setOrderOfMoving(prev_res)
        self.update_field()
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            print('------------------------------------')
            actv_id = self.context.players.getIdByRole('actv')

            context_p = self.context.getPartialCopy(actv_id)
            
            while (wrong_move := isMoveCorrect(
                    (move := self.pl_sbj.ask2move(context_p, actv_id)), 
                    context_p)):
                print(wrong_move)
            
            game_stage = react2Move(move, self.context)
            self.update_field(move)
            print('------------------------------------')
            
        result = whoIsFool(self.context)
        self.processingRoundResult(result)
        collect(self.context)
        
        print('------------end of round------------')
        print('\n\n')
        print('\n\n')
        
        return result

    def playGameSeries(self, num_of_wins: int):
        result = [ResultOfRaund.NEW_GAME]
        while max(self.pl_sbj.score) < num_of_wins:
            result = self.playGameRound(result)
    

    
    
              