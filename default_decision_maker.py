from color_property import ColorProperty
from non_color_property import NonColorProperty
from notification_changes import NotificationChanges
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from random import randint
from constants import *

# TODO: Come up with better DeicisionMaker policies that make every possible state of the game reachable
class DefaultDecisionMaker(object):
	def __init__(self):
		pass

	@staticmethod
	def _can_mortgage_property(prop, state):
		if isinstance(prop, NonColorProperty):
			return True

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
			return GameStateChange.demolish(max_houses_prop, state)
		else:
			return None

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
	def pay(self, player_from, player_to, amount, state):
		transfer_money = GameStateChange.transfer_money(player_from, player_to, amount)
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
			if not prop.mortgaged and DefaultDecisionMaker._can_mortgage_property(prop, state):
				mortgage = GameStateChange.mortgage(prop, player_from, state.bank)
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
			if prop.num_houses > 0:
				demolition = DefaultDecisionMaker._demolish_from_property_group(prop, state)
				if demolition != None:
					changes.append(demolition)
					difference -= demolition.change_in_cash[player_from]

		if difference <= 0:
			changes.append(transfer_money)
			return GroupOfChanges(changes=changes)

		# Player cannot pay it off, so he loses
		return GroupOfChanges(changes=[GameStateChange.eliminate(player_from, player_to, state)])

	# By default, player bids half his cash
	def bid_house_builds(self, player, highest_bid, props_to_build_on, state):
		bid = player.cash / 2
		prop_to_build_on = props_to_build_on[0]
		house_build = GameStateChange.build(prop, state)
		return GroupOfChanges([house_build])

	# By default, player bids half his cash
	def bid_hotel_builds(self, player, highest_bid, props_to_build_on, state):
		bid = player.cash / 2
		prop_to_build_on = props_to_build_on[0]
		hotel_build = GameStateChange.build(prop, state)
		return GroupOfChanges([hotel_build])

	# By default, player bids half his cash
	def bid_hotel_demolitions(self, player, highest_bid, props_to_demolish_on, state):
		bid = player.cash / 2
		prop_to_demolish_on = props_to_demolish_on[0]
		hotel_demolition = GameStateChange.demolish(prop, state)
		house_builds = [GameStateChange.build(prop, state)] * NUM_HOUSES_BEFORE_HOTEL
		return GroupOfChanges([hotel_demolition] + house_builds)

	# By default, players deny all trades
	def will_trade(self, player, proposal, state):
		return False

	# By default, player does nothing unless he is in jail and has a jail-free
	# card, in which case he uses it to get out immediately
	def respond_to_state(self, player, new_state):
		if player.jail_moves > 0 and player.jail_free_count > 0:
			# Pick a Deck to return the jail free card to randomly
			# TODO: Need a better way of picking a Deck to return the jail free card to
			if (randint(0, 1) == 0):
				deck = new_state.decks[CHANCE_CARD]
			else:
				deck = new_state.decks[COMMUNITY_CHEST_CARD]
			use_card 		= GameStateChange.decrement_jail_card_count(player, deck)
			leave_jail 	= GameStateChange.leave_jail(player)
			return NotificationChanges(non_building_changes=[use_card, leave_jail])
		else:
			return NotificationChanges()

	# By default, player does not revise his hotel demolitions
	def revise_hotel_demolitions(self, player, original_hotel_demolitions, state):
		return GroupOfChanges()
