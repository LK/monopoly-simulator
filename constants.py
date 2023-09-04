# Card-related constants
CHANCE_CARD = True
COMMUNITY_CHEST_CARD = not CHANCE_CARD
CHANCE_PER_HOUSE_FEE = 25
CHANCE_PER_HOTEL_FEE = 100
COMMUNITY_CHEST_PER_HOUSE_FEE = 40
COMMUNITY_CHEST_PER_HOTEL_FEE = 115

NUM_HOUSES_BEFORE_HOTEL = 4

# Total quantities of items on the board
NUM_HOUSES = 32
NUM_HOTELS = 12
NUM_SQUARES = 40

# Represents the "Get out of jail free" card
LMBDA_GET_OUT_OF_JAIL_FREE = 'jail card'

# Max number of turns a player can spend in jail. When jail moves
# reach 0, the player must leave on that roll.
JAIL_MOVES = 2

# Property group labels
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

# Square names
GO = "Go"
MEDITERRANEAN_AVENUE = "Mediterranean Avenue"
COMMUNITY_CHEST_1 = "Community Chest 1"
BALTIC_AVENUE = "Baltic Avenue"
INCOME_TAX = "Income Tax"
READING_RAILROAD = "Reading Railroad"
ORIENTAL_AVENUE = "Oriental Avenue"
CHANCE_1 = "Chance 1"
VERMONT_AVENUE = "Vermont Avenue"
CONNECTICUT_AVENUE = "Connecticut Avenue"
JAIL = "Jail"
ST_CHARLES_PLACE = "St. Charles Place"
ELECTRIC_COMPANY = "Electric Company"
STATES_AVENUE = "States Avenue"
VIRGINIA_AVENUE = "Virginia Avenue"
PENNSYLVANIA_RAILROAD = "Pennsylvania Railroad"
ST_JAMES_PLACE = "St. James Place"
COMMUNITY_CHEST_2 = "Community Chest 2"
TENNESSEE_AVENUE = "Tennessee Avenue"
NEW_YORK_AVENUE = "New York Avenue"
FREE_PARKING = "Free Parking"
KENTUCKY_AVENUE = "Kentucky Avenue"
CHANCE_2 = "Chance 2"
INDIANA_AVENUE = "Indiana Avenue"
ILLINOIS_AVENUE = "Illinois Avenue"
B_AND_O_RAILROAD = "B. & O. Railroad"
ATLANTIC_AVENUE = "Atlantic Avenue"
VENTNOR_AVENUE = "Ventnor Avenue"
WATER_WORKS = "Water Works"
MARVIN_GARDENS = "Marvin Gardens"
GO_TO_JAIL = "Go To Jail"
PACIFIC_AVENUE = "Pacific Avenue"
NORTH_CAROLINA_AVENUE = "North Carolina Avenue"
COMMUNITY_CHEST_3 = "Community Chest 3"
PENNSYLVANIA_AVENUE = "Pennsylvania Avenue"
SHORT_LINE_RAILROAD = "Short Line Railroad"
CHANCE_3 = "Chance 3"
PARK_PLACE = "Park Place"
LUXURY_TAX = "Luxury Tax"
BOARDWALK = "Boardwalk"

INDEX = {}  # dictionary maps names to their indices on the board
names = [
  GO,
  MEDITERRANEAN_AVENUE,
  COMMUNITY_CHEST_1,
  BALTIC_AVENUE,
  INCOME_TAX,
  READING_RAILROAD,
  ORIENTAL_AVENUE,
  CHANCE_1,
  VERMONT_AVENUE,
  CONNECTICUT_AVENUE,
  JAIL,
  ST_CHARLES_PLACE,
  ELECTRIC_COMPANY,
  STATES_AVENUE,
  VIRGINIA_AVENUE,
  PENNSYLVANIA_RAILROAD,
  ST_JAMES_PLACE,
  COMMUNITY_CHEST_2,
  TENNESSEE_AVENUE,
  NEW_YORK_AVENUE,
  FREE_PARKING,
  KENTUCKY_AVENUE,
  CHANCE_2,
  INDIANA_AVENUE,
  ILLINOIS_AVENUE,
  B_AND_O_RAILROAD,
  ATLANTIC_AVENUE,
  VENTNOR_AVENUE,
  WATER_WORKS,
  MARVIN_GARDENS,
  GO_TO_JAIL,
  PACIFIC_AVENUE,
  NORTH_CAROLINA_AVENUE,
  COMMUNITY_CHEST_3,
  PENNSYLVANIA_AVENUE,
  SHORT_LINE_RAILROAD,
  CHANCE_3,
  PARK_PLACE,
  LUXURY_TAX,
  BOARDWALK
]
for i in range(0, len(names)):
  INDEX[names[i]] = i
del names
