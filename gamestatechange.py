class GameStateChange(object):
	def __init__(self, change_in_cash={}, new_position={}, added_properties={}, removed_properties={}, change_in_jail_moves={}, change_in_jail_free_count={}, is_in_game={}, change_in_houses={}, is_mortgaged={}):
		self._change_in_cash            = change_in_cash
		self._new_position              = new_position
		self._added_properties          = added_properties
		self._removed_properties        = removed_properties
		self._change_in_jail_moves			= change_in_jail_moves
		self._change_in_jail_free_count	= change_in_jail_free_count
		self._is_in_game								= is_in_game
		self._change_in_houses					= change_in_houses
		self._is_mortgaged							= is_mortgaged

	@property
	def change_in_cash(self):
		return change_in_cash
		
	@property
	def new_position(self):
		return new_position
		
	@property
	def added_properties(self):
		return added_properties
	
	@property
	def removed_properties(self):
		return removed_properties
	
	@property
	def change_in_jail_moves(self):
		return change_in_jail_moves
	
	@staticmethod
	def combine(self, changes):
		combined = GameStateChange()
		for change in changes:
			# Merge change_in_cash
			for player, change_in_cash in change._change_in_cash.iteritems():
				if player not in combined._change_in_cash:
					combined._change_in_cash[player] = 0
				combined._change_in_cash[player] += change_in_cash

			# Merge new_position
			for player, new_position in change._new_position.iteritems():
				combined._new_position[player] = new_position

			# Merge added_properties
			for player, props in change._added_properties.iteritems():
				if player not in combined._added_properties:
					combined._added_properties[player] = []
				
				for prop in props:
					if prop in combined._removed_properties[player]:
						combined._removed_properties[player].remove(prop)

					if prop not in combined._added_properties[player]:
						combined._added_properties[player].append(prop)

			# Merge removed_properties
			for player, props in change._removed_properties.iteritems():
				if player not in combined._removed_properties:
					combined._removed_properties[player] = []
				
				for prop in props:
					if prop in combined._added_properties[player]:
						combined._added_properties[player].remove(prop)

					if prop not in combined._removed_properties[player]:
						combined._removed_properties[player].append(prop)

			# Merge change_in_jail_moves
			for player, change_in_jail_moves in change._change_in_jail_moves.iteritems():
				if player not in combined._change_in_jail_moves:
					combined._change_in_jail_moves[player] = 0
				combined._change_in_jail_moves[player] += change_in_jail_moves

			# Merge change_in_jail_free_count
			for player, change_in_jail_free_count in change._change_in_jail_free_count.iteritems():
				if player not in combined._change_in_jail_free_count:
					combined._change_in_jail_free_count[player] = 0
				combined._change_in_jail_free_count[player] += change_in_jail_free_count

			# Merge is_in_game
			for player, is_in_game in change._is_in_game.iteritems():
				combined._is_in_game[player] = is_in_game

			# Merge change_in_houses
			for color_property, change_in_houses in change._change_in_houses.iteritems():
				if player not in combined._change_in_houses:
					combined._change_in_houses[color_property] = 0
				combined._change_in_houses[color_property] += change_in_houses

			# Merge is_mortgaged
			for prop, is_mortgaged in change._is_mortgaged.iteritems():
				combined._is_mortgaged[prop] = is_mortgaged

		return combined

	def total_houses_built(self):
		return sum(self.change_in_houses.values())
