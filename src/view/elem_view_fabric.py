
from src.core.elems import Deck
from src.view.elems_view import DeckView, StockView, TableView
from src.view.player_view import PlayerView, PlayerSbjView

from src.view.console.game_view_console import (StockViewConsole, TableViewConsole, 
                                      PlayerViewConsole, PlayerSbjViewConsole, 
                                      DeckViewConsole)

class ElemViewFabric:
    
    def getStockView(is_graphic: bool) -> StockView:
        if is_graphic:
            return None
        else:
            return StockViewConsole(False)
    
    def getTableView(is_graphic: bool) -> TableView:
        if is_graphic:
            return None
        else:
            return TableViewConsole(False)

    def getPlayerView(is_graphic: bool) -> PlayerView:
        if is_graphic:
            return None
        else:
            return PlayerViewConsole(False)
    
    def getPlayerSbjView(is_graphic: bool, name: str, id: int) -> PlayerSbjView:
        if is_graphic:
            return None
        else:
            return PlayerSbjViewConsole(False, name, id)
    
    def getDeckView(is_graphic: bool) -> DeckView:
        if is_graphic:
            return None
        else:
            return DeckViewConsole(False)

