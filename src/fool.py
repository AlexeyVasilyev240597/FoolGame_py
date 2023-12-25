# from copy import deepcopy

from src.core.elems  import Deck, Stock, Table
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
                                deck)
    
    def updatePlayersContexts(self):
        for id in range(2):
            context_u = self.context.getPartialCopy(id)
            self.pls.getPlayerById(id).updateContext(context_u)
            
        
    def processingRoundResult(self, result):
        if result[0] == ResultOfRaund.FOOL_EXISTS:
            fool_id = result[1]
            self.pl_sbj.setFoolStatus(fool_id)
            self.updatePlayersContexts()
        else:
            print(result[0].name)
        self.pl_sbj.print_score()
    
    
    def playGameRound(self, prev_res: dict) -> dict:
        self.context.deck.shuffle()
        
        print('\n\n')
        print('-----------start of round-----------')
        
        deal(self.context)
        setOrderOfMoving(self.context, prev_res)
        actv_id = self.context.players.getIdByRole('actv')
        context_p = self.pla.getPartialCopy(actv_id)
        
        self.updatePlayersContexts()
        
        game_stage = GameStage.PLAYING
        while game_stage == GameStage.PLAYING:

            actv_id = self.context.players.getIdByRole('actv')
            context_p = self.context.getPartialCopy(actv_id)
            
            while (wrong_move := isMoveCorrect(
                    (move := self.pl_sbj.ask2move(context_p, actv_id)), 
                    context_p)):
                print(wrong_move)
                        
            react2Move(move, self.context)
            game_stage = gameIsOver(self.context)
            self.updatePlayersContexts()    
        
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
    

    
    
              