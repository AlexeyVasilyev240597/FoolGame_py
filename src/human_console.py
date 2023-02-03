from card import Rank, Suit, Card
from player import Word, PlayerSbj

class HumanConsole(PlayerSbj):
    def __init__(self) -> None:
        print('type your name')
        name = input()
        super().__init__(name)
    
    def str2card(card_str: str) -> Card:
        card_str = card_str.split('-')
        if len(card_str) == 2:
            suit = card_str[0] 
            rank = card_str[1]
        else:
            return None
        if suit in [s.value for s in Suit]:
            suit = Suit(suit)
        else:
            return None
        if rank in [r.value for r in Rank]:
            rank = Rank(rank)
        else:
            return None
        return Card(suit, rank)
    
    def str2word(word_str: str) -> Word:
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
    
    def move(self, context):
        print(f'{self.name}, your move: ')
        move_str = input()
        if card := HumanConsole.str2card(move_str):
            return {'card': card}
        elif word := HumanConsole.str2word(move_str):
            return {'word': word}
        else:
            return None
        