from prop import Property
from groupofchanges import GroupOfChanges
from constants import *

class ColorProperty(Property):
  def __init__(self, name, price, rents, property_group, size_of_property_group, mortgaged=False, house_price=0, num_houses=0):
    super(ColorProperty, self).__init__(name, price, rents, property_group, size_of_property_group, mortgaged)
    self._num_houses = num_houses
    self._house_price = house_price

  def landed(self, player, roll, state):
    owner = state.get_owner(self)
    if owner == player:
      return GroupOfChanges()
    elif owner == state.bank:
      return player.buy_or_deny(self, state)
    else:
      rent = self.get_rent_with(self.num_houses, state)
      return player.pay(owner, rent, state)

  # Getters

  @property
  def num_houses(self):
    return self._num_houses

  @property
  def house_price(self):
    return self._house_price

  # Setters

  @num_houses.setter
  def num_houses(self, num_houses):
    self._num_houses = num_houses

  # Other methods

  def get_rent_with(self, num_houses, state):
    owner = state.get_owner(self)
    if owner.is_property_group_complete(self.property_group):
      if num_houses > 0:
        return self.rents[num_houses]
      else:
        return 2 * self.rents[0]  # rent doubles if property group is complete
    return self.rents[0]

  def build(self, qty):
    self.num_houses += qty

  def demolish(self, qty):
    self.num_houses -= qty

  def has_hotel(self):
    return self.num_houses == NUM_HOUSES_BEFORE_HOTEL + 1

  def __str__(self):
    s = ""
    s += "Name: %s\n" % (self._name)
    s += "Num houses: %d\n" % (self._num_houses)
    s += "Mortgaged: " + str(self._mortgaged) + "\n"
    return s
    
