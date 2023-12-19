from src.core.card import Card
from src.view.console.card_convert_console import CardViewStr
from src.view.graphic.card_convert_graphic import CardViewGraph

class CardConverter:
    
    def card2cardView(card: Card, is_graphic: bool):
        if is_graphic:
            return CardViewGraph(card)
        else:
            return CardViewStr(card)
    
    def cardView2card(card_view, is_graphic: bool):
        if is_graphic:
            return CardViewGraph.cardView2card(card_view)
        else:
            return CardViewStr.cardView2card(card_view)
    
