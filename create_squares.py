from square import Square
from property import Property
from color_property import ColorProperty
from non_color_property import NonColorProperty
from card import Card
from tax import Tax
from gotojail import GoToJail
from free_space import FreeSpace

def create_squares():
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
	
	MEDITERRANEAN 				= ColorProperty(Square.MEDITERRANEAN_AVENUE, 	60, [4, 10, 30, 90, 160, 250], 	PURPLE, 2, 50)
	BALTIC 								= ColorProperty(Square.BALTIC_AVENUE, 				60, [4, 20, 60, 180, 320, 450], PURPLE, 2, 50)

	ORIENTAL 							= ColorProperty(Square.ORIENTAL_AVENUE, 		100, [6, 30, 90, 270, 400, 550], 	LIGHT_BLUE, 3, 50)
	VERMONT 							= ColorProperty(Square.VERMONT_AVENUE, 			100, [6, 30, 90, 270, 400, 550], 	LIGHT_BLUE, 3, 50)
	CONNECTICUT 					= ColorProperty(Square.CONNECTICUT_AVENUE, 	 60, [8, 40, 100, 300, 450, 600], LIGHT_BLUE, 3, 50)

	ST_CHARLES 						= ColorProperty(Square.ST_CHARLES_PLACE,	140, [10, 50, 150, 450, 625, 750], PINK, 3, 100)
	STATES 								= ColorProperty(Square.STATE_AVENUE,			140, [10, 50, 150, 450, 625, 750], PINK, 3, 100)
	VIRGINIA 							= ColorProperty(Square.VIRGINIA_AVENUE,		160, [12, 60, 180, 500, 700, 900], PINK, 3, 100)

	ST_JAMES 							= ColorProperty(Square.ST_JAMES_PLACE,		180, [14, 70, 200, 550, 750, 950], 	ORANGE, 3, 100)
	TENNESSEE 						= ColorProperty(Square.TENNESSEE_AVENUE,	180, [14, 70, 200, 550, 750, 950], 	ORANGE, 3, 100)
	NEW_YORK 							= ColorProperty(Square.NEW_YORK_AVENUE,		200, [16, 80, 220, 600, 800, 1000], ORANGE, 3, 100)

	KENTUCKY 							= ColorProperty(Square.KENTUCKY_AVENUE,	220, [18, 90, 250, 700, 875, 1050],		RED, 3, 150)
	INDIANA 							= ColorProperty(Square.INDIANA_AVENUE,	220, [18, 90, 250, 700, 875, 1050],		RED, 3, 150)
	ILLINOIS 							= ColorProperty(Square.ILLINOIS_AVENUE, 240, [20, 100, 300, 750, 925, 1100],	RED, 3, 150)

	ATLANTIC 							= ColorProperty(Square.ATLANTIC_AVENUE,	260, [22, 110, 330, 800, 975, 1150],	YELLOW, 3, 150)
	VENTNOR 							= ColorProperty(Square.VENTNOR_AVENUE,	260, [22, 110, 330, 800, 975, 1150],	YELLOW, 3, 150)
	MARVIN 								= ColorProperty(Square.MARVIN_GARDENS,	280, [24, 120, 360, 850, 1025, 1200], YELLOW, 3, 150)

	PACIFIC 							= ColorProperty(Square.PACIFIC_AVENUE,				300, [26, 130, 390, 900, 1100, 1275],		GREEN, 3, 200)
	NORTH_CAROLINA 				= ColorProperty(Square.NORTH_CAROLINA_AVENUE,	300, [26, 130, 390, 900, 1100, 1275],		GREEN, 3, 200)
	PENNSYLVANIA 					= ColorProperty(Square.PENNSYLVANIA_AVENUE,		320, [28, 150, 450, 1000, 1200, 1400],	GREEN, 3, 200)

	PARK 									= ColorProperty(Square.PARK_PLACE,	350, [35, 175, 500, 1100, 1300, 1500], DARK_BLUE, 2, 200)
	BOARDWALK 						= ColorProperty(Square.BOARDWALK,		400, [50, 200, 600, 1400, 1700, 2000], DARK_BLUE, 2, 200)

	READING_RAILROAD 			= NonColorProperty(Square.READING_RAILROAD,				200, [25, 50, 100, 200], RAILROAD, 4)
	PENNSYLVANIA_RAILROAD = NonColorProperty(Square.PENNSYLVANIA_RAILROAD,	200, [25, 50, 100, 200], RAILROAD, 4)
	B_AND_O_RAILROAD 			= NonColorProperty(Square.B_AND_O_RAILROAD,				200, [25, 50, 100, 200], RAILROAD, 4)
	SHORT_LINE 						= NonColorProperty(Square.SHORT_LINE_RAILROAD,		200, [25, 50, 100, 200], RAILROAD, 4)

	ELECTRIC_COMPANY 			= NonColorProperty(Square.ELECTRIC_COMPANY,	150, [-1, -1], UTILITY, 2)
	WATER_WORKS 					= NonColorProperty(Square.WATER_WORKS,			150, [-1, -1], UTILITY, 2)

	GO 										= FreeSpace(Square.GO)
	JAIL 									= FreeSpace(Square.JAIL)
	FREE_PARKING 					= FreeSpace(Square.FREE_PARKING)
	GO_TO_JAIL 						= GoToJail(Square.GO_TO_JAIL)

	COMMUNITY_CHEST_1 		= Card(Square.COMMUNITY_CHEST_1, Card.COMMUNITY_CHEST_CARD)
	COMMUNITY_CHEST_2 		= Card(Square.COMMUNITY_CHEST_2, Card.COMMUNITY_CHEST_CARD)
	COMMUNITY_CHEST_3 		= Card(Square.COMMUNITY_CHEST_3, Card.COMMUNITY_CHEST_CARD)

	CHANCE_1 							= Card(Square.CHANCE_1, Card.CHANCE_CARD)
	CHANCE_2 							= Card(Square.CHANCE_2, Card.CHANCE_CARD)
	CHANCE_3 							= Card(Square.CHANCE_3, Card.CHANCE_CARD)

	INCOME_TAX 						= Tax(Square.INCOME_TAX, 200)
	LUXURY_TAX 						= Tax(Square.LUXURY_TAX, 100)

	return [
		GO,
		MEDITERRANEAN,
		COMMUNITY_CHEST_1,
		BALTIC,
		INCOME_TAX,
		READING_RAILROAD,
		ORIENTAL,
		CHANCE_1,
		VERMONT,
		CONNECTICUT,
		JAIL,
		ST_CHARLES,
		ELECTRIC_COMPANY,
		STATES,
		VIRGINIA,
		PENNSYLVANIA_RAILROAD,
		ST_JAMES,
		COMMUNITY_CHEST_2,
		TENNESSEE,
		NEW_YORK,
		FREE_PARKING,
		KENTUCKY,
		CHANCE_2,
		INDIANA,
		ILLINOIS,
		B_AND_O_RAILROAD,
		ATLANTIC,
		VENTNOR,
		WATER_WORKS,
		MARVIN,
		GO_TO_JAIL,
		PACIFIC,
		NORTH_CAROLINA,
		COMMUNITY_CHEST_3,
		PENNSYLVANIA,
		SHORT_LINE,
		CHANCE_3,
		PARK,
		LUXURY_TAX,
		BOARDWALK
	]