from src.core.card import Rank, Suit, Card

from src.core.elems import Stock, Table
from src.core.player import Player
from src.core.context import Context

from src.view.elems_view import StockView, TableView
from src.view.player_view import PlayerView

class CardViewStr:
    def __init__(self, card: Card):
        if card:
            if card.rank.value > 10:
                self.rank = card.rank.name[0]
            else:
                self.rank = str(card.rank.value)
            #[ '\u2660', '\u2665', '\u2666', '\u2663' ]
            self.suit = card.suit.value
        else:
            self.rank = '*'
            self.suit = '*'

    def rankVal(rank_char: str):
        if not isinstance(rank_char, str):
            return None
        if not (0 < len(rank_char) and len(rank_char) <= 2):
            return None
        if rank_char == 'J':
            return Rank.JACK
        elif rank_char == 'Q':
            return Rank.QUEEN
        elif rank_char == 'K':
            return Rank.KING
        elif rank_char == 'A':
            return Rank.ACE
        elif 6 <= int(rank_char) and int(rank_char) <= 10:
            return Rank(int(rank_char))
        else:
            return None

    def str2card(card_str: str) -> Card:
        card_str = card_str.split('-')
        if len(card_str) == 2:
            rank = card_str[0]
            suit = card_str[1]
        else:
            return None
        if suit in [s.value for s in Suit]:
            suit = Suit(suit)
        else:
            return None
        if rank := CardViewStr.rankVal(rank):
            return Card(suit, rank)
        else:
            return None

    def __str__(self):
        return f'{self.rank:>2}-{self.suit}'

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
        cards_repr.append(str(CardViewStr(c)))
    cards_repr = str(cards_repr) + '\n'
    return cards_repr

class StockViewConsole(StockView):
    def __init__(self, stock: Stock):
        super().__init__(stock)
    
    def draw(self):
        stock_repr = '|'
        stock_repr += str(self.vol) + ': '
        if self.vol > 0:
            stock_repr += str(CardViewStr(self.last))
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
    