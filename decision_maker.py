from color_property import ColorProperty
from notification_changes import NotificationChanges
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from random import randint
from card import Card

class DecisionMaker(object):

	def bid_hotel_demolitions(self, player, highest_bid, props_to_demolish_on, state):
		bid = player.cash / 2
		prop_to_demolish_on = props_to_demolish_on[0]
		hotel_demolition = GameStateChange.demolish(prop, player state.bank)
		house_builds = [GameStateChange.build(prop, player, state.bank)] * ColorProperty.NUM_HOUSES_BEFORE_HOTEL
		return GroupOfChanges([hotel_demolition] + house_builds)

	def will_trade(self, player, proposal, state):
		return False

	def respond_to_state(self, player, new_state):
		if player.jail_moves > 0 and player.jail_free_count > 0:
			# Pick a Deck to return the jail free card to randomly
			# TODO: Need a better way of picking a Deck to return the jail free card to
			if (randint(0, 1) == 0):
				deck = new_state.deck[Card.CHANCE_CARD]
			else:
				deck = new_state.deck[Card.COMMUNITY_CHEST_CARD]
			get_out_of_jail = GameStateChange.decrement_jail_card_count(player, deck)
			return NotificationChanges([get_out_of_jail])
		else:
			return NotificationChanges()

	def revise_hotel_demolitions(self, player, original_hotel_demolitions, state):
		return GroupOfChanges()