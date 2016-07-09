from collections import Counter

class Player(object):
	# TODO: Proper default decision maker
	def __init__(self, position=0, cash=1500, props=[], decision_maker=None, jail_free_count=0, jail_moves=0, is_in_game=True):
		self._position					= position
		self._cash 							= cash
		self._decision_maker		= decision_maker
		self._jail_free_count		= jail_free_count
		self._jail_moves				= jail_moves
		self._is_in_game				= is_in_game

		# Use the setter so property_group_count is updated
		self.props 				= props
	
	# Properties

	@property
	def position(self):
		return self._position
	
	@position.setter
	def position(self, position):
		self._position = position

	@property
	def cash(self):
		return self._cash
	
	@cash.setter
	def cash(self, cash):
		self._cash = cash

	@property
	def props(self):
		return self._props
	
	@props.setter
	def props(self, props):
		self._props = props
		
		# When setting the properties, recompute property group count
		groups = [prop.property_group for prop in props]
		self._property_group_count = Counter(groups)

	def add_properties(self, added_properties):
		self.properties.extend(added_properties)
		for prop in added_properties:
			self._property_group_count[prop.property_group] += 1

	def remove_properties(self, removed_properties):
		for prop in removed_properties:
			self.properties.remove(prop)
			self._property_group_count[prop.property_group] -= 1

	@property
	def property_group_count(self):
		return self._property_group_count

	def is_property_group_complete(self, property_group):
		# If the player does not own any of these properties, return False
		if self.property_group_count[property_group] == 0:
			return False

		# Find the first property in the group and check the total size of the 
		# property group
		for prop in self.properties:
			if prop.property_group == property_group:
				return prop.size_of_property_group == self.property_group_count[property_group]

	@property
	def decision_maker(self):
		return self._decision_maker
	
	@property
	def jail_free_count(self):
		return self._jail_free_count
	
	@jail_free_count.setter
	def jail_free_count(self, jail_free_count):
		self._jail_free_count = jail_free_count

	@property
	def jail_moves(self):
		return self._jail_moves

	def is_in_jail(self):
		return self.jail_moves > 0
	
	@jail_moves.setter
	def jail_moves(self, jail_moves):
		self._jail_moves = jail_moves

	@property
	def is_in_game(self):
		return self._is_in_game
	
	@is_in_game.setter
	def is_in_game(self, is_in_game):
		self._is_in_game = is_in_game

	def eliminate(self):
		self.is_in_game = False

	# DecisionMaker interactions

	def buy_or_deny(self, prop, state):
		return self.decision_maker.buy_or_deny(prop, state)

	def pay(self, player, amount, state):
		return self.decision_maker.pay(player, amount, state)

	def bid(self, highest_bid, state):
		return self.decision_maker.bid(highest_bid, state)

	def will_trade(self, proposal):
		return self.decision_maker.will_trade(proposal)

	def notify(self, new_state):
		return self.decision_maker.notify(new_state)
