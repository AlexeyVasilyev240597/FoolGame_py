from src.core.card import Rank, Suit, Side, Card
from src.core.players_hand import Word
from src.core.context import Context
from src.controller.player_sbj import PlayerSbj

class HumanConsole(PlayerSbj):
    def __init__(self) -> None:
        print('type your name')
        name = input()
        super().__init__(name)
    
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
        

    def _str2card(card_str: str) -> Card:
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
        if rank := HumanConsole._rankVal(rank):
            return Card(suit, rank, Side.FACE)
        else:
            return None
    
    def _str2word(word_str: str) -> Word:
        if word_str == 'BT':
            return Word.BEATEN
        elif word_str == 'TK':
            return Word.TAKE
        elif word_str == 'TA':
            return Word.TAKE_AWAY
        elif word_str == 'LS':
            return Word.LOST
        else:
            return None
    
    def chooseCard(self, context):
        pass
    
    # TODO: remove, use PlayerSbj.move (!)
    def move(self, context: Context):
        print(f'{self.name}, your move: ')
        move = {}
        move_str = input()
        if card := HumanConsole._str2card(move_str):
            move['card'] = card
        elif word := HumanConsole._str2word(move_str):
            move['word'] = word
        move['pl_id'] = self.id
        return move
    