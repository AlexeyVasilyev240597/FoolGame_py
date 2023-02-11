from card import Suit, Rank, Side, Card
from card_set import CardSet, CardSetNoGraphic

import copy
import pytest


s1 = CardSetNoGraphic()
s1.addCard(Card(Suit.DIAMONDS, Rank.SIX))
s1.addCard(Card(Suit.DIAMONDS, Rank.SEVEN))

s2 = CardSetNoGraphic()
s2.addCard(Card(Suit.HEARTS, Rank.EIGHT, Side.FACE))
s2.addCard(Card(Suit.HEARTS, Rank.NINE,  Side.FACE))

def get_set_as_str(c_set: CardSet):
    return str(c_set)

@pytest.mark.parametrize("s1,s2", 
                         [(copy.deepcopy(s1), copy.deepcopy(s2))])
def test_open_sets(s1, s2):
    s1.shift(s2, True)
    assert get_set_as_str(s1) == "[]"
    assert get_set_as_str(s2) == "['H-8', 'H-9', 'D-6', 'D-7']"
    # print('\n test of shifting s1 -> s2 with opening s1')

@pytest.mark.parametrize("s1,s2", 
                         [(copy.deepcopy(s1), copy.deepcopy(s2))])
def test_close_sets(s1: CardSet, s2: CardSet):
    s2.shift(s1, True)
    assert get_set_as_str(s1) == "['*-*', '*-*', '*-*', '*-*']"
    assert get_set_as_str(s2) == "[]"
    # print('\n test of shifting s2 -> s1 with closing s2')

print("Hello, i am writing you from card_set_test.py. I feel good-)")

