from   enum import IntEnum
import json

from player import Word

class LogMode(IntEnum):
    ALL      = 1,
    ENDSPIEL = 2,
    SCORE    = 3

class Logger:    
    def __init__(self, mode):
        self.games = {'games': [], 'score': {}}
        self.mode = mode
        self.game_indx = -1
        self.dead_heat_counter = 0
    
    def newGame(self, pl_1, pl_2, stock):
        self.game_indx += 1
        if not self.mode == LogMode.SCORE:
            self.games['games'].append({'game_id': self.game_indx + 1,
                                        'pl_1': {'name': pl_1.name},
                                        'pl_2': {'name': pl_2.name},
                                        'parties': [],
                                        'fool': []})
        self.plrs = [pl_1, pl_2]
        if not self.mode == LogMode.SCORE:
            self.setParty(stock)        
    
    def setParty(self, stock):
        self.games['games'][self.game_indx]['parties'].append(
            {'stock':   {'trump': stock.trump.value, 'vol': stock.vol()},
             self.plrs[0].name: {'vol': self.plrs[0].vol(),
                                 'cards': repr(self.plrs[0].cards)},
             self.plrs[1].name: {'vol': self.plrs[1].vol(),
                                 'cards': repr(self.plrs[1].cards)},
             'moves': []})

    def setMove(self, mv, pl_actv, table, stock):
        if (self.mode == LogMode.ALL or 
            self.mode == LogMode.ENDSPIEL and stock.vol() == 0):
            if 'card' in mv:
                self.games['games'][self.game_indx]['parties'][-1]['moves'].append(
                    {'table':           {'up':   repr(table.cards['up']),
                                         'down': repr(table.cards['down'])}})
            if 'word' in mv:
                self.games['games'][self.game_indx]['parties'][-1]['moves'].append(
                    {pl_actv.name: mv['word'].name})
                if mv['word'] == Word.BEATEN or mv['word'] == Word.TAKE_AWAY:
                    self.setParty(stock)
        
    def setFool(self, fool_name):
        if not self.mode == LogMode.SCORE:
            self.games['games'][self.game_indx]['fool'] = fool_name
        if fool_name == 'no one':
            self.dead_heat_counter += 1
        
    def setScore(self):
        self.games['score'] = {self.plrs[0].name: self.plrs[0].losing_counter,
                               self.plrs[1].name: self.plrs[1].losing_counter,
                               'dead heat':       self.dead_heat_counter}
    
    def saveToJson(self):
        file_name = '../log/' + self.plrs[0].name + '_vs_' + self.plrs[1].name + '.json'
        with open(file_name, 'w') as json_file:
          json.dump(self.games, json_file, indent = 4)
