from collections import Counter

class Player(object):
	# TODO: Proper default decision maker
	# TODO: Initialize property_group_counts so that each property group maps to a count of 0
	def __init__(self, position=0, cash=1500, props=[], property_group_counts={}, decision_maker=None, jail_free_count=0, jail_moves=0, is_in_game=True):
		self._position					= position
		self._cash 							= cash
		self._decision_maker		= decision_maker
		self._jail_free_count		= jail_free_count
		self._jail_moves				= jail_moves
		self._is_in_game				= is_in_game
		self._props 						= props

		# Compute property group count
		groups = [prop.property_group for prop in props]
		self._property_group_counts = Counter(groups)

	
	def copy(self):
		return Player(position=self._position, cash=self._cash, props=self._props, property_group_counts=self._property_group_counts, decision_maker=self._decision_maker, jail_free_count=self._jail_free_count, jail_moves=self._jail_moves, is_in_game=self._is_in_game)



	# Getters

	@property
	def position(self):
		return self._position

	@property
	def cash(self):
		return self._cash

	@property
	def props(self):
		return self._props

	@property
	def property_group_counts(self):
		return self._property_group_counts
	
	@property
	def decision_maker(self):
		return self._decision_maker
	
	@property
	def jail_free_count(self):
		return self._jail_free_count

	@property
	def jail_moves(self):
		return self._jail_moves

	@property
	def is_in_game(self):
		return self._is_in_game

	

	# Setters
	
	@position.setter
	def position(self, position):
		self._position = position
	
	@cash.setter
	def cash(self, cash):
		self._cash = cash

	@jail_free_count.setter
	def jail_free_count(self, jail_free_count):
		self._jail_free_count = jail_free_count

	@jail_moves.setter
	def jail_moves(self, jail_moves):
		self._jail_moves = jail_moves
	
	@is_in_game.setter
	def is_in_game(self, is_in_game):
		self._is_in_game = is_in_game



	# Other methods

	# Getter-esque methods

	def is_property_group_complete(self, property_group):
		# If the player does not own any of these properties, return False
		if self.property_group_counts[property_group] == 0:
			return False

		# Find the first property in the group and check the total size of the 
		# property group
		for prop in self.properties:
			if prop.property_group == property_group:
				return prop.size_of_property_group == self.property_group_counts[property_group]

	def is_in_jail(self):
		return self._jail_moves > 0



	# Setter-esque methods

	# Adds the list of properties and updates the corresponding property group counts
	def add_properties(self, added_properties):
		self.props.extend(added_properties)
		for prop in added_properties:
			self._property_group_counts[prop.property_group] += 1

	# Removes the list of properties and updates the corresponding property group counts
	def remove_properties(self, removed_properties):
		for prop in removed_properties:
			self.props.remove(prop)
			self._property_group_counts[prop.property_group] -= 1

	def eliminate(self):
		self._is_in_game = False



	# DecisionMaker interactions

	def buy_or_deny(self, prop, state):
		return self.decision_maker.buy_or_deny(self, prop, state)

	def pay(self, player, amount, state):
		return self.decision_maker.pay(self, player, amount, state)

	def bid_house_builds(self, highest_bid, props_to_build_on, state):
		return self.decision_maker.bid_house_builds(self, highest_bid, props_to_build_on, state)

	def bid_hotel_builds(self, highest_bid, props_to_build_on, state):
		return self.decision_maker.bid_hotel_builds(self, highest_bid, props_to_build_on, state)

	def bid_hotel_demolitions(self, highest_bid, props_to_demolish_on, state):
		return self.decision_maker.bid_hotel_demolitions(self, highest_bid, props_to_demolish_on, state)

	def will_trade(self, proposal, state):
		return self.decision_maker.will_trade(self, proposal, state)

	def respond_to_state(self, new_state):
		return self.decision_maker.respond_to_state(self, new_state)

	def revise_hotel_demolitions(self, original_hotel_demolitions, state):
		return self.decision_maker.revise_hotel_demolitions(self, original_hotel_demolitions, state)
