from src.core.players_hand import Word
from src.core.context import Context
from src.controller.player_sbj import PlayerSbj
from src.view.console.card_convert_console import CardViewStr

class HumanConsole(PlayerSbj):
    def __init__(self) -> None:
        print('type your name')
        name = input()
        super().__init__(name)
    
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
        move = {}
        move_str = input()
        if card := CardViewStr.cardView2card(move_str):
            move['card'] = card
        elif word := HumanConsole.str2word(move_str):
            move['word'] = word
        return move