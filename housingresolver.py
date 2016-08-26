'''
Author:   Michael Friedman
Created:  8/23/16

Description:
	This class resolves housing conflicts. It takes in a set of housing conditions
	in the form of BuildingRequests and a GameState, and it follows a set of
	rules/procedures to determine when houses/hotels are built, demolished, and
	auctioned. The rules are documented in design/housing-resolver.txt.

	This implementation currently adopts the Convention:
		House builds get priority over hotel demolitions
	(See design/housing-resolver.txt for explanation)
'''

from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from colorproperty import ColorProperty

class HousingResolver(object):

	# Constants
	BEFORE 	= False
	AFTER		= not BEFORE
	BEFORE_HOUSE_BUILDS				= BEFORE
	BEFORE_HOTEL_BUILDS				= BEFORE
	BEFORE_HOUSE_DEMOLITIONS	= BEFORE
	BEFORE_HOTEL_DEMOLITIONS 	= BEFORE
	AFTER_HOUSE_BUILDS				= AFTER
	AFTER_HOTEL_BUILDS				= AFTER
	AFTER_HOUSE_DEMOLITIONS		= AFTER
	AFTER_HOTEL_DEMOLITIONS		= AFTER

	# These are used to override conditions that determine a shortage, in order to
	# enforce our Convention
	OVERRIDE_TRUE 	= True
	OVERRIDE_FALSE	= False

	# Takes in a dictionary mapping Players to their BuildingRequests and the
	# current GameState
	def __init__(self, player_building_requests, state):
		self._player_building_requests = player_building_requests
		self._state = state

		self._houses_built 			= 0
		self._hotels_built			= 0
		self._houses_demolished = 0
		self._hotels_demolished = 0
		for _, building_requests in self._player_building_requests.iteritems():
			self._houses_built 			+= building_requests.houses_built
			self._hotels_built 			+= building_requests.hotels_built
			self._houses_demolished += building_requests.houses_demolished
			self._hotels_demolished += building_requests.hotels_demolished
		_resolve()


	# Building/demolishing

	def _build_houses(self):
		for _, building_requests in player_building_requests.iteritems():
			self._state.apply(building_requests.house_builds)

	def _build_hotels(self):
		for _, building_requests in player_building_requests.iteritems():
			self._state.apply(building_requests.hotel_builds)

	def _demolish_houses(self):
		for _, building_requests in player_building_requests.iteritems():
			self._state.apply(building_requests.house_demolitions)

	def _demolish_hotels(self):
		for _, building_requests in player_building_requests.iteritems():
			self._state.apply(building_requests.hotel_demolitions)

	# Optimized method for applying all building changes in one shot, rather than
	# calling each of the preceding methods individually
	def _build_and_demolish_all(self):
		for _, building_requests in self._player_building_requests.iteritems():
				self._state.apply(building_requests.hotel_demolitions)
				self._state.apply(building_requests.house_builds)
				self._state.apply(building_requests.hotel_builds)


	# Shortage tests

	# Returns true if there is a hotel shortage, false if not, based on whether
	# hotels were demolished yet
	def _is_hotel_shortage(self, were_hotels_demolished):
		if were_hotels_demolished:
			return self._hotels_built > self._state.hotels_remaining
		else:
			return self._hotels_built > self._state.hotels_remaining + self._hotels_demolished

	# Returns true if there is a house shortage, false if not, based on whether
	# houses were demolished yet AND whether hotels were built yet
	def _is_house_shortage(self, were_houses_demolished, were_hotels_built):
		if were_houses_demolished and were_hotels_built:
			return self._houses_built > self._state.houses_remaining
		else:
			if not were_houses_demolished and were_hotels_built:
				num_houses_to_become_available = self._houses_demolished
			elif were_houses_demolished and not were_hotels_built:
				num_houses_to_become_available = ColorProperty.NUM_HOUSES_BEFORE_HOTEL * self._hotels_built
			else:
				num_houses_to_become_available = self._houses_demolished + (ColorProperty.NUM_HOUSES_BEFORE_HOTEL * self._hotels_built)
			return self._houses_built > self._state.houses_remaining + num_houses_to_become_available


	# Auctioning

	# Returns a list of players who requested house builds
	def _get_players_building_houses(self):
		players_building_houses = []
			for player, building_requests in self._player_building_requests.iteritems():
				if building_requests.houses_built > 0:
					players_building_houses.append(player)
		return players_building_houses

	# Auctions the number of houses among the list of players provided. Returns
	# a GroupOfChanges building the houses for the winners of each auction on
	# their desired properties
	@staticmethod
	def _auction_house_builds(num_houses, players, state):
		pass # TODO: Implement auction for house builds

	# Returns a list of players who requested hotel builds
	def _get_players_building_hotels(self):
		players_building_hotels = []
			for player, building_requests in self._player_building_requests.iteritems():
				if building_requests.hotels_built > 0:
					players_building_hotels.append(player)
		return players_building_hotels

	# Auctions the number of hotels among the list of players provided. Returns
	# a GroupOfChanges building the hotels for the winners of each auction on
	# their desired properties
	@staticmethod
	def _auction_hotel_builds(num_hotels, players, state):
		pass # TODO: Implement auction for hotel builds

	# Returns a list of players who requested hotel demolitions
	def _get_players_demolishing_hotels(self):
		players_demolishing_hotels= []
			for player, building_requests in self._player_building_requests.iteritems():
				if building_requests.hotels_demolished > 0:
					players_demolishing_hotels.append(player)
		return players_demolishing_hotels

	# Auctions the number of houses (for hotel demolitions) among the list of
	# players provided. Returns a GroupOfChanges building the houses for the
	# winners of each auction on their desired properties
	@staticmethod
	def _auction_hotel_demolitions(num_houses, players, state):
		pass # TODO: Implement acution for hotel demolitions


	# Special case procedure for hotel demolitions

	# Returns true if there are enough houses to demolish the requested number of
	# hotels, false if not, based on whether houses were built yet
	def _are_enough_houses_for_hotel_demolitions(self, were_houses_built):
		num_houses_needed = ColorProperty.NUM_HOUSES_BEFORE_HOTEL * self._hotels_demolished
		if were_houses_built:
			return num_houses_needed <= self._state.houses_remaining
		else:
			return num_houses_needed <= self._state.houses_remaining + self._houses_built

	# Settles the case when players want to demolish hotels, but there are fewer
	# than 4 houses available. Returns a GroupOfChanges that demolishes hotels and
	# builds houses appropriately according to the players' desires
	def _settle_hotel_demolitions(self, were_houses_built):
		if _are_enough_houses_for_hotel_demolitions(were_houses_built):
				for player, building_requests in self._player_building_requests.iteritems():
					self._state.apply(building_requests.hotel_demolitions)
			else:
				# Ask players demolishing hotels if it is ok to reduce past the 4 house
				# level, or auction them
				players_demolishing_hotels = _get_players_demolishing_hotels()
				if len(players_demolishing_hotels) > 1:
					result_of_auction = _auction_hotel_demolitions(self._state.houses_remaining, players_demolishing_hotels, self._state)
					self._state.apply(result_of_auction)
				else:
					# Ask the 1 player if he wants to reduce past the 4 house level
					player = players_demolishing_hotels[0]
					his_hotel_demolitions = player_building_requests[player].hotel_demolitions
					if player.will_demolish_to(self._state.houses_remaining, his_hotel_demolitions, self._state): # TODO: Implement Player.will_demolish_to()
						# TODO: Get the player's new hotel_demolitions and return them
						return GroupOfChanges([])
					else:
						# No demolitions happen
						return GroupOfChanges([])


	# Main resolution procedure

	# Resolves the housing conflicts according to our rules, and applies the
	# changes directly to the GameState
	def _resolve(self):
		# 1: Demolish houses
		_demolish_houses()

		if _is_hotel_shortage(BEFORE_HOTEL_DEMOLITIONS):
			# 2: Build houses
			if not _is_house_shortage(AFTER_HOUSE_DEMOLITIONS, OVERRIDE_TRUE):
				_build_houses()
			else:
				# Auction houses
				result_of_auction = _auction_house_builds(self._state.houses_remaining, _get_players_building_houses(), self._state)
				self._state.apply(result_of_auction)

			# 3: Demolish hotels
			_settle_hotel_demolitions(AFTER_HOUSE_BUILDS) # special case dealt with separately

			# 4: Build hotels
			if not _is_hotel_shortage(AFTER_HOTEL_DEMOLITIONS):
				_build_hotels()
			else:
				# Auction the remaining hotels
				result_of_auction = _auction_hotel_builds(self._state.hotels_remaining, _get_players_building_hotels(), self._state)
				self._state.apply(result_of_auction)
				
		elif _is_house_shortage(AFTER_HOUSE_DEMOLITIONS, BEFORE_HOTEL_BUILDS):
			# 2: Build hotels
			if not _is_hotel_shortage(OVERRIDE_TRUE):
				_build_hotels()
			else:
				# Auction for the remaining hotels
				result_of_auction = _auction_hotel_builds(self._state.hotels_remaining, _get_players_building_hotels(), self._state)
				self._state.apply(result_of_auction)

			# 3: Build houses
			if not _is_house_shortage(AFTER_HOUSE_DEMOLITIONS, AFTER_HOTEL_BUILDS):
				_build_houses()
			else:
				# Auction for the remaining houses
				result_of_auction = _auction_house_builds(self._state.houses_remaining, _get_players_building_houses(), self._state)
				self._state.apply(result_of_auction)

			# 4: Demolish hotels
			_settle_hotel_demolitions(AFTER_HOUSE_BUILDS) # special case dealt with separately

		else:	# no shortage, so order doesn't matter
			_build_and_demolish_all()
