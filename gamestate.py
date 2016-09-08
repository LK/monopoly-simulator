'''
Author:   Michael Friedman
Created:  6/29/16

Description:
This class serves as a container for all the components of the game in its current
state: players, squares, chance/community chest cards, etc. Any changes to the state
of the game should go through this object via the state-changing methods.
'''

from color_property import ColorProperty
from player import Player
from prop import Property
from card import Card
from square import Square
from non_color_property import NonColorProperty
from tax import Tax
from gotojail import GoToJail
from free_space import FreeSpace
from deck import Deck
from constants import *

class GameState(object):

	# Initialization

	@staticmethod
	def _initialize_squares():
		PURPLE 			= 0
		LIGHT_BLUE 	= 1
		PINK 				= 2
		ORANGE 			= 3
		RED 				= 4
		YELLOW 			= 5
		GREEN 			= 6
		DARK_BLUE 	= 7

		RAILROAD 		= 100
		UTILITY 		= 101
		
		PROP_MEDITERRANEAN 					= ColorProperty(MEDITERRANEAN_AVENUE, 		60, 	[4, 10, 30, 90, 160, 250], 				PURPLE, 		2, 50)
		PROP_BALTIC 								= ColorProperty(BALTIC_AVENUE, 						60, 	[4, 20, 60, 180, 320, 450], 			PURPLE, 		2, 50)

		PROP_ORIENTAL 							= ColorProperty(ORIENTAL_AVENUE, 					100, 	[6, 30, 90, 270, 400, 550], 			LIGHT_BLUE, 3, 50)
		PROP_VERMONT 								= ColorProperty(VERMONT_AVENUE, 					100, 	[6, 30, 90, 270, 400, 550], 			LIGHT_BLUE, 3, 50)
		PROP_CONNECTICUT 						= ColorProperty(CONNECTICUT_AVENUE, 	 		60, 	[8, 40, 100, 300, 450, 600], 			LIGHT_BLUE, 3, 50)

		PROP_ST_CHARLES 						= ColorProperty(ST_CHARLES_PLACE,					140, 	[10, 50, 150, 450, 625, 750], 		PINK, 			3, 100)
		PROP_STATES 								= ColorProperty(STATES_AVENUE,						140, 	[10, 50, 150, 450, 625, 750], 		PINK, 			3, 100)
		PROP_VIRGINIA 							= ColorProperty(VIRGINIA_AVENUE,					160, 	[12, 60, 180, 500, 700, 900], 		PINK, 			3, 100)

		PROP_ST_JAMES 							= ColorProperty(ST_JAMES_PLACE,						180, 	[14, 70, 200, 550, 750, 950], 		ORANGE, 		3, 100)
		PROP_TENNESSEE 							= ColorProperty(TENNESSEE_AVENUE,					180, 	[14, 70, 200, 550, 750, 950], 		ORANGE, 		3, 100)
		PROP_NEW_YORK 							= ColorProperty(NEW_YORK_AVENUE,					200, 	[16, 80, 220, 600, 800, 1000], 		ORANGE, 		3, 100)

		PROP_KENTUCKY 							= ColorProperty(KENTUCKY_AVENUE,					220, 	[18, 90, 250, 700, 875, 1050],		RED, 				3, 150)
		PROP_INDIANA 								= ColorProperty(INDIANA_AVENUE,						220, 	[18, 90, 250, 700, 875, 1050],		RED, 				3, 150)
		PROP_ILLINOIS 							= ColorProperty(ILLINOIS_AVENUE, 					240, 	[20, 100, 300, 750, 925, 1100],		RED, 				3, 150)

		PROP_ATLANTIC 							= ColorProperty(ATLANTIC_AVENUE,					260, 	[22, 110, 330, 800, 975, 1150],		YELLOW, 		3, 150)
		PROP_VENTNOR 								= ColorProperty(VENTNOR_AVENUE,						260, 	[22, 110, 330, 800, 975, 1150],		YELLOW, 		3, 150)
		PROP_MARVIN 								= ColorProperty(MARVIN_GARDENS,						280, 	[24, 120, 360, 850, 1025, 1200], 	YELLOW, 		3, 150)

		PROP_PACIFIC 								= ColorProperty(PACIFIC_AVENUE,						300, 	[26, 130, 390, 900, 1100, 1275],	GREEN, 			3, 200)
		PROP_NORTH_CAROLINA 				= ColorProperty(NORTH_CAROLINA_AVENUE,		300, 	[26, 130, 390, 900, 1100, 1275],	GREEN, 			3, 200)
		PROP_PENNSYLVANIA 					= ColorProperty(PENNSYLVANIA_AVENUE,			320, 	[28, 150, 450, 1000, 1200, 1400],	GREEN, 			3, 200)

		PROP_PARK 									= ColorProperty(PARK_PLACE,								350, 	[35, 175, 500, 1100, 1300, 1500], DARK_BLUE, 	2, 200)
		PROP_BOARDWALK 							= ColorProperty(BOARDWALK,								400, 	[50, 200, 600, 1400, 1700, 2000], DARK_BLUE, 	2, 200)

		PROP_READING_RAILROAD 			= NonColorProperty(READING_RAILROAD,			200, 	[25, 50, 100, 200], 							RAILROAD, 	4)
		PROP_PENNSYLVANIA_RAILROAD 	= NonColorProperty(PENNSYLVANIA_RAILROAD,	200, 	[25, 50, 100, 200], 							RAILROAD, 	4)
		PROP_B_AND_O_RAILROAD 			= NonColorProperty(B_AND_O_RAILROAD,			200, 	[25, 50, 100, 200], 							RAILROAD, 	4)
		PROP_SHORT_LINE 						= NonColorProperty(SHORT_LINE_RAILROAD,		200, 	[25, 50, 100, 200], 							RAILROAD, 	4)

		PROP_ELECTRIC_COMPANY 			= NonColorProperty(ELECTRIC_COMPANY,			150, 	[-1, -1], 												UTILITY, 		2)
		PROP_WATER_WORKS 						= NonColorProperty(WATER_WORKS,						150, 	[-1, -1], 												UTILITY, 		2)

		PROP_GO 										= FreeSpace(GO)
		PROP_JAIL 									= FreeSpace(JAIL)
		PROP_FREE_PARKING 					= FreeSpace(FREE_PARKING)
		PROP_GO_TO_JAIL 						= GoToJail(GO_TO_JAIL)

		PROP_COMMUNITY_CHEST_1 			= Card(COMMUNITY_CHEST_1, COMMUNITY_CHEST_CARD)
		PROP_COMMUNITY_CHEST_2 			= Card(COMMUNITY_CHEST_2, COMMUNITY_CHEST_CARD)
		PROP_COMMUNITY_CHEST_3 			= Card(COMMUNITY_CHEST_3, COMMUNITY_CHEST_CARD)

		PROP_CHANCE_1 							= Card(CHANCE_1, CHANCE_CARD)
		PROP_CHANCE_2 							= Card(CHANCE_2, CHANCE_CARD)
		PROP_CHANCE_3 							= Card(CHANCE_3, CHANCE_CARD)

		PROP_INCOME_TAX 						= Tax(INCOME_TAX, 200)
		PROP_LUXURY_TAX 						= Tax(LUXURY_TAX, 100)

		return [
			PROP_GO,
			PROP_MEDITERRANEAN,
			PROP_COMMUNITY_CHEST_1,
			PROP_BALTIC,
			PROP_INCOME_TAX,
			PROP_READING_RAILROAD,
			PROP_ORIENTAL,
			PROP_CHANCE_1,
			PROP_VERMONT,
			PROP_CONNECTICUT,
			PROP_JAIL,
			PROP_ST_CHARLES,
			PROP_ELECTRIC_COMPANY,
			PROP_STATES,
			PROP_VIRGINIA,
			PROP_PENNSYLVANIA_RAILROAD,
			PROP_ST_JAMES,
			PROP_COMMUNITY_CHEST_2,
			PROP_TENNESSEE,
			PROP_NEW_YORK,
			PROP_FREE_PARKING,
			PROP_KENTUCKY,
			PROP_CHANCE_2,
			PROP_INDIANA,
			PROP_ILLINOIS,
			PROP_B_AND_O_RAILROAD,
			PROP_ATLANTIC,
			PROP_VENTNOR,
			PROP_WATER_WORKS,
			PROP_MARVIN,
			PROP_GO_TO_JAIL,
			PROP_PACIFIC,
			PROP_NORTH_CAROLINA,
			PROP_COMMUNITY_CHEST_3,
			PROP_PENNSYLVANIA,
			PROP_SHORT_LINE,
			PROP_CHANCE_3,
			PROP_PARK,
			PROP_LUXURY_TAX,
			PROP_BOARDWALK
		]

	@staticmethod
	def _initialize_players(num_players):
		players = []
		for i in range(0, num_players):
			players.append(Player(name='\033[92mPlayer ' + str(i+1) + '\033[0m'))
		return players

	@staticmethod
	def _initialize_bank(all_squares):
		all_props = []
		for square in all_squares:
			if isinstance(square, Property):
				prop = square
				all_props += [prop]
		return Player(cash=0, props=all_props, name='\033[94mThe Bank\033[0m')


	# Constructor

	def __init__(self, num_players):
		self._players                = GameState._initialize_players(num_players)
		self._squares                = GameState._initialize_squares()
		self._houses_remaining       = NUM_HOUSES
		self._hotels_remaining       = NUM_HOTELS
		self._bank 									 = GameState._initialize_bank(self._squares)
		self._decks									 = { CHANCE_CARD: Deck(Card.make_chance_functions()), COMMUNITY_CHEST_CARD: Deck(Card.make_community_chest_functions()) }

		self._decks[CHANCE_CARD].shuffle()
		self._decks[COMMUNITY_CHEST_CARD].shuffle()

	# Private

	def _copy(self):
		num_players = len(self._players)
		copy = GameState(num_players)
		for i in range(0, num_players):
			copy._players[i] = self._players[i].copy()
		for square in self._squares:
			copy._squares.append(square.copy())		# TODO: Implement Square.copy() for all subclasses
		copy._houses_remaining = self._houses_remaining
		copy._hotels_remaining = self._hotels_remaining
		return copy


	# Getters

	@property
	def players(self):
		return self._players

	@property
	def squares(self):
		return self._squares

	@property
	def houses_remaining(self):
		return self._houses_remaining
	
	@property
	def hotels_remaining(self):
		return self._hotels_remaining
	
	@property
	def bank(self):
		return self._bank

	@property
	def decks(self):
		return self._decks
	
	# Other
	def get_property_group(self, prop_group):
		property_group = [square if isinstance(square, Property) and square.property_group == prop_group else None for square in self.squares]
		return filter(lambda x: x != None, property_group)

	def get_owner(self, prop):
		for player in self._players:
			for p in player.props:
				if (p == prop):
					return player
		return self._bank

	def are_enough_houses(self, qty):
		return self._houses_remaining - qty >= 0

	def are_enough_hotels(self, qty):
		return self._hotels_remaining - qty >= 0

	# Applies a single GameStateChange
	def _apply_single_change(self, change):
		print change.description

		for player, change_in_cash in change.change_in_cash.iteritems():
			player.cash += change_in_cash

		for player, new_position in change.new_position.iteritems():
			player.position = new_position

		for player, added_props in change.added_props.iteritems():
			player.add_properties(added_props)

		for player, removed_props in change.removed_props.iteritems():
			player.remove_properties(removed_props)

		for deck, card_drawn in change.card_drawn.iteritems():
			deck.draw_and_remove()

		for deck, card_replaced in change.card_replaced.iteritems():
			deck.insert_on_bottom(card_replaced)

		for player, change_in_jail_free_count in change.change_in_jail_free_count.iteritems():
			player.jail_free_count += change_in_jail_free_count

		for player, change_in_jail_moves in change.change_in_jail_moves.iteritems():
			player.jail_moves += change_in_jail_moves

		for player, is_in_game in change.is_in_game.iteritems():
			player.is_in_game = is_in_game

		for prop, change_in_houses in change.change_in_houses.iteritems():
			# TODO: Add a mechanism to validate that Players did not try to build/demolish houses AND hotels in the same GroupOfChanges. This must be done by two separate GroupOfChanges objects
			if change_in_houses == 0:
				continue
			elif change_in_houses > 0:
				prop.build(change_in_houses)
			else:
				prop.demolish(change_in_houses)

		self._houses_remaining += change.change_in_houses_remaining
		self._hotels_remaining += change.change_in_hotels_remaining

		for prop, is_mortgaged in change.is_mortgaged.iteritems():
			prop.is_mortgaged = is_mortgaged  


	# Applies a GroupOfChanges
	def apply(self, changes):
		for change in changes:
			self._apply_single_change(change)

	def __str__(self):
		s = ""
		s += "Players:\n"
		for player in self._players:
			s += "\t" + str(player) + "\n"
		s += "Squares:\n"
		for square in self._squares:
			s += "\t" + str(square) + "\n"
		s += "Houses remaining: %d\n" % (self._houses_remaining)
		s += "Hotels remaining: %d\n" % (self._hotels_remaining)
		s += "Bank: " + str(bank) + "\n"
		return s
