from color_property import ColorProperty
from notification_changes import NotificationChanges
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from random import randint
from constants import *

class DefaultDecisionMaker(object):
	def __init__(self):
		pass

	@staticmethod
	def _can_mortgage_property(prop, state):
		for prop in state.get_property_group(prop.property_group):
			if prop.num_houses > 0:
				return False

		return True

	@staticmethod
	def _demolish_from_property_group(prop, state):
		max_houses = 0
		max_houses_prop = None
		for prop in state.get_property_group(prop.property_group):
			if prop.num_houses > max_houses:
				max_houses = prop.num_houses
				max_houses_prop = prop

		if max_houses_prop != None:
			return GameStateChange.demolish(max_houses_prop, state.bank)
		else:
			return None

	def buy_or_deny(player, prop, state):
		if player.cash >= prop.price:
			return GroupOfChanges(changes=[GameStateChange.transfer_money(state.bank, player, prop.price)])
		else:
			return GroupOfChanges(changes=[])

	def pay(player_from, player_to, amount, state):
		changes = [GameStateChange.transfer_money(player_from, player_to, amount)]
		difference = amount - player.cash
		while difference > 0:
			for prop in player_from.props:
				if not prop.mortgaged and DefaultDecisionMaker._can_mortgage_property(prop, state):
					changes.append(GameStateChange.mortgage(prop, state.bank))
					continue

			for prop in player_from.props:
				if prop.num_houses > 0:
					changes.append(DefaultDecisionMaker._demolish_from_property_group(prop, state))
					continue

			return GroupOfChanges(changes=[GameStateChange.eliminate(player_from, player_to)])

		return GroupOfChanges(changes=changes)

	def bid_house_builds(player, highest_bid, props_to_build_on):
		pass

	def bid_hotel_builds(player, highest_bid, props_to_build_on):
		pass

	def bid_hotel_demolitions(self, player, highest_bid, props_to_demolish_on, state):
		bid = player.cash / 2
		prop_to_demolish_on = props_to_demolish_on[0]
		hotel_demolition = GameStateChange.demolish(prop, player, state.bank)
		house_builds = [GameStateChange.build(prop, player, state.bank)] * NUM_HOUSES_BEFORE_HOTEL
		return GroupOfChanges([hotel_demolition] + house_builds)

	def will_trade(self, player, proposal, state):
		return False

	def respond_to_state(self, player, new_state):
		if player.jail_moves > 0 and player.jail_free_count > 0:
			# Pick a Deck to return the jail free card to randomly
			# TODO: Need a better way of picking a Deck to return the jail free card to
			if (randint(0, 1) == 0):
				deck = new_state.deck[CHANCE_CARD]
			else:
				deck = new_state.deck[COMMUNITY_CHEST_CARD]
			get_out_of_jail = GameStateChange.decrement_jail_card_count(player, deck)
			return NotificationChanges([get_out_of_jail])
		else:
			return NotificationChanges()

	def revise_hotel_demolitions(self, player, original_hotel_demolitions, state):
		return GroupOfChanges()