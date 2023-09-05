'''
Author:   Michael Friedman
Created:  8/25/16

Description:
  This class holds a set of building requests from a player. It contains a
  GroupOfChanges for each of the following:
    - House Builds
    - Hotel Builds
    - House Demolitions
    - Hotel Demolitions
  BuildingRequests are kept separate from other changes a player wishes to make
  to the game so that the HousingResolver can settle building conflicts before
  applying them.
'''

class BuildingRequests(object):

  # Construct from four GroupOfChanges objects, one for each category of
  # building changes
  def __init__(self, house_builds=None, hotel_builds=None, house_demolitions=None, hotel_demolitions=None):
    self._house_builds = house_builds
    self._hotel_builds = hotel_builds
    self._house_demolitions = house_demolitions
    self._hotel_demolitions = hotel_demolitions

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
