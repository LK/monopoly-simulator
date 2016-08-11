from property import Property
from gamestatechange import GameStateChange

class ColorProperty(Property):
	def __init__(self, num_houses):
		self._num_houses = num_houses

	def landed(self, player, state):
		owner = state.get_owner(self)
		if owner == player:
			return GameStateChange()

		return player.pay(owner, self.get_rent_with(self.num_houses, state), state)

	def get_rent_with(self, num_houses, state):
		if num_houses == 0:
			if state.get_owner(self).is_property_group_complete(self.property_group):
				# If property group is complete but no houses are built, rent doubles
				return self.rents[0] * 2
			else:
				return self.rents[0]
		else:
			# Assume that if houses are built the property group is complete
			return self.rents[num_houses]

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