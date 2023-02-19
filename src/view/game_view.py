# from abc import ABC, abstractmethod

from src.core.context import Context
# from .elems_view import DeckView, StockView, TableView
# from .player_view import PlayerView

from src.view.elem_view_fabric import ElemViewFabric

class GameView:
    def __init__(self, 
                 is_graphic: bool,
                 rival_name: str,
                 my_name: str, 
                 my_id: int,
                 is_user: bool = False
                 ) -> None:
        self.my_id = my_id
        self.is_user = is_user
        
        rival_id = int(not self.my_id)
        self.stock_v     = ElemViewFabric.getStockView(is_graphic)
        self.rival       = ElemViewFabric.getPlayerSbjView(is_graphic, rival_name, rival_id)
        self.rival_cards = ElemViewFabric.getPlayerView(is_graphic)
        self.table_v     = ElemViewFabric.getTableView(is_graphic)
        self.me_myself   = ElemViewFabric.getPlayerSbjView(is_graphic, my_name, my_id)
        self.my_cards    = ElemViewFabric.getPlayerView(is_graphic)
        self.deck_v      = ElemViewFabric.getDeckView(is_graphic)
    
    def update(self, context: Context):
        self.stock_v.update(context.stock)
        rival_id = int(not self.my_id)
        self.rival.update(context.last_move, 
                          rival_id == context.players.getIdByRole('actv'))
        self.rival_cards.update(context.players.getPlayerById(rival_id))
        self.table_v.update(context.table)
        self.my_cards.update(context.players.getPlayerById(self.my_id))
        self.me_myself.update(context.last_move, 
                              self.my_id == context.players.getIdByRole('actv'))
        self.deck_v.update(context.deck)
        if self.is_user:
            self.draw()
    
    def draw(self):
        self.stock_v.draw()
        self.rival.draw()
        self.rival_cards.draw()
        self.table_v.draw()
        self.my_cards.draw()
        self.me_myself.draw()
        self.deck_v.draw()
    
