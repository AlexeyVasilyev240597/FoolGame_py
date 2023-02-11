# # from fool import play_fool_game

# # play_fool_game('Alexey', 'Nikita_A')

# class ListClass:   
#     def __init__(self, arr):
#         self.arr = arr

#     def swapper(func):
#         def wrap(self, *args, **kwargs):
#             print("inside wrap")
#             el = func(self, *args, **kwargs)
#             self.arr[0], self.arr[1] = self.arr[1], self.arr[0]
#             return el
#         return wrap

#     @swapper
#     def method(self, i):
#         el =self.arr.pop(i)
#         print(self.arr)
#         return el

#     # wrapper = staticmethod(wrapper)


# l = ListClass([10, 15, 20])
# e = l.method(1)
# print(e)
# print(l.arr)

# def read_even():
#     print('put even number')
#     return int(input())

# while (n := read_even()) % 2 == 1:
#     pass
# print(f'yes, {n} is even')

# from enum import Enum

# class Rank(Enum):
#     SIX   = '6'
#     SEVEN = '7'
#     EIGHT = '8'
#     NINE  = '9'
#     TEN   = '10'
#     JACK  = 'J'
#     QUEEN = 'Q'
#     KING  = 'K'
#     ACE   = 'A'

#     def int(self):
#         if self.value == 'J':
#             return 11
#         elif self.value == 'Q':
#             return 12
#         elif self.value == 'K':
#             return 13
#         elif self.value == 'A':
#             return 14
#         else:
#             return int(self.value)


# r1 = Rank(Rank.JACK)
# r2 = Rank('6')
# print(r1.int()+r2.int()+Rank.ACE.int())




from src.subjects.ai import Nikita_A, Sergey_C
from src.subjects.human_console import HumanConsole
from src.subjects.player_sbj import PlayersSbjs
from src.fool import FoolGame


pl_1 = HumanConsole()
# pl_1 = Nikita_A()
pl_2 = Sergey_C()

pls = PlayersSbjs(pl_1, pl_2)

game = FoolGame(pls)
game.playGameRound()