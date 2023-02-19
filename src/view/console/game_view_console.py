from src.view.elems_view import PileView, DeckView, StockView, TableView
from src.view.player_view import PlayerView, PlayerSbjView
from src.view.console.card_convert_console import CardViewStr

# def display_set(cards, align):
#     cards_repr = '['
#     for c in cards:
#         card = str(c)
#         if align == 'left':
#             cards_repr += f'{card:<7},'
#         elif align == 'right':
#             cards_repr += f'{card:>7},'
#     cards_repr += ']\n'
#     return cards_repr

# class FieldView:
#     def __init__(self, player_id):
#         self.player_id = player_id


def display_set(cards):
    cards_repr = []
    for c in cards:
        cards_repr.append(str(c))
    cards_repr = str(cards_repr) + '\n'
    return cards_repr

class PileViewConsole(PileView):
    def __init__(self):
        PileView.__init__(self, False)

class DeckViewConsole(PileViewConsole, DeckView):
    def draw(self):
        pass
        # print(self.vol)

class StockViewConsole(PileViewConsole, StockView):    
    def draw(self):
        stock_repr = '|'
        stock_repr += str(self.vol) + ': '
        if self.vol > 0:
            stock_repr += str(CardViewStr(self.last))
        else:
            stock_repr += self.trump.value
        stock_repr += '|' + '\n'
        print(stock_repr)


class PlayerViewConsole(PileViewConsole, PlayerView):        
    def draw(self):
        player_repr = ''
        player_repr += display_set(self.cards)
        player_repr += '\n'
        print(player_repr)


class PlayerSbjViewConsole(PlayerSbjView):
    def __init__(self, name: str, id: int) -> None:
        PlayerSbjView.__init__(self, name, id)
    
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
        

class TableViewConsole(PileViewConsole, TableView):    
    def draw(self):
        table_repr = ''
        table_repr += display_set(self.low)
        table_repr += display_set(self.top)
        table_repr += '\n'
        print(table_repr)

# def display_field(context: Context, last_move: dict, user_id: int) -> None:
#     StockViewConsole(context.stock).draw()
    
#     rival_id = int(not user_id)
#     PlayerViewConsole(context.players.getPlayerById(rival_id)).draw( 
#                             get_prefix(context, rival_id, last_move))
    
#     TableViewConsole(context.table).draw()
    
#     PlayerViewConsole(context.players.getPlayerById(user_id)).draw( 
#                             get_prefix(context, user_id, last_move))
    