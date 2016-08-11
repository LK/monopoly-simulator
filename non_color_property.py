from property import Property
from gamestatechange import GameStateChange

class NonColorProperty(Property):
	def __init__(self):
		pass

	def landed(self, player, state):
		owner = state.get_owner(self)
		if owner == player:
			return GameStateChange()

		num_owned = owner.property_group_count()[self.property_group]
		return player.pay(owner, self.rents[num_owned], state)

