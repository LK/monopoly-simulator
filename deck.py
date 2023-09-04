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
    self._next = 0                       # index of the next card to draw
    self._cards = [None] * len(cards)   # list of cards

    # Make private copy of cards
    for i in range(0, len(cards)):
      self._cards[i] = cards[i]

  def size(self):
    return len(self._cards)

  def shuffle(self):
    for i in range(0, self.size()):
      r = randint(0, self.size() - 1)
      temp = self._cards[i]
      self._cards[i] = self._cards[r]
      self._cards[r] = temp

  def draw(self):
    if self.size() < 1:
      raise Exception("No cards in the Deck")

    card = self._cards[self._next]
    self._next = (self._next + 1) % self.size()
    return card

  def peek(self):
    if self.size() < 1:
      raise Exception("No cards in the Deck")

    return self._cards[self._next]

  def draw_and_remove(self):
    if self.size() < 1:
      raise Exception("No cards in the Deck")

    card = self._cards[self._next]
    del self._cards[self._next]
    return card

  def insert_on_bottom(self, item):
    self._cards.append(item)

  def insert_on_top(self, item):
    self._cards.insert(0, item)

  def insert_randomly(self, item):
    r = randint(0, self.size() - 1)
    self._cards.insert(r, item)



# Test client
def main():
  cards = [1, 2, 3, 4, 5]
  print("---CARDS---")
  print(cards)



  print("Test shuffle() properly randomizes the cards")
  deck = Deck(cards)
  T = 10000

  # Initialize frequency table to record how often each card appears in
  # each position of the deck
  freq = {}
  for card in cards:
    for i in range(0, deck.size()):
      p = (card, i)
      freq[p] = 0

  print("Shuffling over many trials...")
  for t in range(0, T):
    deck.shuffle()

    # Record how often each card appears in each position of the deck
    for i in range(0, deck.size()):
      p = (deck.draw(), i)
      freq[p] += 1

  # Calculate average frequencies and compare to probabilistic average
  prob = 1.0 / deck.size()
  print("Each card should appear in each position of the deck with probability " + str(prob))
  print("(c, d) : average number of times card c appeared at position d in the deck")
  for p, freq in freq.items():
    avg_freq = float(freq) / float(T)
    print(str(p) + " : " + str(avg_freq))
  print()
  del deck



  print("Test draw() takes cards out in order")
  deck = Deck(cards)
  deck.shuffle()
  for count in range(0, 2): # repeat twice to check same order both times
    for i in range(0, deck.size()):
      print("Draw card " + str(i+1) + ": " + str(deck.draw()))
    print()
  print()
  del deck



  print("Test draw() vs peek()")
  deck = Deck(cards)
  deck.shuffle()
  for i in range(0, deck.size()):
    print("Peek", deck.peek())
    print("Draw", deck.draw())
    print("Peek again", deck.peek())
  print()
  del deck



  print("Test draw_and_remove() + insert_on_bottom() does the same as draw()")
  deck1 = Deck(cards)
  deck2 = Deck(cards)
  for i in range(0, deck1.size()):
    item = deck1.draw_and_remove()
    print("Deck 1: Draw and remove", item)
    print("Deck 1: Inserting on bottom...")
    deck1.insert_on_bottom(item)
    print("Deck 2: Draw", deck2.draw())
  print()
  del deck1
  del deck2



  print("Test draw_and_remove() + insert_on_top() does the same as peek()")
  deck1 = Deck(cards)
  deck2 = Deck(cards)
  for i in range(0, deck1.size()):
    item = deck1.draw_and_remove()
    print("Deck 1: Draw and remove", item)
    print("Deck 1: Inserting on top...")
    deck1.insert_on_top(item)
    print("Deck 2: Peek", deck2.peek())
    print("Next card...")
    deck1.draw()
    deck2.draw()
  print()
  del deck1
  del deck2



if __name__ == "__main__":
  main()