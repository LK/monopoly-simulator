from buildingrequests import BuildingRequests
from decision_maker import DecisionMaker
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges
from notification_changes import NotificationChanges
from constants import *

class ConservativeDecisionMaker(DecisionMaker):
  # Order in which player will build on properties
  property_ranking = [
    BOARDWALK,
    PARK_PLACE,

    NEW_YORK_AVENUE,
    ST_JAMES_PLACE,
    TENNESSEE_AVENUE,

    INDIANA_AVENUE,
    KENTUCKY_AVENUE,
    ILLINOIS_AVENUE,

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

  # Player will build houses only if they have enough cash
  # reserve to pay the highest rent times a multiple, and they
  # build on the best properties first.
  def respond_to_state(self, state):
    changes = None
    cash_delta = 0
    while self._player.cash + cash_delta >= self._cash_reserve_multiple * self._max_rent(state):
      can_build = False
      # print('new_cash={cash}, max_rent={max_rent}'.format(cash=self._player.cash+cash_delta, max_rent=self._cash_reserve_multiple * self._max_rent(state)))
      for prop_name in self._property_ranking:
        prop_idx = INDEX[prop_name]
        prop = state.squares[prop_idx]
        # print('prop={prop}'.format(prop=str(prop)))
        # print('can_build={can_build}'.format(can_build=self._can_build(prop, state)))
        if state.can_build(self._player, prop, pending_changes=changes):
          change = GameStateChange.build(prop, state)
          changes = GroupOfChanges.combine([changes, GroupOfChanges(changes=[change])])
          can_build = True
          break

      cash_delta = changes.net_change_in_cash(self._player) if changes != None else 0
      if not can_build:
        break

    building_requests = BuildingRequests(house_builds=changes)
    return NotificationChanges(building_requests=building_requests)
