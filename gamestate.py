'''
Author:   Michael Friedman
Created:  6/29/16

Description:
This class serves as a container for all the components of the game in its current
state: players, squares, chance/community chest cards, etc. Any changes to the state
of the game should go through this object via the state-changing methods.
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

	def __init__(self, num_players):
		self._players                = initialize_players(num_players)
		self._squares                = create_squares()
		self._houses_remaining       = NUM_HOUSES
		self._hotels_remaining       = NUM_HOTELS
		self._bank									 = Player(cash=0)

	# Private
	def _copy(self):
		num_players = len(self._players)
		copy = GameState(num_players)
		for i in range(0, num_players):
			copy._players[i] = self._players[i].copy()
		for square in self._squares:
			copy._squares.append(square.copy())		# TODO: Implement Square.copy() for all subclasses
		copy._houses_remaining = self._houses_remaining
		copy._hotels_remaining = self._hotels_remaining
		return copy

	# Getters
	@property
	def squares(self):
		return self._squares

	@property
	def players(self):
		return self._players

	@property
	def houses_remaining(self):
		return self._houses_remaining
	
	@property
	def hotels_remaining(self):
		return self._hotels_remaining
	
	@property
	def bank(self):
		return self._bank
	

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

	# Applies a single GameStateChange
	def _apply_single_change(self, change):
		for player, change_in_cash in change.change_in_cash.iteritems():
			player.cash += change_in_cash

		for player, new_position in change.new_position.iteritems():
			player.position = new_position
			if new_position < player.position:
				player.cash += 200

		for player, added_props in change.added_props.iteritems():
			player.add_properties(added_props)

		for player, removed_props in change.removed_props.iteritems():
			player.remove_properties(removed_props)

		for player, change_in_jail_moves in change.change_in_jail_moves.iteritems():
			player.jail_moves += change_in_jail_moves

		for player, change_in_jail_free_count in change.change_in_jail_free_count.iteritems():
			player.jail_free_count += change_in_jail_free_count

		for player, is_in_game in change.is_in_game.iteritems():
			player.is_in_game = is_in_game

		for prop, change_in_houses in change.change_in_houses.iteritems():
			if change_in_houses == 0:
				continue
			
			prev = prop.num_houses
			prop.num_houses += change_in_houses
			if prop.num_houses == 5:
				self._houses_remaining += prev
				self._hotels_remaining -= 1
			else:
				self._houses_remaining -= change_in_houses

		for prop, is_mortgaged in change.is_mortgaged.iteritems():
			prop.is_mortgaged = is_mortgaged  


	# Applies a GroupOfChanges
	def apply(self, changes):
		for change in changes:
			_apply_single_change(change)   
