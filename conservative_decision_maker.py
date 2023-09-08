from buildingrequests import BuildingRequests
from decision_maker import DecisionMaker
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges
from notification_changes import NotificationChanges
from prop import Property
from constants import *

class ConservativeDecisionMaker(DecisionMaker):
  # Default order in which player prefers to build on properties
  property_ranking = [
    BOARDWALK,
    PARK_PLACE,

    NEW_YORK_AVENUE,
    ST_JAMES_PLACE,
    TENNESSEE_AVENUE,

    ILLINOIS_AVENUE,
    KENTUCKY_AVENUE,
    INDIANA_AVENUE,

    ATLANTIC_AVENUE,
    VENTNOR_AVENUE,
    MARVIN_GARDENS,

    VIRGINIA_AVENUE,
    ST_CHARLES_PLACE,
    STATES_AVENUE,

    CONNECTICUT_AVENUE,
    ORIENTAL_AVENUE,
    VERMONT_AVENUE,

    BALTIC_AVENUE,
    MEDITERRANEAN_AVENUE,

    PENNSYLVANIA_AVENUE,
    PACIFIC_AVENUE,
    NORTH_CAROLINA_AVENUE,
  ]

  # cash_reserve_multiple is the multiple of the most expensive
  # rent on the board
  def __init__(self, player, cash_reserve_multiple=1, property_ranking=property_ranking):
    super().__init__(player)
    self._cash_reserve_multiple = cash_reserve_multiple
    self._property_ranking = property_ranking

  # Returns the best non-maxed-out property from the preference ranking, while
  # maintaining a cash reserve.
  def _get_best_property_to_build(self, state, pending_changes=None) -> Property:
    for prop_name in self._property_ranking:
      prop_idx = INDEX[prop_name]
      prop = state.squares[prop_idx]
      if state.owns_property_group(self._player, prop.property_group) and not prop.has_hotel(pending_changes=pending_changes) and not state.is_built_ahead_of_group(prop, pending_changes=pending_changes):
        # Only build if we can afford, otherwise stop (and hence save for it)
        delta_cash = pending_changes.net_change_in_cash(self._player) if pending_changes != None else 0
        delta_prop_houses = pending_changes.net_houses_on(prop) if pending_changes != None else 0
        prop_houses = prop.num_houses + delta_prop_houses
        enough_cash = self._player.cash + delta_cash - prop.house_price >= self._cash_reserve_multiple * self._max_rent(state)
        if prop_houses < NUM_HOUSES_BEFORE_HOTEL:
          delta_houses = pending_changes.net_houses() if pending_changes != None else 0
          enough_units = state.houses_remaining + delta_houses > 0
        else:
          delta_hotels = pending_changes.net_hotels() if pending_changes != None else 0
          enough_units = state.hotels_remaining + delta_hotels > 0
        print('prop={prop}, enough_cash={enough_cash}, prop_houses={prop_houses}, enough_units={enough_units}'.format(prop=prop.name, enough_cash=enough_cash, prop_houses=prop_houses, enough_units=enough_units))
        if not enough_units:
          continue
        elif enough_cash:
          return prop
        else:
          break
    return None

  # Player doesnt bid
  def bid_house_builds(self, player, highest_bid, props_to_build_on, state):
    return None

  # Player doesnt bid
  def bid_hotel_builds(self, player, highest_bid, props_to_build_on, state):
    return None

  # Player doesnt bid
  def bid_hotel_demolitions(self, player, highest_bid, props_to_demolish_on, state):
    return None

  # Player does not revise their hotel demolitions
  def revise_hotel_demolitions(self, player, original_hotel_demolitions, state):
    return None

  # Players denies all trades
  def will_trade(self, player, proposal, state):
    return False

  # Player will build on the best properties that they can afford
  def build_allocated_houses(self, house_allocation, state):
    changes = None
    num_houses = house_allocation[self._player]
    for _ in range(num_houses):
      prop = self._get_best_property_to_build(state, pending_changes=changes)
      if prop == None:
        break
      change = GameStateChange.build(prop, state)
      changes = GroupOfChanges.combine([changes, GroupOfChanges(changes=[change])])
    return changes

  # Player will build on the best houses, maintaining enough cash
  # reserve to pay the highest rent times a multiple
  def respond_to_state(self, state):
    prop = None
    changes = None
    while True:
      prop = self._get_best_property_to_build(state, pending_changes=changes)
      if prop == None:
        break
      change = GameStateChange.build(prop, state)
      changes = GroupOfChanges.combine([changes, GroupOfChanges(changes=[change])])
    print('changes: houses={houses}, hotels={hotels}'.format(houses=changes.net_houses(), hotels=changes.net_hotels()))
    building_requests = BuildingRequests(house_builds=changes)
    return NotificationChanges(building_requests=building_requests)
