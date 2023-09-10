'''
Author:   Michael Friedman
Created:  8/23/16

Description:
  This class resolves housing conflicts. It takes in a set of housing conditions
  in the form of BuildingRequests and a GameState, and it follows a set of
  rules/procedures to determine when houses/hotels are built, demolished, and
  auctioned. The rules are documented in design/housing-resolver.txt.

  This implementation currently adopts the Convention:
    House builds get priority over hotel demolitions
  (See design/housing-resolver.txt for explanation)
'''

from buildingrequests import BuildingRequests
from enum import Enum
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
import datetime
from constants import *

# Passed to HousingResolver to determines how to resolve house/hotel shortages
class ShortageResolution(Enum):
  AUCTION = 'auction' # houses/hotels are to be auctioned among players
  EQUAL = 'equal' # houses/hotels are to be divided equally among players
  NOOP = 'noop' # no one is to build the remaining houses/hotels

# Constants to represent the type of house/hotel shortage
class ShortageType(Enum):
  HOUSE_BUILD = 'house_build'
  HOTEL_BUILD = 'hotel_build'
  HOTEL_DEMO = 'hotel_demo'

class HousingResolver(object):
  # Takes in a dictionary mapping Players to their BuildingRequests and the
  # current GameState. shortage_resolution is one of ShortageResolution
  def __init__(self, player_building_changes: GroupOfChanges, state, shortage_resolution=ShortageResolution.EQUAL):
    self._player_building_requests = {player: BuildingRequests(changes) for player, changes in player_building_changes.items()}
    self._state = state
    if shortage_resolution not in ShortageResolution:
      raise Exception('Invalid shortage resolution: %s' % shortage_resolution)
    self._shortage_resolution = shortage_resolution

    self._houses_built = 0
    self._hotels_built = 0
    self._houses_demolished = 0
    self._hotels_demolished = 0
    for _, building_requests in self._player_building_requests.items():
      self._houses_built += building_requests.houses_built
      self._hotels_built += building_requests.hotels_built
      self._houses_demolished += building_requests.houses_demolished
      self._hotels_demolished += building_requests.hotels_demolished

  # Building/demolishing

  def _build_houses(self):
    for _, building_requests in self._player_building_requests.items():
      self._state.apply(building_requests.house_builds)

  def _build_hotels(self):
    for _, building_requests in self._player_building_requests.items():
      self._state.apply(building_requests.hotel_builds)

  def _demolish_houses(self):
    for _, building_requests in self._player_building_requests.items():
      self._state.apply(building_requests.house_demolitions)

  def _demolish_hotels(self):
    for _, building_requests in self._player_building_requests.items():
      self._state.apply(building_requests.hotel_demolitions)

  # Optimized method for applying all building changes in one shot, rather than
  # calling each of the preceding methods individually
  def _build_and_demolish_all(self):
    for _, building_requests in self._player_building_requests.items():
      self._state.apply(building_requests.hotel_demolitions)
      self._state.apply(building_requests.house_builds)
      self._state.apply(building_requests.hotel_builds)

  # Shortage tests

  # Returns true if there is a hotel shortage, false if not, based on whether
  # to include hotel demolitions in the calculation

  def _is_hotel_shortage(self, include_hotel_demos=False):
    if not include_hotel_demos:
      return self._hotels_built > self._state.hotels_remaining
    else:
      return self._hotels_built > self._state.hotels_remaining + self._hotels_demolished

  # Returns true if there is a house shortage, false if not, based on whether
  # to include house demolitions and hotel builds in the calculation
  def _is_house_shortage(self, include_house_demos=False, include_hotel_builds=False):
    if not include_house_demos and not include_hotel_builds:
      return self._houses_built > self._state.houses_remaining
    else:
      if include_house_demos and not include_hotel_builds:
        num_houses_to_become_available = self._houses_demolished
      elif not include_house_demos and include_hotel_builds:
        num_houses_to_become_available = NUM_HOUSES_BEFORE_HOTEL * self._hotels_built
      else:
        num_houses_to_become_available = self._houses_demolished + \
          (NUM_HOUSES_BEFORE_HOTEL * self._hotels_built)
      return self._houses_built > self._state.houses_remaining + num_houses_to_become_available

  # Auctioning

  # Returns a list of players who requested house builds

  def _get_players_building_houses(self):
    players_building_houses = []
    for player, building_requests in self._player_building_requests.items():
      if building_requests.houses_built > 0:
        players_building_houses.append(player)
    return players_building_houses

  @staticmethod
  def _auction(num_houses, players, lambda_bid, lambda_extract_bid):
    players_in_auction = dict(list(zip(players, [True] * len(players))))
    properties_to_build_houses_on = self._properties_to_build_houses_on()
    all_changes = []
    for i in range(num_houses):
      highest_bid = 0
      highest_changes = None
      # Run multiple rounds of auctions, eliminating players who have bids less
      # than the highest, until there is only 1 player left or no one bids.
      # Record the game state changes corresponding to the highest bidder.
      while True:
        # Request a bid from each player. Record the player(s) with the highest
        # bid, along with their proposed changes
        highest_bid_for_round = highest_bid
        highest_changes_for_round = dict()
        for player in players:
          if not players_in_auction[player]:
            continue

          goc = lambda_bid(player, highest_bid,
                           properties_to_build_houses_on[player], self._state)
          bid = 0
          for change in goc:
            if len(change.change_in_houses) > 0:
              bid = lambda_extract_bid(change, state)

          if bid < highest_bid:
            players_in_auction[player] = False
          elif bid > highest_bid_for_round:
            highest_bid_for_round = bid
            highest_changes_for_round = {player: goc}
          elif bid == highest_bid_for_round:
            highest_changes_for_round[player] = goc

        # If there is a tie, ask the tied players to bid again, timing their
        # responses. The player with the fastest average time of 3 bids wins
        if len(highest_changes_for_round) > 1:
          fastest_time = 10000
          fastest_player = None
          fastest_goc = None
          for player, goc in highest_changes_for_round.items():
            # TODO: Don't use datetime, better timing solution (timeit doesn't work bc lambda params are out of scope)
            times = []
            for i in range(3):
              start = datetime.datetime.now()
              lambda_bid(player, highest_changes_for_round,
                         properties_to_build_houses_on[player], self._state)
              end = datetime.datetime.now()

              times.append((end - start).total_seconds())

            avg_time = sum(times) / len(times)
            if avg_time < fastest_time:
              fastest_time = avg_time
              fastest_player = player
              fastest_goc = goc

          highest_changes_for_round = {fastest_player: fastest_goc}

        # Update highest bid of the auction so far
        if highest_bid_for_round > highest_bid:
          highest_bid = highest_bid_for_round
          highest_changes = highest_changes_for_round[list(
            highest_changes_for_round.keys())[0]]

        if len(highest_changes_for_round) == 0 or list(players_in_auction.values()).count(True) <= 1:
          break

      all_changes.append(highest_changes)

    return GroupOfChanges.combine(all_changes)

  # Auctions the number of houses among the list of players provided. Returns
  # a GroupOfChanges building the houses for the winners of each auction on
  # their desired properties
  @staticmethod
  def _auction_house_builds(num_houses, players):
    def bid(player, highest_bid, props, state): return player.bid_house_builds(
      highest_bid, props, state)
    def extract_bid(change, state): return change.change_in_cash[state.bank] - list(
      change.changes_in_houses.keys())[0].house_price
    HousingResolver._auction(num_houses, players, bid, extract_bid)

  # Returns a list of players who requested hotel builds
  def _get_players_building_hotels(self):
    players_building_hotels = []
    for player, building_requests in self._player_building_requests.items():
      if building_requests.hotels_built > 0:
        players_building_hotels.append(player)
    return players_building_hotels

  # Auctions the number of hotels among the list of players provided. Returns
  # a GroupOfChanges building the hotels for the winners of each auction on
  # their desired properties
  @staticmethod
  def _auction_hotel_builds(num_hotels, players):
    def bid(player, highest_bid, props, state): return player.bid_hotel_builds(
      highest_bid, props, state)
    def extract_bid(change, state): return change.change_in_cash[state.bank] - list(
      change.changes_in_houses.keys())[0].house_price
    HousingResolver._auction(num_houses, players, bid, extract_bid)

  # Returns a list of players who requested hotel demolitions
  def _get_players_demolishing_hotels(self):
    players_demolishing_hotels = []
    for player, building_requests in self._player_building_requests.items():
      if building_requests.hotels_demolished > 0:
        players_demolishing_hotels.append(player)
    return players_demolishing_hotels

  # Auctions the number of houses (for hotel demolitions) among the list of
  # players provided. Returns a GroupOfChanges building the houses for the
  # winners of each auction on their desired properties
  @staticmethod
  def _auction_hotel_demolitions(num_houses, players):
    def bid(player, highest_bid, props, state): return player.bid_hotel_demolitions(
      highest_bid, props, state)

    def extract_bid(change, state): return change.change_in_cash[state.bank] + list(
      change.changes_in_houses.keys())[0].house_price / 2
    Housing_Resolver._auction(
      int(num_houses / NUM_HOUSES_BEFORE_HOTEL), players, bid, extract_bid)

  # Special case procedure for hotel demolitions

  # Returns true if there are enough houses to demolish the requested number of
  # hotels, false if not, based on whether to include house builds in the
  # calculation
  def _are_enough_houses_for_hotel_demolitions(self, include_house_builds=False):
    num_houses_needed = NUM_HOUSES_BEFORE_HOTEL * self._hotels_demolished
    if not include_house_builds:
      return num_houses_needed <= self._state.houses_remaining
    else:
      return num_houses_needed <= self._state.houses_remaining + self._houses_built

  # Settles the case when players want to demolish hotels, but there are fewer
  # than 4 houses available. Applies the resulting changes
  def _settle_hotel_demolitions(self):
    if self._are_enough_houses_for_hotel_demolitions(include_house_builds=False):
      for _, building_requests in self._player_building_requests.items():
        self._state.apply(building_requests.hotel_demolitions)
    else:
      players_demolishing_hotels = self._get_players_demolishing_hotels()
      if len(players_demolishing_hotels) > 1:
        result = self._handle_shortage(ShortageType.HOTEL_DEMO)
        self._state.apply(result)

  # Convenience Methods

  # Returns a dict mapping players to a list of properties on which they indent to build houses on

  def _properties_to_build_houses_on(self):
    retval = dict()
    for (player, building_request) in self._player_building_requests.items():
      properties = []
      for change in building_request.house_builds:
        properties.append(list(change.change_in_houses.keys())[0])

      retval[player] = properties
    return retval

  def _properties_to_build_hotels_on(self):
    retval = dict()
    for (player, building_request) in self._player_building_requests.items():
      properties = []
      for change in building_request.hotel_builds:
        properties.append(list(change.change_in_houses.keys())[0])

      retval[player] = properties
    return retval

  # Handling shortages

  # Divides houses/hotels equally among the players, excluding any remainder.
  # Returns the resulting building changes.
  def _divide_equally(self, typ: ShortageType, num_units: int, players) -> GroupOfChanges:
    # Reorganize building requests to index houses/hotels built/demo'd by typ
    amount_requested = {
      player: {
        ShortageType.HOUSE_BUILD: self._player_building_requests[player].houses_built,
        ShortageType.HOTEL_BUILD: self._player_building_requests[player].hotels_built,
        ShortageType.HOTEL_DEMO: self._player_building_requests[player].hotels_demolished,
      } for player in players
    }

    # Round robin allocate items to players equally until you reach the amount
    # they requested or run out
    allocation = {player: 0 for player in players}
    remaining = set([i for i in range(len(players))])
    current = 0
    unit_increment = NUM_HOUSES_BEFORE_HOTEL if typ == ShortageType.HOTEL_DEMO else 1
    while len(remaining) > 0 and num_units > 0:
      if current in remaining:
        current_player = players[current]
        allocation[current_player] += 1
        num_units -= unit_increment
        if allocation[current_player] >= amount_requested[current_player][typ]:
          remaining.remove(current)
      current += 1 % len(players)

    # Pass allocated amounts to players to build
    result = []
    for player in players:
      if allocation[player] > 0:
        changes = player.handle_allocated_units(allocation, typ, self._state)
        result.append(changes)
    return GroupOfChanges.combine(result)


  # Handles housing shortages via the shortage resolution method. Returns a
  # the resulting building changes.
  def _handle_shortage(self, typ: ShortageType) -> GroupOfChanges:
    if self._shortage_resolution == ShortageResolution.EQUAL:
      params = {
        ShortageType.HOUSE_BUILD: (self._state.houses_remaining, self._get_players_building_houses()),
        ShortageType.HOTEL_BUILD: (self._state.hotels_remaining, self._get_players_building_hotels()),
        ShortageType.HOTEL_DEMO: (self._state.houses_remaining, self._get_players_demolishing_hotels()),
      }
      num_items, players = params[typ]
      result = self._divide_equally(typ, num_items, players)
    elif self._shortage_resolution == ShortageResolution.AUCTION:
      if typ == ShortageType.HOUSE_BUILD:
        result = HousingResolver._auction_house_builds(
          self._state.houses_remaining, self._get_players_building_houses(), self._state)
      elif typ == ShortageType.HOTEL_BUILD:
        result = HousingResolver._auction_hotel_builds(
          self._state.hotels_remaining, self._get_players_building_hotels(), self._state)
      else:
        result = HousingResolver._auction_hotel_demolitions(
          self._state.houses_remaining, self._get_players_demolishing_hotels(), self._state)
    else:
      result = None
    return result

  # Main resolution procedure

  # Resolves the housing conflicts according to our rules, and applies the
  # changes directly to the GameState

  def resolve(self):
    # 1: Demolish houses
    self._demolish_houses()

    if self._is_hotel_shortage(include_hotel_demos=True):
      # 2: Build houses
      if not self._is_house_shortage():
        self._build_houses()
      else:
        result = self._handle_shortage(ShortageType.HOUSE_BUILD)
        self._state.apply(result)

      # 3: Demolish hotels
      # special case dealt with separately
      self._settle_hotel_demolitions()

      # 4: Build hotels
      if not self._is_hotel_shortage():
        self._build_hotels()
      else:
        result = self._handle_shortage(ShortageType.HOTEL_BUILD)
        self._state.apply(result)

    elif self._is_house_shortage(include_hotel_builds=True):
      # 2: Build hotels
      if not self._is_hotel_shortage():
        self._build_hotels()
      else:
        result = self._handle_shortage(ShortageType.HOTEL_BUILD)
        self._state.apply(result)

      # 3: Build houses
      if not self._is_house_shortage():
        self._build_houses()
      else:
        result = self._handle_shortage(ShortageType.HOUSE_BUILD)
        self._state.apply(result)

      # 4: Demolish hotels
      # special case dealt with separately
      self._settle_hotel_demolitions()

    else:  # no shortage, so order doesn't matter
      self._build_and_demolish_all()
