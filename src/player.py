from src.core.card              import Card
from src.core.elems             import Pile
from src.core.players_hand      import Word, PlayersHand, PlayersHands
from src.core.context           import Context
from src.core.rules             import GameStage, deal, setOrderOfMoving, react2Move, ResultOfRaund, whoIsFool, collect
from src.controller.player_sbj  import PlayerSbj, PlayersSbjs
from src.view.elems_view        import DeckView
from src.view.game_view         import GameView


class Player:
    def __init__(self, pl_sbj: PlayerSbj) -> None:
        self.name = pl_sbj.name
        self.hand = PlayersHand()
        # model: will set after a deal form partial copy of general context
        self.context = None
        # view and controller: will set after meetinf with a rival
        self.view = None
        self.sbj = pl_sbj
        
        
    def updateContext(self, new_context: Context, stage: GameStage) -> None:
        self.context = new_context
        
        rival_id = not self.sbj.id
        last_move = new_context.last_move
        
        if stage == GameStage.START:
            print('\n\n')
            print('-----------start of round-----------')
            
            deal(self.view, self.view.deck)
            # TODO: fix it! prevRes should be stored into Player
            self.openCardsInMyHand()
            self.view.stock.cards[0] =  self.view.stock.card2cardView(
                new_context.stock.last)
            self.view.stock.setTrump()
            setOrderOfMoving(self.view, [ResultOfRaund.NEW_GAME])
            self.view.players.getPlayerById(self.sbj.id).sortHand()
        elif stage == GameStage.PLAYING:
            if (last_move['pl_id'] == rival_id and
                'card' in last_move):
                        self._flipRivalCards(rival_id, last_move['card'])
            
            react2Move(last_move, self.view)

            # if last_move['pl_id'] == self.sbj.id:
            #     if 'word' in last_move and last_move['word'] == Word.TAKE_AWAY:
                    # self._flipRivalCards(rival_id)
                    # self.openCardsInMyHand()
            
            
            # if 'word' in last_move and (last_move['word'] == Word.BEATEN):
            self._flipRivalCards(rival_id)
            self.openCardsInMyHand()
        # TODO: process it!
        elif stage == GameStage.GAME_OVER:
            react2Move(last_move, self.view)
            self.view.update()
            
            result = whoIsFool(self.view)
            # TODO: replace those prints by words!
            if result[0] == ResultOfRaund.FOOL_EXISTS:
                if result[1] == self.sbj.id:
                    print('I am a Fool')
                else:
                    print('You are a Fool')
            else:
                print(result[0].name)
                    
            collect(self.view, self.view.deck)
            [card.hide() for card in self.view.deck.cards]
            
            print('------------end of round------------')
            print('\n\n')
            print('\n\n')
        
        self.view.update()

    def openCardsInMyHand(self):
        my_hand_v = self.view.players.getPlayerById(self.sbj.id)
        # find closed cards in self.hand, 
        old_hand_v = self.view.players.getPlayerById(self.sbj.id).cards
        closed_cards_ids = [i for i in range(len(old_hand_v)) if not old_hand_v[i].open]
        if not closed_cards_ids:
            return
    
        # find diff between self.hand and new_context.players.getById(self.sbj.id)
        known_cards = []
        for card_v in old_hand_v:
            if card_v.open:
                known_cards.append(card_v)
        
        new_hand = self.context.players.getPlayerById(self.sbj.id).cards
        unknown_cards = []
        for card in new_hand:
            if not card in known_cards:
                unknown_cards.append(card)
        
        # replace closed dummy cards by found in diff
        j = 0
        for i in closed_cards_ids:
            old_hand_v[i] = my_hand_v.card2cardView(unknown_cards[j])
            j += 1
        self.view.players.getPlayerById(self.sbj.id).sortHand()
    
    
    def _flipRivalCards(self, rival_id: int, card: Card = None):
        rival = self.view.players.getPlayerById(rival_id)
        rivals_hand = rival.cards
        if card and rivals_hand:
            rivals_hand[0] = rival.card2cardView(card)
        else:        
            rival.flipCards()
                
        

class Players(PlayersSbjs):
    def __init__(self, pl_1: Player, pl_2: Player, is_graphic: bool = False) -> None:
        self._players = [pl_1, pl_2]
        # TODO: make meeting with rival better
        for id, pl in zip(range(len(self._players)), self._players):
            pl.view = GameView(is_graphic, self._players[(not id)].name, pl.name, id)
        super().__init__(pl_1.sbj, pl_2.sbj)
        self._players = [pl_1, pl_2]
    
    def getPlayerById(self, id: int) -> Player:
        if id == 0 or id == 1:
            return self._players[id]
        else:
            return None

    