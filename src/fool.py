from copy import deepcopy

from src.core.elems  import Deck, Stock, Table
from src.core.player import Player, Players
from src.controller.player_sbj import PlayersSbjs
from src.core.context import Context
from src.core.rules import (deal, whoIsFool, setOrderOfMoving, GameStage, isMoveCorrect,
                         react2Move, ResultOfRaund, collect, gameIsOver)
from src.view.game_view import GameView

class FoolGame:
    def __init__(self, deck: Deck, pl_sbj: PlayersSbjs, user_id) -> None:
        self.pl_sbj = pl_sbj
        # self.context = Context(Stock(), 
        #                        Table(), 
        #                        Players(Player(),
        #                                Player()), 
        #                        deck)
        self.user_id = user_id
        rival_id = int(not user_id)
        self.game_view = GameView(False,
                                  pl_sbj.getNameByID(rival_id),
                                  pl_sbj.getNameByID(user_id), 
                                  user_id,
                                  deck)


    # def update_field(self):
    #     context_u = self.context.getPartialCopy(self.user_id)
    #     self.pl_sbj.game_view.update(context_u)
        
    def processingRoundResult(self, result):
        if result[0] == ResultOfRaund.FOOL_EXISTS:
            fool_id = result[1]
            self.pl_sbj.setFoolStatus(fool_id)
            # self.update_field()
        else:
            print(result[0].name)
        self.pl_sbj.print_score()
    
    def playGameRound(self, prev_res: dict) -> dict:
        # self.context.deck.shuffle()
        # self.game_view.deck.syncDeck(deepcopy(self.context.deck))
        self.game_view.deck.shuffle()
        
        print('\n\n')
        print('-----------start of round-----------')
        
        # deal(self.context)
        # setOrderOfMoving(self.context, prev_res)
        
        deal(self.game_view)
        setOrderOfMoving(self.game_view, prev_res)
        self.game_view.update()
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:
            # actv_id = self.context.players.getIdByRole('actv')
            # context_p = self.context.getPartialCopy(actv_id)

            actv_id = self.game_view.players.getIdByRole('actv')
            context_p = self.game_view.getPartialCopy(actv_id)
            
            while (wrong_move := isMoveCorrect(
                    (move := self.pl_sbj.ask2move(context_p, actv_id)), 
                    context_p)):
                print(wrong_move)
            
            # react2Move(move, self.context)
            # game_stage = gameIsOver(self.context)
            
            react2Move(move, self.game_view)
            game_stage = gameIsOver(self.game_view)
            self.game_view.update()
            # print('------------------------------------')
            
        # result = whoIsFool(self.context)
        # self.processingRoundResult(result)
        # collect(self.context)
        
        result = whoIsFool(self.game_view)
        self.processingRoundResult(result)
        collect(self.game_view)
        
        print('------------end of round------------')
        print('\n\n')
        print('\n\n')
        
        return result

    def playGameSeries(self, num_of_wins: int):
        result = [ResultOfRaund.NEW_GAME]
        while max(self.pl_sbj.score) < num_of_wins:
            result = self.playGameRound(result)
    

    
    
              