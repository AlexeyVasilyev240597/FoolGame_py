# from enum import IntEnum

from params import MAGIC_CONST
from items  import DECK_VOLUME
from player import Role, Status, Word
from rules  import swapRole, how_many_add_from_stock

class PlayingContext:
    # in the start of the game
    def __init__(self, trump):
        # a little complex, will implement later
        # self.table = {'up': [],
        #               'down': []}
        self.table_vol = 0
        # for 2 players
        self.stock_vol = DECK_VOLUME - 2*MAGIC_CONST
        self.trump = trump
        self.players = {Role.ACTV: {'vol': MAGIC_CONST,
                                    'status': Status.ATTACKER},
                        Role.PSSV: {'vol': MAGIC_CONST,
                                    'status': Status.DEFENDING}}
        
    def get_rival_vol(self):
        return self.players[Role.PSSV]['vol']
    
    def _add_from_stock(context):
        pv = {k: v['vol'] for k, v in context.players.items()}
        dv = how_many_add_from_stock(pv, context.stock_vol)
        for role in context.players:
            context.players[role]['vol'] += dv[role]
            context.stock_vol -= dv[role]
    
    def __repr__(self):
        return str("table_vol = " + str(self.table_vol) + " \n" +\
                 "stock_vol = " + str(self.stock_vol) + " \n" +\
                 str(self.players)) + "\n"
    
    # TODO: refactor as generator
    def netx_context(context, move):  
        new_context = context
        if 'card' in move:
            new_context.table_vol += 1
            new_context.players[Role.ACTV]['vol'] -= 1
            if not new_context.players[Role.ACTV]['status'] == Status.ADDING:
                swapRole(new_context.players)
        elif 'word' in move:
            if move['word'] == Word.BEATEN:
                new_context.players[Role.ACTV]['status'] = Status.DEFENDING
                new_context.players[Role.PSSV]['status'] = Status.ATTACKER
                PlayingContext._add_from_stock(new_context)
                new_context.table_vol = 0
                swapRole(new_context.players)
            elif move['word'] == Word.TAKE:
                new_context.players[Role.PSSV]['status'] = Status.DEFENDING
                swapRole(new_context.players)
            elif move['word'] == Word.TAKE_AWAY:
                new_context.players[Role.PSSV]['vol'] += new_context.table_vol
                new_context.players[Role.ACTV]['status'] = Status.ATTACKER
                new_context.players[Role.PSSV]['status'] = Status.DEFENDING
                PlayingContext._add_from_stock(new_context)
                new_context.table_vol = 0
        return new_context
    