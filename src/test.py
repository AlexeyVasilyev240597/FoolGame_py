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

from ai import Nikita_A, Sergey_C
from fool import FoolGame

pl_1 = Nikita_A()
pl_2 = Sergey_C()

game = FoolGame(pl_1, pl_2)
game.playGameRound()