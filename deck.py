'''
This is a helper class to represent a deck of cards. Used for chance and community
chest. Ensures a random* and correct card-drawing order.

*Random according to python's native random.randint() method. The random number
generator can always be changed later by substituting this method where relevant.
'''

from random import randint
from sys import argv

class Deck(object):
    def __init__(self, cards):
        self._next = 0     # index of the next card to draw
        self._cards = []   # list of cards

        # Make private copy of cards
        for card in cards:
            self._cards.append(card)

        # Shuffle cards
        for i in range(0, len(cards)):
            r = randint(0, len(cards) - 1)
            temp = self._cards[i]
            self._cards[i] = self._cards[r]
            self._cards[r] = temp

    def draw(self):
        card = self._cards[self._next]
        self._next = (self._next + 1) % len(self._cards)
        return card

    def size(self):
        return len(self._cards)



# Test client
def main(num_trials):
    for t in range(0, num_trials):
        print "Trial ", t+1
        cards = [1, 2, 3, 4, 5]
        deck = Deck(cards)
        for count in range(0, 2): # repeat twice to check same order both times
          for i in range(0, deck.size()):
              print deck.draw()
          print

if (argv[0] == "deck.py"):
    num_trials = int(argv[1])
    main(num_trials)