from src.core.elems import Stock, Table
from src.core.player import Player
from src.core.context import Context

from src.view.elems_view import StockView, TableView
from src.view.player_view import PlayerView

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

def get_prefix(context: Context, pl_id: int, last_move: dict):
    prefix = ''
    if ('pl_id' in last_move and 
        pl_id == last_move['pl_id'] and
        'word' in last_move):
        word = last_move['word'].name
        prefix = f'({word})'
    else:
        if pl_id == context.players.getIdByRole('actv'):
            prefix = '(!)'
    return prefix

def display_set(cards):
    cards_repr = []
    for c in cards:
        if c:
            cards_repr.append(str(c))
        else:
            cards_repr.append('*-*')
    cards_repr = str(cards_repr) + '\n'
    return cards_repr

class StockViewConsole(StockView):
    def __init__(self, stock: Stock):
        super().__init__(stock)
    
    def draw(self):
        stock_repr = '|'
        stock_repr += str(self.vol) + ': '
        if self.vol > 0:
            stock_repr += str(self.last)
        else:
            stock_repr += self.trump.value
        stock_repr += '|' + '\n'
        # return stock_repr
        print(stock_repr)


class PlayerViewConsole(PlayerView):
    def __init__(self, player: Player):
        super().__init__(player)
        
    def draw(self, prefix: str):
        player_repr = ''
        player_repr += self.status.name[0:2]
        player_repr += prefix
        player_repr += display_set(self.cards)
        player_repr += '\n'
        # return player_repr
        print(player_repr)


class TableViewConsole(TableView):
    def __init__(self, table: Table):
        super().__init__(table)
    
    def draw(self):
        table_repr = ''
        table_repr += display_set(self.low)
        table_repr += display_set(self.top)
        table_repr += '\n'
        # return table_repr
        print(table_repr)

def display_field(context_vis: Context, last_move: dict, user_id: int) -> None:
    StockViewConsole(context_vis.stock).draw()
    
    rival_id = int(not user_id)
    PlayerViewConsole(context_vis.players.getPlayerById(rival_id)).draw( 
                            get_prefix(context_vis, rival_id, last_move))
    
    TableViewConsole(context_vis.table).draw()
    
    PlayerViewConsole(context_vis.players.getPlayerById(user_id)).draw( 
                            get_prefix(context_vis, user_id, last_move))
    