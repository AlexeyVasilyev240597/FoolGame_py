from elems import Stock, Table
from player import Player
from context import Context

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
    if (pl_id == last_move['pl_id'] and
        'word' in last_move['move']):
        word = last_move['move']['word'].name
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


def display_stock(stock: Stock):
    stock_repr = '|'
    stock_repr += str(stock.vol) + ': '
    if stock.vol > 0:
        stock_repr += str(stock.last)
    else:
        stock_repr += stock.trump.value
    stock_repr += '|' + '\n'
    return stock_repr


def display_player(player: Player, prefix: str):
    player_repr = ''
    player_repr += player.status.name[0:2]
    player_repr += prefix
    player_repr += display_set(player.cards)
    player_repr += '\n'
    return player_repr


def display_table(table: Table):
    table_repr = ''
    table_repr += display_set(table.cards['down'])
    table_repr += display_set(table.cards['up'])
    table_repr += '\n'
    return table_repr


def display_field(context_vis: Context, last_move: dict):
    field = ''
    field += display_stock(context_vis.stock)
    
    field += display_player(context_vis.players.getPlayerById(0), 
                            get_prefix(context_vis, 0, last_move))
    
    field += display_table(context_vis.table)
    
    field += display_player(context_vis.players.getPlayerById(1),
                            get_prefix(context_vis, 1, last_move))
    
    field += '\n'
    print(field)
