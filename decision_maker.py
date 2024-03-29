from color_property import ColorProperty
from housingresolver import ShortageType
from non_color_property import NonColorProperty
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from roll import Roll
from random import randint
from constants import *
from typing import Tuple

# TODO: Come up with better DeicisionMaker policies that make every possible state of the game reachable


class DecisionMaker(object):
  def __init__(self, player):
    self._player = player

  def _can_mortgage_property(self, prop, state):
    if isinstance(prop, NonColorProperty):
      return True

    for prop in state.get_property_group(prop.property_group):
      if prop.num_houses > 0:
        return False

    return True

  def _demolish_from_property_group(self, prop, state):
    max_houses = 0
    max_houses_prop = None
    for prop in state.get_property_group(prop.property_group):
      if prop.num_houses > max_houses:
        max_houses = prop.num_houses
        max_houses_prop = prop

    if max_houses_prop != None:
      return GameStateChange.demolish(max_houses_prop, state)
    else:
      return None

  def _max_rent(self, state):
    max_rent = 0
    for prop in state.squares:
      if isinstance(prop, ColorProperty):
        max_rent = max(max_rent, prop.get_rent_with(prop.num_houses, state))
      elif isinstance(prop, NonColorProperty):
        owner = state.get_owner(prop)
        num_owned = owner.property_group_counts[prop.property_group]
        max_rent = max(max_rent, prop.get_rent(
          num_owned, Roll.max_value(), state, from_card=False))
    return max_rent

  def _return_jail_free_card(self, player, state):
    # Pick a Deck to return the jail free card to randomly
    # TODO: Need a better way of picking a Deck to return the jail free card to
    if (randint(0, 1) == 0):
      deck = state.decks[CHANCE_CARD]
    else:
      deck = state.decks[COMMUNITY_CHEST_CARD]
    use_card = GameStateChange.decrement_jail_card_count(player, deck)
    leave_jail = GameStateChange.leave_jail(player)
    return GroupOfChanges(changes=[use_card, leave_jail])

  # By default, player buys the property if he has enough cash on hand.
  # Otherwise he passes
  def buy_or_deny(self, player, prop, state):
    if player.cash >= prop.price:
      return GroupOfChanges(changes=[GameStateChange.buy_property(prop, player, state.bank)])
    else:
      return GroupOfChanges()

  # By default, the player attempts to pay all cash, then resorts to mortgaging
  # properties, then resorts to demolishing houses. If all of these fail, then
  # he loses
  def pay(self, player_from, player_to, amount, state, cause=None):
    transfer_money = GameStateChange.transfer_money(
      player_from, player_to, amount, cause=cause)
    changes = []

    # Try paying all cash first
    if player_from.cash >= amount:
      changes.append(transfer_money)
      return GroupOfChanges(changes=changes)

    # Mortgage properties until the difference is paid off
    difference = amount - player_from.cash
    i = 0
    while difference > 0 and i < len(player_from.props):
      prop = player_from.props[i]
      i += 1
      if not prop.mortgaged and self._can_mortgage_property(prop, state):
        mortgage = GameStateChange.mortgage(prop, state)
        changes.append(mortgage)
        difference -= mortgage.change_in_cash[player_from]

    if difference <= 0:
      changes.append(transfer_money)
      return GroupOfChanges(changes=changes)

    # Mortgaging was not enough. Demolish until the difference is paid off
    i = 0
    while difference > 0 and i < len(player_from.props):
      prop = player_from.props[i]
      i += 1
      if isinstance(prop, ColorProperty) and prop.num_houses > 0:
        demolition = self._demolish_from_property_group(
          prop, state)
        if demolition != None:
          changes.append(demolition)
          difference -= demolition.change_in_cash[player_from]

    if difference <= 0:
      changes.append(transfer_money)
      return GroupOfChanges(changes=changes)

    # Player cannot pay it off, so he loses
    return GroupOfChanges(changes=[GameStateChange.eliminate(player_from, player_to, state)])

  # Call when there is an auction for houses due to housing shortage. Each
  # call represents a single round of bidding for a single house. player is the
  # current player, highest_bid is the highest bid so far, and props_to_build_on
  # is the list of properties that the player originally requested to build on,
  # which triggered a housing shortage. Returns a GroupOfChanges representing
  # the player paying their bid and building the house, which will be applied if
  # they win.
  #
  # By default, player bids half their cash to build on the first property in
  # their list.
  def bid_house_builds(self, player, highest_bid, props_to_build_on, state):
    bid = player.cash / 2
    prop_to_build_on = props_to_build_on[0]
    house_build = GameStateChange.build(prop_to_build_on, state)
    return GroupOfChanges([house_build])

  # Call when there is an auction for hotels due to hotel shortage.
  # Analogous to bid_house_builds.
  def bid_hotel_builds(self, player, highest_bid, props_to_build_on, state):
    bid = player.cash / 2
    prop_to_build_on = props_to_build_on[0]
    hotel_build = GameStateChange.build(prop_to_build_on, state)
    return GroupOfChanges([hotel_build])

  # Call when there is an auction for hotel demolitions due to house
  # shortage (since demolishing hotels requires houses to downgrade to).
  # Analogous to bid_house_builds.
  def bid_hotel_demolitions(self, player, highest_bid, props_to_demolish_on, state):
    bid = player.cash / 2
    prop_to_demolish_on = props_to_demolish_on[0]
    hotel_demolition = GameStateChange.demolish(prop_to_demolish_on, state)
    house_builds = [GameStateChange.build(
      prop_to_demolish_on, state)] * NUM_HOUSES_BEFORE_HOTEL
    return GroupOfChanges([hotel_demolition] + house_builds)

  # Call when the allocation of houses/hotels among players has been determined
  # after resolving a housing shortage. house_allocation is a dict {player: num_units}
  # representing the allocation. Returns a GroupOfChanges representing the
  # player building/demo'ing the units allocated to them on their desired
  # properties.
  #
  # By default, player doesn't build.
  def handle_allocated_units(self, house_allocation, typ: ShortageType, state) -> GroupOfChanges:
    return None

  # By default, players deny all trades
  def will_trade(self, player, proposal, state):
    return False

  # By default, player will only use a jail free card if they're in jail.
  # Returns 2 GroupOfChanges: the first consists of only non-building changes,
  # and the second separately consists of any building changes.
  def respond_to_state(self, state) -> Tuple[GroupOfChanges, GroupOfChanges]:
    if self._player.jail_moves > 0 and self._player.jail_free_count > 0:
      use_jail_free_card = self._return_jail_free_card(self._player, state)
      return use_jail_free_card, None
    return None, None

  # By default, player does not revise his hotel demolitions
  def revise_hotel_demolitions(self, player, original_hotel_demolitions, state):
    return GroupOfChanges()
