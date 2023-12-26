# from copy import deepcopy

from src.core.elems  import Pile, Deck, Stock, Table
from src.core.players_hand import PlayersHand, PlayersHands
# from src.controller.player_sbj import PlayersSbjs
from src.core.context import Context
from src.core.rules import (deal, whoIsFool, setOrderOfMoving, GameStage, isMoveCorrect,
                         react2Move, ResultOfRaund, collect, gameIsOver)
from src.player import Players
# from src.view.game_view import GameView

class FoolGame:
    def __init__(self, deck: Deck, pls: Players) -> None:
        self.pls = pls
        self.context = Context(Stock(), 
                                Table(), 
                                PlayersHands(PlayersHand(), PlayersHand()), 
                                Pile())
        self.deck = deck
    
        
    def updatePlayersContexts(self, game_stage):
        # for id in range(2):
        # ASSUMPTION: User has id == 0
        id = 0
        context_u = self.context.getPartialCopy(id)
        self.pls.getPlayerById(id).updateContext(context_u, game_stage)
            
        
    def processingRoundResult(self, result):
        if result[0] == ResultOfRaund.FOOL_EXISTS:
            fool_id = result[1]
            self.pls.setFoolStatus(fool_id)
            self.updatePlayersContexts(GameStage.GAME_OVER)
        else:
            print(result[0].name)
        self.pls.print_score()
    
    
    def playGameRound(self, prev_res: dict) -> dict:
        self.deck.shuffle()
        
        print('\n\n')
        print('-----------start of round-----------')
        
        deal(self.context, self.deck)
        setOrderOfMoving(self.context, prev_res)
        self.updatePlayersContexts(GameStage.START)
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:

            actv_id = self.context.players.getIdByRole('actv')
            context_p = self.context.getPartialCopy(actv_id)
            
            while (wrong_move := isMoveCorrect(
                    (move := self.pls.ask2move(context_p, actv_id)), 
                    context_p)):
                print(wrong_move)
                        
            react2Move(move, self.context)
            game_stage = gameIsOver(self.context)
            self.updatePlayersContexts(game_stage)    
        
        result = whoIsFool(self.context)
        self.processingRoundResult(result)
        collect(self.context, self.deck)
        
        print('------------end of round------------')
        print('\n\n')
        print('\n\n')
        
        return result

    def playGameSeries(self, num_of_wins: int):
        result = [ResultOfRaund.NEW_GAME]
        while max(self.pls.score) < num_of_wins:
            result = self.playGameRound(result)
    

    
    
              