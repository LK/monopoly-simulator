'''
Author:   Michael Friedman
Created:  6/29/16

Description:
This class serves as a container for all the components of the game in its current
state: players, squares, chance/community chest cards, etc. Any changes to the state
of the game should go through this object via the state-changing methods.


TODO:
In-line:
1)  Assumes Square/Card class initializes by its name, as specified in squares.txt.
2)  Insert checks to ensure even building given the GSC that builds houses
'''

class GameState(object):
	# Constants
	NUM_HOUSES = 32
	NUM_HOTELS = 12
	NUM_SQUARES = 40

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
			squares.append(Square(square_name)) # TODO: Initialize squares 1
		return squares

	def __init__(self, num_players):
		self._players                = initialize_players(num_players)
		self._squares                = initialize_squares()
		self._houses_remaining       = NUM_HOUSES
		self._hotels_remaining       = NUM_HOTELS

	# Private
	def _copy(self):
		num_players = len(self._players)
		copy = GameState(num_players)
		for i in range(0, num_players):
			copy._players[i] = self._players[i].copy()
		for square in self._squares:
			copy._squares.append(square.copy())
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

	@property
	def total_houses(self):
		return self._total_houses
	
	@property
	def total_hotels(self):
		return self._total_hotels
	
	def get_owner(self, prop):
		for player in self._players:
			for p in player.props:
				if (p == prop):
					return player
		return None

	# Other
	def are_enough_houses(self, qty):
		return self._houses_remaining - qty >= 0

	def are_enough_hotels(self, qty):
		return self._hotels_remaining - qty >= 0

	def builds_evenly(self, changes):
		# TODO: 2 - Implement builds_evenly()
		return None

	def apply(self, changes):
		for player, change_in_cash in changes.change_in_cash.iteritems():
			player.cash += change_in_cash

		for player, new_position in changes.new_position.iteritems():
			player.position = new_position

		for player, added_props in changes.added_props.iteritems():
			player.add_properties(added_props)

		for player, removed_props in changes.removed_props.iteritems():
			player.remove_properties(removed_props)

		for player, change_in_jail_moves in changes.change_in_jail_moves.iteritems():
			player.jail_moves += change_in_jail_moves

		for player, change_in_jail_free_count in changes.change_in_jail_free_count.iteritems():
			player.jail_free_count += change_in_jail_free_count

		for player, is_in_game in changes.is_in_game.iteritems():
			player.is_in_game = is_in_game

		for prop, change_in_houses in changes.change_in_houses.iteritems():
			if change_in_houses == 0:
				continue
			
			prev = prop.num_houses
			prop.num_houses += change_in_houses
			if prop.num_houses == 5:
				self._houses_remaining += prev
				self._hotels_remaining -= 1
			else:
				self._houses_remaining -= change_in_houses

		for prop, is_mortgaged in changes.is_mortgaged.iteritems():
			prop.is_mortgaged = is_mortgaged     
