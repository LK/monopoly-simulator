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
		Can implement with a map from strings to functions and use eval() to run a
		method by string name.
2)  How to charge the owner for building? Properties don't have references to their
		owners
3)  Insert checks to ensure even building
4)  Insert checks to ensure even demolition

Other:
A)  Add methods for drawing a chance/community chest card. Entire implementation of
		the card decks belongs in the Card class! When landed() is called, Card will draw
		from the deck and make corresponding changes to the GameState.
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
			self._houses_requested       = { }  # maps a property to qty of houses requested there
			self._total_houses_requested = 0
			

	# Getters
	def get_square(self, i):
		return self._squares[i]

	def get_player(self, i):
		return self._players[i]

	def houses_requested_on(self, prop):
		return self._houses_requested[prop]


	# State-changing methods
	def set_owner(self, prop, player):
		player.add_prop(prop)

	def mortgage(self, prop):
		prop.mortgage()

	def unmortgage(self, prop):
		prop.unmortgage()

	def change_to(self, new_state):
		self = new_state


	# Building methods
	def request_houses_on(self, prop, qty):
		self._houses_requested[prop] = qty
		self._total_houses_requested += qty

	def are_enough_houses(self):
		return self._total_houses - self._total_houses_requested >= 0

	def build_all(self):    # TODO 2
		for prop in self._houses_requested.keys():
			prop.build(self._houses_requested[prop]) # TODO 3
			if (prop.has_hotel()):
				self._total_hotels -= 1
			else:
				self._total_houses -= self._houses_requested[prop]
		self._houses_requested = { }
		self._total_houses_requested = 0

	def demolish_houses_on(self, prop, qty):
		if (prop.has_hotel()):
			self._total_hotels += 1
			self._total_houses += qty - 1
		else:
			self._total_houses += qty
		prop.demolish(qty)  # TODO 4
