from property import Property
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges
from square import Square

class NonColorProperty(Property):

	# Constants
	_UTILITY_MULTIPLIERS = { 1: 4, 2: 10 } # multipliers for owning 1 or 2 utilities

	def __init__(self, name, price, rents, property_group, size_of_property_group, mortgaged=False):
		super(NonColorProperty, self).__init__(name, price, rents, property_group, size_of_property_group, mortgaged)

	def landed(self, player, roll, state):
		owner = state.get_owner(self)
		if owner == player:
			return GroupOfChanges()
		elif owner == state.bank:
			return player.buy_or_deny(self, state)
		else:
			num_owned = owner.property_group_count[self.property_group]
			rent = self.get_rent(num_owned, roll, state)
			return player.pay(owner, rent, state)

	# Returns the rent on this property based on the number of properties in this
	# group owned and the landing player's roll
	def get_rent(self, num_owned, roll, state):
		water_works				= state.props[Square.INDEX[Square.WATER_WORKS]]
		electric_company	= state.props[Square.INDEX[Square.ELECTRIC_COMPANY]]
		if self == water_works or self == electric_company:
			multiplier = NonColorProperty._UTILITY_MULTIPLIERS[num_owned]
			return multiplier * roll
		else:
			return self.rents[num_owned]
