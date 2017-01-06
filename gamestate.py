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
		PROP_MEDITERRANEAN 					= ColorProperty(name=MEDITERRANEAN_AVENUE, 
																								price=60, 
																								rents=[4, 10, 30, 90, 160, 250], 				
																								property_group=PURPLE,
																								size_of_property_group=2, 
																								house_price=50)

		PROP_BALTIC 								= ColorProperty(name=BALTIC_AVENUE, 		
																								price=60, 	
																								rents=[4, 20, 60, 180, 320, 450], 			
																								property_group=PURPLE,
																								size_of_property_group=2,
																								house_price=50)

		PROP_ORIENTAL 							= ColorProperty(name=ORIENTAL_AVENUE, 	
																								price=100, 	
																								rents=[6, 30, 90, 270, 400, 550], 			
																								property_group=LIGHT_BLUE, 
																								size_of_property_group=3,
																								house_price=50)

		PROP_VERMONT 								= ColorProperty(name=VERMONT_AVENUE, 		
																								price=100, 	
																								rents=[6, 30, 90, 270, 400, 550], 			
																								property_group=LIGHT_BLUE, 
																								size_of_property_group=3,
																								house_price=50)

		PROP_CONNECTICUT 						= ColorProperty(name=CONNECTICUT_AVENUE, 	
																								price=120, 	
																								rents=[8, 40, 100, 300, 450, 600], 			
																								property_group=LIGHT_BLUE, 
																								size_of_property_group=3,
																								house_price=50)


		PROP_ST_CHARLES 						= ColorProperty(name=ST_CHARLES_PLACE,	
																								price=140, 	
																								rents=[10, 50, 150, 450, 625, 750], 		
																								property_group=PINK, 			
																								size_of_property_group=3,
																								house_price=100)

		PROP_STATES 								= ColorProperty(name=STATES_AVENUE,			
																								price=140, 	
																								rents=[10, 50, 150, 450, 625, 750], 		
																								property_group=PINK, 			
																								size_of_property_group=3,
																								house_price=100)

		PROP_VIRGINIA 							= ColorProperty(name=VIRGINIA_AVENUE,		
																								price=160, 	
																								rents=[12, 60, 180, 500, 700, 900], 		
																								property_group=PINK, 			
																								size_of_property_group=3,
																								house_price=100)


		PROP_ST_JAMES 							= ColorProperty(name=ST_JAMES_PLACE,		
																								price=180, 	
																								rents=[14, 70, 200, 550, 750, 950], 		
																								property_group=ORANGE, 		
																								size_of_property_group=3,
																								house_price=100)

		PROP_TENNESSEE 							= ColorProperty(name=TENNESSEE_AVENUE,	
																								price=180, 	
																								rents=[14, 70, 200, 550, 750, 950], 		
																								property_group=ORANGE, 		
																								size_of_property_group=3,
																								house_price=100)

		PROP_NEW_YORK 							= ColorProperty(name=NEW_YORK_AVENUE,		
																								price=200, 	
																								rents=[16, 80, 220, 600, 800, 1000], 		
																								property_group=ORANGE, 		
																								size_of_property_group=3,
																								house_price=100)


		PROP_KENTUCKY 							= ColorProperty(name=KENTUCKY_AVENUE,			
																								price=220, 	
																								rents=[18, 90, 250, 700, 875, 1050],		
																								property_group=RED, 				
																								size_of_property_group=3, 
																								house_price=150)

		PROP_INDIANA 								= ColorProperty(name=INDIANA_AVENUE,		
																								price=220, 	
																								rents=[18, 90, 250, 700, 875, 1050],		
																								property_group=RED, 				
																								size_of_property_group=3,
																								house_price=150)

		PROP_ILLINOIS 							= ColorProperty(name=ILLINOIS_AVENUE, 		
																								price=240, 	
																								rents=[20, 100, 300, 750, 925, 1100],		
																								property_group=RED, 				
																								size_of_property_group=3, 
																								house_price=150)


		PROP_ATLANTIC 							= ColorProperty(name=ATLANTIC_AVENUE,			
																								price=260, 	
																								rents=[22, 110, 330, 800, 975, 1150],		
																								property_group=YELLOW, 		
																								size_of_property_group=3, 
																								house_price=150)

		PROP_VENTNOR 								= ColorProperty(name=VENTNOR_AVENUE,
																								price=260, 
																								rents=[22, 110, 330, 800, 975, 1150],
																								property_group=YELLOW, 
																								size_of_property_group=3, 
																								house_price=150)

		PROP_MARVIN 								= ColorProperty(name=MARVIN_GARDENS,
																								price=280, 	
																								rents=[24, 120, 360, 850, 1025, 1200], 	
																								property_group=YELLOW, 	
																								size_of_property_group=3,
																								house_price=150)

		PROP_PACIFIC 								= ColorProperty(name=PACIFIC_AVENUE,
																								price=300, 	
																								rents=[26, 130, 390, 900, 1100, 1275],	
																								property_group=GREEN, 			
																								size_of_property_group=3, 
																								house_price=200)

		PROP_NORTH_CAROLINA 				= ColorProperty(name=NORTH_CAROLINA_AVENUE,	
																								price=300, 	
																								rents=[26, 130, 390, 900, 1100, 1275],	
																								property_group=GREEN, 			
																								size_of_property_group=3, 
																								house_price=200)

		PROP_PENNSYLVANIA 					= ColorProperty(name=PENNSYLVANIA_AVENUE,	
																								price=320, 	
																								rents=[28, 150, 450, 1000, 1200, 1400],	
																								property_group=GREEN, 
																								size_of_property_group=3,
																								house_price=200)


		PROP_PARK 									= ColorProperty(name=PARK_PLACE,
																								price=350, 	
																								rents=[35, 175, 500, 1100, 1300, 1500], 
																								property_group=DARK_BLUE, 
																								size_of_property_group=2, 
																								house_price=200)

		PROP_BOARDWALK 							= ColorProperty(name=BOARDWALK,	
																								price=400, 	
																								rents=[50, 200, 600, 1400, 1700, 2000], 
																								property_group=DARK_BLUE,
																								size_of_property_group=2, 
																								house_price=200)

		PROP_READING_RAILROAD 			= NonColorProperty(name=READING_RAILROAD,
																									 price=200, 	
																									 rents=[25, 50, 100, 200], 
																									 property_group=RAILROAD, 	
																									 size_of_property_group=4)

		PROP_PENNSYLVANIA_RAILROAD 	= NonColorProperty(name=PENNSYLVANIA_RAILROAD,
																									 price=200, 	
																									 rents=[25, 50, 100, 200], 
																									 property_group=RAILROAD, 	
																									 size_of_property_group=4)

		PROP_B_AND_O_RAILROAD 			= NonColorProperty(name=B_AND_O_RAILROAD,
																									 price=200,
																									 rents=[25, 50, 100, 200], 
																									 property_group=RAILROAD,
																									 size_of_property_group=4)

		PROP_SHORT_LINE 						= NonColorProperty(name=SHORT_LINE_RAILROAD,
																									 price=200, 	
																									 rents=[25, 50, 100, 200], 
																									 property_group=RAILROAD, 	
																									 size_of_property_group=4)

		PROP_ELECTRIC_COMPANY 			= NonColorProperty(name=ELECTRIC_COMPANY,
																									 price=150, 	
																									 rents=[-1, -1], 					
																									 property_group=UTILITY, 		
																									 size_of_property_group=2)

		PROP_WATER_WORKS 						= NonColorProperty(name=WATER_WORKS,										
																									 price=150, 	
																									 rents=[-1, -1],
																									 property_group=UTILITY, 		
																									 size_of_property_group=2)

		PROP_GO 										= FreeSpace(name=GO)
		PROP_JAIL 									= FreeSpace(name=JAIL)
		PROP_FREE_PARKING 					= FreeSpace(name=FREE_PARKING)
		PROP_GO_TO_JAIL 						= GoToJail(name=GO_TO_JAIL)

		PROP_COMMUNITY_CHEST_1 			= Card(name=COMMUNITY_CHEST_1, card_type=COMMUNITY_CHEST_CARD)
		PROP_COMMUNITY_CHEST_2 			= Card(name=COMMUNITY_CHEST_2,  card_type=COMMUNITY_CHEST_CARD)
		PROP_COMMUNITY_CHEST_3 			= Card(name=COMMUNITY_CHEST_3,  card_type=COMMUNITY_CHEST_CARD)

		PROP_CHANCE_1 							= Card(name=CHANCE_1, card_type=CHANCE_CARD)
		PROP_CHANCE_2 							= Card(name=CHANCE_2, card_type=CHANCE_CARD)
		PROP_CHANCE_3 							= Card(name=CHANCE_3, card_type=CHANCE_CARD)

		PROP_INCOME_TAX 						= Tax(name=INCOME_TAX, tax=200)
		PROP_LUXURY_TAX 						= Tax(name=LUXURY_TAX, tax=100)

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

	@staticmethod
	def _initialize_decks():
		chance_deck 					= Deck(Card.make_chance_functions())
		community_chest_deck 	= Deck(Card.make_community_chest_functions())
		chance_deck.shuffle()
		community_chest_deck.shuffle()
		return { CHANCE_CARD: chance_deck, COMMUNITY_CHEST_CARD: community_chest_deck }


	# Constructor

	def __init__(self, num_players):
		self._players                = GameState._initialize_players(num_players)
		self._squares                = GameState._initialize_squares()
		self._houses_remaining       = NUM_HOUSES
		self._hotels_remaining       = NUM_HOTELS
		self._bank 									 = GameState._initialize_bank(self._squares)
		self._decks									 = GameState._initialize_decks()

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
			player.add_props(added_props)

		for player, removed_props in change.removed_props.iteritems():
			player.remove_props(removed_props)

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
			if change_in_houses > 0:
				prop.build(change_in_houses)
			elif change_in_houses < 0:
				prop.demolish(-change_in_houses)

		self._houses_remaining += change.change_in_houses_remaining
		self._hotels_remaining += change.change_in_hotels_remaining

		for prop, is_mortgaged in change.is_mortgaged.iteritems():
			prop.mortgaged = is_mortgaged


	# Applies a GroupOfChanges
	def apply(self, changes):
		for change in changes:
			self._apply_single_change(change)

	def __str__(self):
		s = ""

		s += "Players:\n"
		for player in self._players:
			s += str(player) + "\n"
		s += "\n"

		s += "Bank: " + str(self._bank) + "\n"

		s += "Squares:\n"
		for square in self._squares:
			s += str(square) + "\n"
		s += "\n"

		s += "Houses remaining: %d\n" % (self._houses_remaining)
		s += "Hotels remaining: %d\n" % (self._hotels_remaining)
		return s
