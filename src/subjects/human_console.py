from src.core.card import Rank, Suit, Card
from src.core.player import Word
from src.core.context import Context
from src.subjects.player_sbj import PlayerSbj

class HumanConsole(PlayerSbj):
    def __init__(self) -> None:
        print('type your name')
        name = input()
        super().__init__(name)
    
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
    
    def chooseCard(self, context):
        pass
    
    def move(self, context: Context):
        print(f'{self.name}, your move: ')
        my_id = context.players.getIdByRole('actv')
        move = {'pl_id': my_id}
        move_str = input()
        if card := HumanConsole.str2card(move_str):
            move['move'] = {'card': card}
        elif word := HumanConsole.str2word(move_str):
            move['move'] = {'word': word}
        else:
            move['move'] = {}
        return move    