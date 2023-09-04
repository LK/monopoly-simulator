from prop import Property
from groupofchanges import GroupOfChanges
from constants import *


class NonColorProperty(Property):

  # Constants
  # multipliers for owning 1 or 2 utilities
  _UTILITY_MULTIPLIERS = {1: 4, 2: 10}
  _UTILITY = True
  _RAILROAD = False

  def __init__(self, name, price, rents, property_group, size_of_property_group, mortgaged=False):
    super(NonColorProperty, self).__init__(name, price, rents,
                                           property_group, size_of_property_group, mortgaged)

  def _type_of_property(self, state):
    utility_property_group = state.squares[INDEX[WATER_WORKS]].property_group
    railroad_property_group = state.squares[INDEX[READING_RAILROAD]].property_group
    if self.property_group == utility_property_group:
      return NonColorProperty._UTILITY
    elif self.property_group == railroad_property_group:
      return NonColorProperty._RAILROAD
    else:
      raise Exception("This instance is not a proper NonColorProperty")

  def landed(self, player, roll, state, from_card=False):
    owner = state.get_owner(self)
    if owner == player:
      return GroupOfChanges()
    elif owner == state.bank:
      return player.buy_or_deny(self, state)
    else:
      num_owned = owner.property_group_counts[self.property_group]
      rent = self.get_rent(num_owned, roll, state, from_card)
      return player.pay(owner, rent, state)

  # Returns the rent on this property based on the number of properties in this
  # group owned, anding player's roll, and whether they came from a card or not
  def get_rent(self, num_owned, roll, state, from_card):
    if self._type_of_property(state) == NonColorProperty._UTILITY:
      if from_card:
        multiplier = NonColorProperty._UTILITY_MULTIPLIERS[2]
      else:
        multiplier = NonColorProperty._UTILITY_MULTIPLIERS[num_owned]
      return multiplier * roll
    else:
      rent = self.rents[num_owned - 1]
      if from_card:
        return 2 * rent
      else:
        return rent

  def __str__(self):
    s = ""
    s += "Name: %s\n" % (self._name)
    s += "Mortgaged: " + str(self._mortgaged) + "\n"
    return s
