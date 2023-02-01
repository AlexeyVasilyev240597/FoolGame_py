from elems import Stock, Table
from player import Player, Word
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


def display_player(player: Player, is_acive: bool, word: Word):
    player_repr = ''
    player_repr += player.status.name[0:2]
    if is_acive:
        player_repr += '(!) '
    else:
        if word:
            player_repr += f'({word.name}!) '
    player_repr += display_set(player.cards)
    player_repr += '\n'
    return player_repr


def display_table(table: Table):
    table_repr = ''
    table_repr += display_set(table.cards['down'])
    table_repr += display_set(table.cards['up'])
    table_repr += '\n'
    return table_repr


def display_field(context_vis: Context, move, moved_id):
    if 'word' in move:
        word = move.get('word')
    else:
        word = None
    field = ''
    field += display_stock(context_vis.stock)
    field += display_player(context_vis.players.getPlayerById(0), 
                            context_vis.players.getIdByRole('actv') == 0,
                            word if moved_id == 0 else None)
    field += display_table(context_vis.table)
    field += display_player(context_vis.players.getPlayerById(1), 
                            context_vis.players.getIdByRole('actv') == 1,
                            word if moved_id == 1 else None)
    field += '\n'
    print(field)
