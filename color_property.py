from property import Property
from groupofchanges import GroupOfChanges

class ColorProperty(Property):
	# Constants
	NUM_HOUSES_BEFORE_HOTEL = 4

	def __init__(self, name, price, rents, property_group, size_of_property_group, house_price, mortgaged=False, num_houses=0):
		super(ColorProperty, self).__init__(name, price, rents, property_group, size_of_property_group, mortgaged)
		self._num_houses = num_houses
		self._house_price = house_price

	def get_rent_with(self, num_houses, state):
		owner = state.get_owner(self)
		if owner.is_property_group_complete(self.property_group):
			if num_houses > 0:
				return self.rents[num_houses]
			else:
				return 2 * self.rents[0]  # rent doubles if property group is complete
		return self.rents[0]

	def landed(self, player, roll, state):
		owner = state.get_owner(self)
		if owner == player:
			return GroupOfChanges()

		rent = self.get_rent_with(self.num_houses, state)
		return player.pay(owner, rent, state)

	def build(self, qty):
		self.num_houses += qty

	def demolish(self, qty):
		self.num_houses -= qty

	def demolish_all(self):
		self.num_houses = 0

	@property
	def num_houses(self):
		return self._num_houses
	
	@num_houses.setter
	def num_houses(self, num_houses):
		self._num_houses = num_houses

	@property
	def house_price(self):
		return self._house_price
		