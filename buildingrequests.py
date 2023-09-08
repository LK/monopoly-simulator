'''
Author:   Michael Friedman
Created:  8/25/16

This class holds a set of building requests from a player. It contains a
GroupOfChanges for each of the following:
  - House Builds
  - Hotel Builds
  - House Demolitions
  - Hotel Demolitions
BuildingRequests should be constructed whenever there are building-related
changes, and they are passed to the HousingResolver so it can settle building
conflicts before applying them.
'''

from collections import defaultdict
from constants import *
from groupofchanges import GroupOfChanges

class BuildingRequests(object):
  # changes should consist of only building-related changes
  def __init__(self, changes: GroupOfChanges):
    # Validate
    for change in changes:
      if len(change.change_in_houses) != 1:
        raise Exception('Invalid change: does not build or demo on one property: {change}'.format(change=change.change_in_houses))

    # Separate changes into house and hotel builds/demos
    changes_map = defaultdict(lambda: [])
    for change in changes:
      for prop in change.change_in_houses:
        changes_map[prop].append(change)

    house_builds = []
    hotel_builds = []
    house_demolitions = []
    hotel_demolitions = []
    for prop, changes_list in changes_map.items():
      group = GroupOfChanges(changes_list)
      delta_houses = group.net_houses_on(prop)
      if not prop.has_hotel() and prop.has_hotel(pending_changes=group):
        hotel_builds.append(group)
      elif prop.has_hotel() and prop.num_houses + delta_houses == NUM_HOUSES_BEFORE_HOTEL:
        hotel_demolitions.append(group)
      elif delta_houses > 0:
        house_builds.append(group)
      else:
        house_demolitions.append(group)

    self._house_builds = GroupOfChanges.combine(house_builds)
    self._hotel_builds = GroupOfChanges.combine(hotel_builds)
    self._house_demolitions = GroupOfChanges.combine(house_demolitions)
    self._hotel_demolitions = GroupOfChanges.combine(hotel_demolitions)

    # Calculate integer quantities of houses/hotels built and demolished
    self._houses_built = self._house_builds.houses_built() if self._house_builds != None else 0
    self._hotels_built = self._hotel_builds.hotels_built() if self._hotel_builds != None else 0
    self._houses_demolished = self._house_demolitions.houses_demolished() if self._house_demolitions != None else 0
    self._hotels_demolished = self._hotel_demolitions.hotels_demolished() if self._hotel_demolitions != None else 0

  # Getters

  @property
  def house_builds(self):
    return self._house_builds

  @property
  def hotel_builds(self):
    return self._hotel_builds

  @property
  def house_demolitions(self):
    return self._house_demolitions

  @property
  def hotel_demolitions(self):
    return self._hotel_demolitions

  @property
  def houses_built(self):
    return self._houses_built

  @property
  def hotels_built(self):
    return self._hotels_built

  @property
  def houses_demolished(self):
    return self._houses_demolished

  @property
  def hotels_demolished(self):
    return self._hotels_demolished
