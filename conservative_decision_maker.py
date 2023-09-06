from buildingrequests import BuildingRequests
from decision_maker import DecisionMaker
from gamestatechange import GameStateChange
from groupofchanges import GroupOfChanges
from notification_changes import NotificationChanges
from constants import *

class ConservativeDecisionMaker(DecisionMaker):
  # cash_reserve_multiple is the multiple of the most expensive
  # rent on the board
  def __init__(self, player, cash_reserve_multiple=1, property_ranking=None):
    super().__init__(player)
    self._cash_reserve_multiple = cash_reserve_multiple
    if property_ranking == None:
      self._property_ranking = DecisionMaker.property_ranking

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
      change = self._build_best_house(state, property_ranking=self._property_ranking, pending_changes=changes)
      if change == None:
        break
      changes = GroupOfChanges.combine([changes, GroupOfChanges(changes=[change])])
    return changes

  # Player will build on the best houses, maintaining enough cash
  # reserve to pay the highest rent times a multiple
  def respond_to_state(self, state):
    changes = None
    cash_delta = 0
    while self._player.cash + cash_delta >= self._cash_reserve_multiple * self._max_rent(state):
      change = self._build_best_house(state, property_ranking=self._property_ranking, pending_changes=changes)
      if change == None:
        break
      changes = GroupOfChanges.combine([changes, GroupOfChanges(changes=[change])])
      cash_delta = changes.net_change_in_cash(self._player) if changes != None else 0
    building_requests = BuildingRequests(house_builds=changes)
    return NotificationChanges(building_requests=building_requests)
