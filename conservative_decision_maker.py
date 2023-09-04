from decision_maker import DecisionMaker
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges
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
  def respond_to_state(self, player, state):
    changes = []
    while player.cash >= self._cash_reserve_multiple * self._max_rent(state):
      for prop_name in self._property_ranking:
        prop_idx = INDEX[prop_name]
        prop = state.squares[prop_idx]
        if self._can_build(prop, state):
          changes.append(GameStateChange.build(prop, state))
          break
    return GroupOfChanges(changes=changes)
