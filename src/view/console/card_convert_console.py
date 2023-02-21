from src.core.card import Rank, Suit, Card
from src.view.card_view import CardView

class CardViewStr(CardView):
    def __init__(self, card: Card):
        CardView.__init__(self, card)
        if self.open:
            if card.rank.value > 10:
                self.rank = card.rank.name[0]
            else:
                self.rank = str(card.rank.value)
            #[ '\u2660', '\u2665', '\u2666', '\u2663' ]
            self.suit = card.suit.value
        else:
            self.rank = '*'
            self.suit = '*'
        self.repr = f'{self.rank:>2}-{self.suit}'

    def _rankVal(rank_char: str):
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

    def cardView2card(card_str: str) -> Card:
        if not isinstance(card_str, str):
            return None
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
        if rank := CardViewStr._rankVal(rank):
            return Card(suit, rank)
        else:
            return None

    def __str__(self):
        return self.repr

    def draw(self):
        print(self.repr)
