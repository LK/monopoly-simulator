from square import Square

class GameStateChange(object):
	def __init__(self, change_in_cash={}, new_position={}, added_props={}, removed_props={}, change_in_jail_moves={}, change_in_jail_free_count={}, is_in_game={}, change_in_houses={}, is_mortgaged={}):
		self._change_in_cash            = change_in_cash
		self._new_position              = new_position
		self._added_props          			= added_props
		self._removed_props        			= removed_props
		self._change_in_jail_moves			= change_in_jail_moves
		self._change_in_jail_free_count	= change_in_jail_free_count
		self._is_in_game								= is_in_game
		self._change_in_houses					= change_in_houses
		self._is_mortgaged							= is_mortgaged

	@property
	def change_in_cash(self):
		return self._change_in_cash
		
	@property
	def new_position(self):
		return self._new_position
		
	@property
	def added_props(self):
		return self._added_props
	
	@property
	def removed_props(self):
		return self._removed_props
	
	@property
	def change_in_jail_moves(self):
		return self._change_in_jail_moves

	@property
	def change_in_jail_free_count(self):
		return self._change_in_jail_free_count

	@property
	def is_in_game(self):
		return self._is_in_game
	
	@property
	def change_in_houses(self):
		return self._change_in_houses
	
	@property
	def is_mortgaged(self):
		return self._is_mortgaged
	
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

			# Merge added_props
			for player, props in change._added_props.iteritems():
				if player not in combined._added_props:
					combined._added_props[player] = []
				
				for prop in props:
					if prop in combined._removed_props[player]:
						combined._removed_props[player].remove(prop)

					if prop not in combined._added_props[player]:
						combined._added_props[player].append(prop)

			# Merge removed_props
			for player, props in change._removed_props.iteritems():
				if player not in combined._removed_props:
					combined._removed_props[player] = []
				
				for prop in props:
					if prop in combined._added_props[player]:
						combined._added_props[player].remove(prop)

					if prop not in combined._removed_props[player]:
						combined._removed_props[player].append(prop)

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
			for color_prop, change_in_houses in change._change_in_houses.iteritems():
				if player not in combined._change_in_houses:
					combined._change_in_houses[color_prop] = 0
				combined._change_in_houses[color_prop] += change_in_houses

			# Merge is_mortgaged
			for prop, is_mortgaged in change._is_mortgaged.iteritems():
				combined._is_mortgaged[prop] = is_mortgaged

		return combined

	def total_houses_built(self):
		return sum(self.change_in_houses.values())

		# -------------

	@staticmethod
	def transfer_money(player_from, player_to, amount):
		return GameStateChange(change_in_cash={player_from: -amount, player_to: +amount})

	@staticmethod
	def change_position(player, new_position, bank):
		if player.position >= (Square.INDEX['go']-12) % 40 and new_position < (Square.INDEX['go']-12) % 40:
			return GameStateChange(new_position={player: new_position}, change_in_cash:{player: 200, bank: -200})
		else:
			return GameStateChange(new_position={player: new_position})

	@staticmethod
	def buy_property(player, prop, bank, mortgaged=False):
		return GameStateChange(added_props={player: [prop]}, change_in_cash={player: -prop.price, bank: prop.price})

	@staticmethod
	def transfer_property(player_from, player_to, prop):
		return GameStateChange(removed_props={player_from: [prop]}, added_props={player_to: [prop]})

	@staticmethod
	def mortgage(prop, bank):
		return GameStateChange(is_mortgaged={prop: True}, change_in_cash={player: prop.price/2, bank: -prop.price/2})
	
	@staticmethod
	def unmortgage(prop, bank):
		return GameStateChange(is_mortgaged={prop: False}, change_in_cash={player: -prop.price/2 * 1.1, bank: prop.price/2 * 1.1})
	
	@staticmethod
	def build_house(prop, bank):
		return GameStateChange(change_in_houses={prop: 1}, change_in_cash={player: -prop.house_price, bank: prop.house_price})
	
	@staticmethod
	def build_hotel(property):
		return GameStateChange(change_in_houses={prop: 1}, change_in_cash={player: -prop.house_price, bank: prop.house_price})

	@staticmethod
	def demolish_house(property):
		return GameStateChange(change_in_houses={prop: -1}, change_in_cash={player: prop.house_price/2, bank: -prop.house_price/2})

	@staticmethod
	def demolish_hotel(property):
		return GameStateChange(change_in_houses={prop: -1}, change_in_cash={player: prop.house_price/2, bank: -prop.house_price/2})

	@staticmethod
	def send_to_jail(player):
		return GameStateChange(new_position={player: Square.INDEX['jail']}, change_in_jail_moves={player: 3})

	@staticmethod
	def decrement_in_jail_moves(player):
		return GameStateChange(change_in_jail_moves={player: -1})

	@staticmethod
	def leave_jail(player):
		return GameStateChange(change_in_jail_moves={player: -player.jail_moves})

	@staticmethod
	def increment_jail_card_count(player):
		return GameStateChange(change_in_jail_free_count={player: 1})

	@staticmethod
	def decrement_jail_card_count(player):
		return GameStateChange(change_in_jail_free_count={player: -1})

	@staticmethod
	def eliminate(player_eliminated, player_eliminator):
		return GameStateChange(is_in_game={player_eliminated: False}, change_in_cash={player_eliminated: -player_eliminated.cash, player_eliminator: player_eliminated.cash}, removed_props={player_eliminated: player_eliminated.props}, added_props={player_eliminator: player_eliminated.props})
