from src.core.card import Rank, Suit, Side, Card
from src.view.card_view import CardView

class CardViewStr(CardView):
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
        try:
            rank_int = int(rank_char)
            if 6 <= rank_int and rank_int <= 10:
                return Rank(rank_int)
            else:
                return None
        except:
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
            return Card(suit, rank, Side.FACE)
        else:
            return None


    # def __repr__(self):
    #     if self.open:
    #         if self.rank.value > 10:
    #             rank = self.rank.name[0]
    #         else:
    #             rank = str(self.rank.value)
    #         #[ '\u2660', '\u2665', '\u2666', '\u2663' ]
    #         suit = self.suit.value
    #     else:
    #         rank = '*'
    #         suit = '*'
    #     return f'{rank:>2}-{suit}'        

    def draw(self):
        return self.__repr__()
