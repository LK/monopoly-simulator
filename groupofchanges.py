'''
Author:   Lenny Khazan & Michael Friedman
Created:

Description:
  This class contains a list of GameStateChanges that should be applied as a unit.
  This is designed with the convention that the GameStateChanges will be applied
  in the order given during initialization.
'''


class GroupOfChanges(object):

  # Takes in a list of GameStateChanges to be applied together as a unit
  def __init__(self, changes=None):
    self._changes = []
    if changes != None:
      for change in changes:
        self._changes.append(change)

  # Returns an iterator so this object becomes iterable
  def __iter__(self):
    return iter(self._changes)

  # Concatenates a list of GroupOfChanges objects, returns a new GroupOfChanges
  @staticmethod
  def combine(groups_of_changes):
    combined_group_of_changes = []
    for group_of_changes in groups_of_changes:
      if group_of_changes != None:
        combined_group_of_changes += group_of_changes
    return GroupOfChanges(combined_group_of_changes)

  def houses_built(self):
    houses = 0
    for change in self._changes:
      if change.change_in_houses_remaining < 0:
        houses += -change.change_in_houses_remaining

    return houses

  def hotels_built(self):
    hotels = 0
    for change in self._changes:
      if change.change_in_hotels_remaining < 0:
        hotels += -change.change_in_hotels_remaining
    return hotels

  def houses_demolished(self):
    houses = 0
    for change in self._changes:
      if change.change_in_houses_remaining > 0:
        houses += change.change_in_houses_remaining
    return houses

  def hotels_demolished(self):
    hotels = 0
    for change in self._changes:
      if change.change_in_hotels_remaining > 0:
        hotels += change.change_in_hotels_remaining
    return hotels

  def net_houses_on(self, prop):
    return sum([change.change_in_houses[prop] if prop in change.change_in_houses else 0
                for change in self._changes])

  def net_houses(self):
    return sum([change.change_in_houses_remaining for change in self._changes])

  def net_hotels(self):
    return sum([change.change_in_hotels_remaining for change in self._changes])

  def net_change_in_cash(self, player):
    return sum([change.change_in_cash[player] if player in change.change_in_cash else 0
                for change in self._changes])

  def new_owner(self, prop):
    owner = None
    for change in self._changes:
      for player, props in change.added_props:
        if prop in props:
          owner = player
    return owner
