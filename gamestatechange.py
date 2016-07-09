class GameStateChange(object):
	def __init__(self, change_in_cash={}, new_position={}, added_properties={}, removed_properties={}, change_in_jail_moves={}, change_in_jail_free_count={}, is_in_game={}):
		self._change_in_cash            = change_in_cash
		self._new_position              = new_position
		self._added_properties          = added_properties
		self._removed_properties        = removed_properties
		self._change_in_jail_moves      = change_in_jail_moves
		self._change_in_jail_free_count = change_in_jail_free_count
		self._is_in_game                = is_in_game

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
			for player, val in change._change_in_cash.iteritems():
				if player not in combined._change_in_cash:
					combined._change_in_cash[player] = 0

				combined._change_in_cash[player] += val

			# Merge new_position
			for player, val in change._new_position.iteritems():
				if player not in combined._new_position:
					combined._new_position[player] = 0

				combined._new_position[player] = val

			# Merge added_properties
			for player, val in change._added_properties.iteritems():
				if player not in combined._added_properties:
					combined._added_properties[player] = []
				
				for prop in val:
					if prop in combined._removed_properties[player];
						combined._removed_properties[player].remove(prop)

					if prop not in combined._added_properties[player]:
						combined._added_properties[player].append(prop)

			# Merge removed_properties
			for player, val in change._removed_properties.iteritems():
				if player not in combined._removed_properties:
					combined._removed_properties[player] = []
				
				for prop in val:
					if prop in combined._added_properties[player];
						combined._added_properties[player].remove(prop)

					if prop not in combined._removed_properties[player]:
						combined._removed_properties[player].append(prop)

			# Merge change_in_jail_moves
			for player, val in change._change_in_jail_moves.iteritems():
				if player not in combined._change_in_jail_moves:
					combined._change_in_jail_moves[player] = 0

				combined._change_in_jail_moves[player] += val

			# Merge change_in_jail_free_count
			for player, val in change._change_in_jail_free_count.iteritems():
				if player not in combined._change_in_jail_free_count:
					combined._change_in_jail_free_count[player] = 0

				combined._change_in_jail_free_count[player] += val

			# Merge is_in_game
			for player, val in change._is_in_game.iteritems():
				combined._is_in_game[player] = val;
