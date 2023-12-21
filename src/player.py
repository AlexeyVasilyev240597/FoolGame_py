from src.core.card              import Card
from src.core.players_hand      import Word, PlayersHand, PlayersHands
from src.core.context           import Context
from src.core.rules             import react2Move
from src.controller.player_sbj  import PlayerSbj, PlayersSbjs
from src.view.game_view         import GameView
from src.view.card_convert      import CardConverter


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = PlayersHand()
        # TODO: set after a deal form partial copy of general context
        self.context = None
        
    def updateContext(self, new_context: Context):
        self.context = new_context
        
        rival_id = not self.sbj.id
        last_move = new_context.last_move
      
        if last_move['pl_id'] == rival_id:
            if 'card' in last_move:
                self._flipRivalCards(rival_id, last_move['card'])
        elif last_move['pl_id'] == self.sbj.id:
            if 'word' in last_move and last_move['word'] == Word.TAKE_AWAY:
                self._flipRivalCards(rival_id)
        else:
            print('ERROR: pl_id is not in last_move')
        
        react2Move(last_move, self.view)
        
        
        if 'word' in last_move and last_move['word'] == Word.BEATEN:
            # find closed cards in self.hand, 
            old_hand_v = self.view.players.getPlayerById(self.sbj.id).cards
            closed_cards_ids = [i for i in range(len(old_hand_v)) if not old_hand_v[i].open]
            if not closed_cards_ids:
                return
 
            # find diff between self.hand and new_context.players.getById(self.sbj.id)
            known_cards = []
            for card_v in old_hand_v:
                if card_v.open:
                    # ASSUMPTION: is_graphic = False
                    known_cards.append(CardConverter.cardView2card(card_v, False))
            
            new_hand = new_context.players.getPlayerById(self.sbj.id).cards
            unknown_cards = []
            for card in new_hand:
                if not card in known_cards:
                    unknown_cards.append(card)
            
            # replace closed dummy cards by found in diff
            j = 0
            for i in closed_cards_ids:
                # ASSUMPTION: is_graphic = False
                old_hand_v[i] = CardConverter.card2cardView(unknown_cards[j], False)
                j += 1
        
        self.view.update()
            
            
    def _flipRivalCards(self, rival_id: int, card: Card = None):
        rivals_hand = self.view.players.getPlayerById(rival_id).cards
        if card and rivals_hand:
            rivals_hand[0] = card
        else:        
            self.rival_id.flipCards()
                
        

class Players:
    def __init__(self, pl_1: Player, pl_2: Player) -> None:
        self._players = [pl_1, pl_2]
        # TODO: make meeting with rival better
        for id, pl in zip(range(len(self._players)), self._players):
            pl.sbj = PlayerSbj(pl.name, id)
            # ASSUMPTION: is_graphic = False
            pl.view = GameView(False, self._players[(not id)], pl.name, id)
        
        # self._players = PlayersSbj()
    