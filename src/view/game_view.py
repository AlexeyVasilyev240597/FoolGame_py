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
        
                         
        # self.stock     = ElemViewFabric.getStockView(is_graphic)
        # self.table     = ElemViewFabric.getTableView(is_graphic)
        # self.players   = PlayersHands(ElemViewFabric.getPlayerView(is_graphic),
        #                          ElemViewFabric.getPlayerView(is_graphic))
        # self.deck      = ElemViewFabric.getDeckView(is_graphic, deck)
        
        self.me_myself = ElemViewFabric.getPlayerSbjView(is_graphic, my_name, my_id)
        self.rival     = ElemViewFabric.getPlayerSbjView(is_graphic, rival_name, self.rival_id)
        
    @property
    def rival_id(self):
        return int(not self.me_myself.id)
    
    # def _flipRivalCards(self):
    #     self.players.getPlayerById(self.rival_id).flipCards()
    
    def update(self):
        # syncPile(self.pile, context.pile)
        # syncPile(self.stock, context.stock)
        # syncPile(self.players.getPlayerById(self.me_myself.id), context.getPlayerById(self.me_myself.id))
        # syncPile(self.players.getPlayerById(self.rival_id), context.getPlayerById(self.rival_id))
        # syncPile(self.table.low, context.table.low)
        # syncPile(self.table.top, context.table.top)
        
        # self._flipRivalCards()
        # self.stock_v.update(context.stock)
        self.rival.update(self.last_move, 
                          self.players.getIdByRole('actv'))
        # self.rival_cards.update(context.players.getPlayerById(rival_id))
        # self.table_v.update(context.table)
        # self.my_cards.update(context.players.getPlayerById(self.my_id))
        self.me_myself.update(self.last_move, 
                              self.players.getIdByRole('actv'))
        # self.deck_v.update(context.deck)
        self.draw()
        # self._flipRivalCards()
    
    def draw(self):
        self.stock.draw()
        self.rival.draw()
        self.players.getPlayerById(self.rival_id).draw()
        self.table.draw()
        self.players.getPlayerById(self.me_myself.id).draw()
        self.me_myself.draw()
        self.pile.draw()
    
# class GameView:
#     def __init__(self, 
#                  is_graphic: bool,
#                  rival_name: str,
#                  my_name: str, 
#                  my_id: int,
#                  is_user: bool = False
#                  ) -> None:
#         self.my_id = my_id
#         self.is_user = is_user
        
#         rival_id = int(not self.my_id)
#         self.stock_v     = ElemViewFabric.getStockView(is_graphic)
#         self.rival       = ElemViewFabric.getPlayerSbjView(is_graphic, rival_name, rival_id)
#         self.rival_cards = ElemViewFabric.getPlayerView(is_graphic)
#         self.table_v     = ElemViewFabric.getTableView(is_graphic)
#         self.me_myself   = ElemViewFabric.getPlayerSbjView(is_graphic, my_name, my_id)
#         self.my_cards    = ElemViewFabric.getPlayerView(is_graphic)
#         self.deck_v      = ElemViewFabric.getDeckView(is_graphic)
    
#     def update(self, context: Context):
#         self.stock_v.update(context.stock)
#         rival_id = int(not self.my_id)
#         self.rival.update(context.last_move, 
#                           rival_id == context.players.getIdByRole('actv'))
#         self.rival_cards.update(context.players.getPlayerById(rival_id))
#         self.table_v.update(context.table)
#         self.my_cards.update(context.players.getPlayerById(self.my_id))
#         self.me_myself.update(context.last_move, 
#                               self.my_id == context.players.getIdByRole('actv'))
#         self.deck_v.update(context.deck)
#         if self.is_user:
#             self.draw()
    
#     def draw(self):
#         self.stock_v.draw()
#         self.rival.draw()
#         self.rival_cards.draw()
#         self.table_v.draw()
#         self.my_cards.draw()
#         self.me_myself.draw()
#         self.deck_v.draw()
    
