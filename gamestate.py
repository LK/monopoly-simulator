'''
Author:   Michael Friedman
Created:  6/29/16

Description:
This class serves as a container for all the components of the game in its current
state: players, squares, chance/community chest cards, etc. Any changes to the state
of the game should go through this object via the state-changing methods.


TODO
In-line:
1)  Assumes Square/Card class initializes by its name, as specified in squares.txt.
2)  Insert checks to ensure even building given the GSC that builds houses
3)  Write apply()
'''

class GameState(object):
  # Constants
  NUM_HOUSES = 32
  NUM_HOTELS = 12

  # Initialization
  def initialize_players(num_players):
    players = []
    for i in range(0, num_players):
      players.append(Player())
    return players

  def initialize_squares():
    squares_file = "squares.txt"
    squares = []
    f = open(squares_file, "r")
    square_names = f.read().split("\n")
    for square_name in square_names:
      squares.append(Square(square_name)) # TODO 1
    return squares

  def __init__(self, num_players):
      self._players                = initialize_players(num_players)
      self._squares                = initialize_squares()
      self._total_houses           = NUM_HOUSES
      self._total_hotels           = NUM_HOTELS

  # Private
  def _copy(self):
    num_players = len(self._players)
    copy = GameState(num_players)
    for i in range(0, num_players):
        copy._players[i] = self._players[i]
    for square in self._squares:
        copy._squares.append(square)
    copy._total_houses = self._total_houses
    copy._total_hotels = self._total_hotels
    return copy

  # Getters
  @property
  def squares(self):
      return self._squares
  
  @property
  def players(self):
      return self._players
  
  def get_owner(self, prop):
    for player in self._players:
        props = player.props
        for p in props:
            if (p == prop):
                return player
    return None

  # Other
  def are_enough_houses(self, qty):
    return self._num_houses - qty >= 0

  def builds_evenly(self, changes):
    # TODO 2

  def apply(self, changes):
    # TODO 3