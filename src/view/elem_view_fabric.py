# from abc import ABC, abstractmethod

# from src.core.context import Context
from .elems_view import DeckView, StockView, TableView
from .player_view import PlayerView, PlayerSbjView

from .console.game_view_console import (StockViewConsole, TableViewConsole, 
                                      PlayerViewConsole, PlayerSbjViewConsole, 
                                      DeckViewConsole)


class ElemViewFabric:
    
    def getStockView(is_graphic: bool) -> StockView:
        if is_graphic:
            return None
        else:
            return StockViewConsole()
    
    def getTableView(is_graphic: bool) -> TableView:
        if is_graphic:
            return None
        else:
            return TableViewConsole()

    def getPlayerView(is_graphic: bool) -> PlayerView:
        if is_graphic:
            return None
        else:
            return PlayerViewConsole()
    
    def getPlayerSbjView(is_graphic: bool, name: str, id: int) -> PlayerSbjView:
        if is_graphic:
            return None
        else:
            return PlayerSbjViewConsole(name, id)
    
    def getDeckView(is_graphic: bool) -> DeckView:
        if is_graphic:
            return None
        else:
            return DeckViewConsole()