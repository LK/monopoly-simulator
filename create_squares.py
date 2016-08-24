def create_squares():
	PURPLE = 0
	LIGHT_BLUE = 1
	PINK = 2
	ORANGE = 3
	RED = 4
	YELLOW = 5
	GREEN = 6
	DARK_BLUE = 7

	RAILROAD = 100
	UTILITY = 101
	
	MEDITERRANEAN = ColorProperty('Mediterranean Avenue', 60, [4, 10, 30, 90, 160, 250], PURPLE, 2, 50)
	BALTIC = ColorProperty('Baltic Avenue', 60, [4, 20, 60, 180, 320, 450], PURPLE, 2, 50)

	ORIENTAL = ColorProperty('Oriental Avenue', 100, [6, 30, 90, 270, 400, 550], LIGHT_BLUE, 3, 50)
	VERMONT = ColorProperty('Vermont Avenue', 100, [6, 30, 90, 270, 400, 550], LIGHT_BLUE, 3, 50)
	CONNECTICUT = ColorProperty('Connecticut Avenue', 60, [8, 40, 100, 300, 450, 600], LIGHT_BLUE, 3, 50)

	ST_CHARLES = ColorProperty('St. Charles Place', 140, [10, 50, 150, 450, 625, 750], PINK, 3, 100)
	STATES = ColorProperty('States Avenue', 140, [10, 50, 150, 450, 625, 750], PINK, 3, 100)
	VIRGINIA = ColorProperty('Virginia Avenue', 160, [12, 60, 180, 500, 700, 900], PINK, 3, 100)

	ST_JAMES = ColorProperty('St. James Place', 180, [14, 70, 200, 550, 750, 950], ORANGE, 3, 100)
	TENNESSEE = ColorProperty('Tennessee Avenue', 180, [14, 70, 200, 550, 750, 950], ORANGE, 3, 100)
	NEW_YORK = ColorProperty('New York Avenue', 200, [16, 80, 220, 600, 800, 1000], ORANGE, 3, 100)

	KENTUCKY = ColorProperty('Kentucky Avenue', 220, [18, 90, 250, 700, 875, 1050], RED, 3, 150)
	INDIANA = ColorProperty('Indiana Avenue', 220, [18, 90, 250, 700, 875, 1050], RED, 3, 150)
	ILLINOIS = ColorProperty('Illinois Avenue', 240, [20, 100, 300, 750, 925, 1100], RED, 3, 150)

	ATLANTIC = ColorProperty('Atlantic Avenue', 260, [22, 110, 330, 800, 975, 1150], YELLOW, 3, 150)
	VENTNOR = ColorProperty('Ventnor Avenue', 260, [22, 110, 330, 800, 975, 1150], YELLOW, 3, 150)
	MARVIN = ColorProperty('Marvin Gardens', 280, [24, 120, 360, 850, 1025, 1200], YELLOW, 3, 150)

	PACIFIC = ColorProperty('Pacific Avenue', 300, [26, 130, 390, 900, 1100, 1275], GREEN, 3, 200)
	NORTH_CAROLINA = ColorProperty('North Carolina Avenue', 300, [26, 130, 390, 900, 1100, 1275], GREEN, 3, 200)
	PENNSYLVANIA = ColorProperty('Pennsylvania Avenue', 320, [28, 150, 450, 1000, 1200, 1400], GREEN, 3, 200)

	PARK = ColorProperty('Park Place', 350, [35, 175, 500, 1100, 1300, 1500], DARK_BLUE, 2, 200)
	BOARDWALK = ColorProperty('Boardwalk', 400, [50, 200, 600, 1400, 1700, 2000], DARK_BLUE, 2, 200)

	READING_RAILROAD = NonColorProperty('Reading Railroad', 200, [25, 50, 100, 200], RAILROAD, 4)
	PENNSYLVANIA_RAILROAD = NonColorProperty('Pennsylvania Railroad', 200, [25, 50, 100, 200], RAILROAD, 4)
	B_AND_O_RAILROAD = NonColorProperty('B. & O. Railroad', 200, [25, 50, 100, 200], RAILROAD, 4)
	SHORT_LINE = NonColorProperty('Short Line', 200, [25, 50, 100, 200], RAILROAD, 4)

	ELECTRIC_COMPANY = NonColorProperty('Electric Company', 150, [4, 10], UTILITY, 2)
	WATER_WORKS = NonColorProperty('Water Works', 150, [4, 10], UTILITY, 2)

	GO = FreeSpace('Go')
	JAIL = FreeSpace('Jail')
	FREE_PARKING = FreeSpace('Free Parking')
	GO_TO_JAIL = GoToJail('Go To Jail')

	COMMUNITY_CHEST_1 = Card('Community Chest', Card.COMMUNITY_CHEST_CARD)
	COMMUNITY_CHEST_2 = Card('Community Chest', Card.COMMUNITY_CHEST_CARD)
	COMMUNITY_CHEST_3 = Card('Community Chest', Card.COMMUNITY_CHEST_CARD)

	CHANCE_1 = Card('Chance', Card.CHANCE)
	CHANCE_2 = Card('Chance', Card.CHANCE)
	CHANCE_3 = Card('Chance', Card.CHANCE)

	INCOME_TAX = Tax('Income Tax', 200)
	LUXURY_TAX = Tax('Luxury Tax', 100)

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