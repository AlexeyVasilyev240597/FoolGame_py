# from abc import ABC, abstractmethod

from src.core.elems import Deck
from src.core.players_hand import PlayersHands
from src.core.context import Context
# from .elems_view import syncPile # DeckView, StockView, TableView
# from .player_view import PlayerView

from src.view.elem_view_fabric import ElemViewFabric

class GameView(Context):
    def __init__(self, 
                 is_graphic: bool,
                 rival_name: str,
                 my_name: str, 
                 my_id: int,
                 ) -> None:       
        Context.__init__(self,
                        ElemViewFabric.getStockView(is_graphic),
                        ElemViewFabric.getTableView(is_graphic),
                        PlayersHands(ElemViewFabric.getPlayerView(is_graphic),
                                     ElemViewFabric.getPlayerView(is_graphic)),
                        ElemViewFabric.getPileView(is_graphic))
        
        self.deck = ElemViewFabric.getDeckView(is_graphic)
        self.is_graphic = is_graphic
        
        
        self.me_myself = ElemViewFabric.getPlayerSbjView(is_graphic, my_name, my_id)
        self.rival     = ElemViewFabric.getPlayerSbjView(is_graphic, rival_name, self.rival_id)
        
    @property
    def rival_id(self):
        return int(not self.me_myself.id)
    
    # def _flipRivalCards(self):
    #     self.players.getPlayerById(self.rival_id).flipCards()
    
    def update(self):
        self.rival.update(self.last_move, 
                          self.players.getIdByRole('actv'))
        self.me_myself.update(self.last_move, 
                              self.players.getIdByRole('actv'))
        self.draw()
    
    def draw(self):
        self.stock.draw()
        self.rival.draw()
        self.players.getPlayerById(self.rival_id).draw()
        self.table.draw()
        self.players.getPlayerById(self.me_myself.id).draw()
        self.me_myself.draw()
        self.pile.draw()
