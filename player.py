from default_decision_maker import DefaultDecisionMaker
from constants import *

class Player(object):

	@staticmethod
	def _initialize_property_group_counts():
		groups = [PURPLE, LIGHT_BLUE, PINK, ORANGE, RED, YELLOW, GREEN, DARK_BLUE, RAILROAD, UTILITY]
		property_group_counts = {}
		for group in groups:
			property_group_counts[group] = 0
		return property_group_counts

	def __init__(self, position=0, cash=1500, props=[], decision_maker=DefaultDecisionMaker(), jail_free_count=0, jail_moves=0, is_in_game=True, name=''):
		self._position							= position
		self._cash 									= cash
		self._props 								= []
		self._property_group_counts = Player._initialize_property_group_counts()
		for prop in props:
			self._props.append(prop)
			self._property_group_counts[prop.property_group] += 1
		self._decision_maker				= decision_maker
		self._jail_free_count				= jail_free_count
		self._jail_moves						= jail_moves
		self._is_in_game						= is_in_game
		self._name 									= name


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

	@property
	def name(self):
		return self._name


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
		for prop in self.props:
			if prop.property_group == property_group:
				return prop.size_of_property_group == self.property_group_counts[property_group]

	def is_in_jail(self):
		return self._jail_moves > 0



	# Setter-esque methods

	# Adds the list of properties and updates the corresponding property group counts
	def add_props(self, added_props):
		self._props += added_props
		for prop in added_props:
			group = prop.property_group
			if group in list(self._property_group_counts.keys()):
				self._property_group_counts[group] += 1
			else:
				self._property_group_counts[group] = 1

	# Removes the list of properties and updates the corresponding property group
	# counts
	def remove_props(self, removed_props):
		# Construct a new list of properties excluding the removed ones
		new_props = []
		for prop in self._props:
			if prop not in removed_props:
				new_props.append(prop)
			else:
				# Adjust the removed properties' property group counts
				group = prop.property_group
				self._property_group_counts[group] -= 1
		self._props = new_props

	def eliminate(self):
		self._is_in_game = False

	def __str__(self):
		s = ""
		s += self._name + "\n"
		s += "Position: %d\n" % (self._position)
		s += "Cash: %d\n" % (self._cash)

		s += "Props:\n"
		for prop in self._props:
			s += prop.name + ", "
		s += "\n"

		s += "Property group counts:\n"
		for group, count in self._property_group_counts.items():
			s += str(group) + ": " + str(count) + "\n"

		s += "Jail free count: %d\n" % (self._jail_free_count)
		s += "Jail moves: %d\n" % (self._jail_moves)
		s += "Is in game: " + str(self._is_in_game) + "\n"
		return s


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
