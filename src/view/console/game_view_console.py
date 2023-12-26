from src.view.elems_view import ItemView, PileView, StockView, TableView, DeckView
from src.view.player_view import PlayerView, PlayerSbjView


def display_set(cards):
    cards_repr = '[ '
    for card in cards:
        cards_repr += card.draw() + ' '
    cards_repr += ']\n'
    return cards_repr


# class PileViewConsole(ItemView):
#     def __init__(self):
#         ItemView.__init__(self, False)


class PileViewConsole(PileView):
    def draw(self):
        pass
        # print(self.vol)

class DeckViewConsole(DeckView):
    def draw(self):
        pass

class StockViewConsole(StockView):    
    def draw(self):
        stock_repr = '------------------------------------'
        stock_repr = '|'
        stock_repr += str(self.vol) + ': '
        if self.last:
            stock_repr += self.last.draw()
        else:
            if self.trump:
                stock_repr += self.trump.value
        stock_repr += '|' + '\n'
        print(stock_repr)


class PlayerViewConsole(PlayerView):        
    def draw(self):
        player_repr = ''
        player_repr += display_set(self.cards)
        player_repr += '\n'
        print(player_repr)


class PlayerSbjViewConsole(PlayerSbjView):    
    def draw(self):
        player_sbj_repr = ''
        player_sbj_repr += self.name + ': '
        if self.word:
            player_sbj_repr += f'{self.word.name}!'
        else:
            if self.is_active:
                player_sbj_repr += '(!)'
            else:
                player_sbj_repr += '...'
        player_sbj_repr += '\n'        
        print(player_sbj_repr)
        

class TableViewConsole(TableView):    
    def draw(self):
        table_repr = ''
        table_repr += display_set(self.low.cards)
        table_repr += display_set(self.top.cards)
        table_repr += '\n'
        print(table_repr)

