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
import datetime
from constants import *

class HousingResolver(object):

	# Constants
	_BEFORE 	= False
	_AFTER		= not _BEFORE
	_BEFORE_HOUSE_BUILDS				= _BEFORE
	_BEFORE_HOTEL_BUILDS				= _BEFORE
	_BEFORE_HOUSE_DEMOLITIONS		= _BEFORE
	_BEFORE_HOTEL_DEMOLITIONS 	= _BEFORE
	_AFTER_HOUSE_BUILDS					= _AFTER
	_AFTER_HOTEL_BUILDS					= _AFTER
	_AFTER_HOUSE_DEMOLITIONS		= _AFTER
	_AFTER_HOTEL_DEMOLITIONS		= _AFTER

	# These are used to override conditions that determine a shortage, in order to
	# enforce our Convention
	_OVERRIDE_TRUE 	= True
	_OVERRIDE_FALSE	= False

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
		self._resolve()


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
				num_houses_to_become_available = NUM_HOUSES_BEFORE_HOTEL * self._hotels_built
			else:
				num_houses_to_become_available = self._houses_demolished + (NUM_HOUSES_BEFORE_HOTEL * self._hotels_built)
			return self._houses_built > self._state.houses_remaining + num_houses_to_become_available


	# Auctioning

	# Returns a list of players who requested house builds
	def _get_players_building_houses(self):
		players_building_houses = []
			for player, building_requests in self._player_building_requests.iteritems():
				if building_requests.houses_built > 0:
					players_building_houses.append(player)
		return players_building_houses

	@staticmethod
	def _auction(num_houses, players, lambda_bid, lambda_extract_bid):
		players_in_auction = dict(zip(players, [True] * len(players)))
		properties_to_build_houses_on = self._properties_to_build_houses_on()
		all_changes = []
		for i in range(num_houses):
			highest_bid = 0
			highest_changes = None
			while True:
				highest_bid_for_round = highest_bid
				highest_changes_for_round = dict()
				for player in players:
					if not players_in_auction[player]:
						continue

					goc = lambda_bid(player, highest_bid, properties_to_build_houses_on[player], self._state)
					bid = 0
					for change in goc:
						if len(change.change_in_houses) > 0:
							bid = lambda_extract_bid(change, state)

					if bid < highest_bid:
						players_in_auction[player] = False
					elif bid > highest_bid_for_round:
						highest_bid_for_round = bid
						highest_changes_for_round = {player: goc}
					elif bid == highest_bid_for_round:
						highest_changes_for_round[player] = goc

				if len(highest_changes_for_round) > 1:
					fastest_time = 10000
					fastest_player = None
					fastest_goc = None
					for player, goc in highest_changes_for_round.iteritems():
						# TODO: Don't use datetime, better timing solution (timeit doesn't work bc lambda params are out of scope)
						times = []
						for i in range(3):
							start = datetime.datetime.now()
							lambda_bid(player, highest_changes_for_round, properties_to_build_houses_on[player], self._state)
							end = datetime.datetime.now()

							times.append((end - start).total_seconds())

						avg_time = sum(times)/len(times)
						if avg_time < fastest_time:
							fastest_time = avg_time
							fastest_player = player
							fastest_goc = goc

					highest_changes_for_round = {fastest_player: fastest_goc}

				if highest_bid_for_round > highest_bid:
					highest_bid = highest_bid_for_round
					highest_changes = highest_changes_for_round[highest_changes_for_round.keys()[0]]

				if len(highest_changes_for_round) == 0 or players_in_auction.values().count(True) <= 1:
					break

			all_changes.append(highest_changes)

		return GroupOfChanges.combine(all_changes)

	# Auctions the number of houses among the list of players provided. Returns
	# a GroupOfChanges building the houses for the winners of each auction on
	# their desired properties
	@staticmethod
	def _auction_house_builds(num_houses, players):
		bid = lambda player, highest_bid, props, state: player.bid_house_builds(highest_bid, props, state)
		extract_bid = lambda change, state: change.change_in_cash[state.bank] - change.changes_in_houses.keys()[0].house_price
		HousingResolver._auction(num_houses, players, bid, extract_bid)

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
	def _auction_hotel_builds(num_hotels, players):
		lambda bid(player, highest_bid, props, state): player.bid_hotel_builds(highest_bid, props, state)
		lambda extract_bid(change, state): change.change_in_cash[state.bank] - change.changes_in_houses.keys()[0].house_price
		HousingResolver._auction(num_houses, players, bid, extract_bid)

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
	def _auction_hotel_demolitions(num_houses, players):
		lambda bid(player, highest_bid, props, state): player.bid_hotel_demolitions(highest_bid, props, state)
		lambda extract_bid(change, state): change.change_in_cash[state.bank] + change.changes_in_houses.keys()[0].house_price/2
		Housing_Resolver._auction(int(num_houses/NUM_HOUSES_BEFORE_HOTEL), players, bid, extract_bid)


	# Special case procedure for hotel demolitions

	# Returns true if there are enough houses to demolish the requested number of
	# hotels, false if not, based on whether houses were built yet
	def _are_enough_houses_for_hotel_demolitions(self, were_houses_built):
		num_houses_needed = NUM_HOUSES_BEFORE_HOTEL * self._hotels_demolished
		if were_houses_built:
			return num_houses_needed <= self._state.houses_remaining
		else:
			return num_houses_needed <= self._state.houses_remaining + self._houses_built

	# Settles the case when players want to demolish hotels, but there are fewer
	# than 4 houses available. Applies the changes that demolish hotels and
	# builds houses appropriately according to the players' desires
	def _settle_hotel_demolitions(self, were_houses_built):
		if self._are_enough_houses_for_hotel_demolitions(were_houses_built):
				for player, building_requests in self._player_building_requests.iteritems():
					self._state.apply(building_requests.hotel_demolitions)
			else:
				# Ask players demolishing hotels if it is ok to reduce past the 4 house
				# level, or auction them
				players_demolishing_hotels = self._get_players_demolishing_hotels()
				if len(players_demolishing_hotels) > 1:
					result_of_auction = HousingResolver._auction_hotel_demolitions(self._state.houses_remaining, players_demolishing_hotels, self._state)
					self._state.apply(result_of_auction)
				elif len(players_demolishing_hotels) == 1:
					# Ask the 1 player if he wants to reduce past the 4 house level
					player = players_demolishing_hotels[0]
					original_hotel_demolitions	= player_building_requests[player].hotel_demolitions
					revised_hotel_demolitions 	= player.revise_hotel_demolitions(original_hotel_demolitions, self._state)
					self._state.apply(revised_hotel_demolitions) # TODO: Validate that these hotel demolitions are actually legal
				else:
					return self._state.apply(GroupOfChanges())


	# Main resolution procedure

	# Resolves the housing conflicts according to our rules, and applies the
	# changes directly to the GameState
	def _resolve(self):
		# 1: Demolish houses
		self._demolish_houses()

		if self._is_hotel_shortage(_BEFORE_HOTEL_DEMOLITIONS):
			# 2: Build houses
			if not self._is_house_shortage(_AFTER_HOUSE_DEMOLITIONS, _OVERRIDE_TRUE):
				self._build_houses()
			else:
				# Auction houses
				result_of_auction = HousingResolver._auction_house_builds(self._state.houses_remaining, self._get_players_building_houses(), self._state)
				self._state.apply(result_of_auction)

			# 3: Demolish hotels
			self._settle_hotel_demolitions(_AFTER_HOUSE_BUILDS) # special case dealt with separately

			# 4: Build hotels
			if not self._is_hotel_shortage(_AFTER_HOTEL_DEMOLITIONS):
				self._build_hotels()
			else:
				# Auction the remaining hotels
				result_of_auction = HousingResolver._auction_hotel_builds(self._state.hotels_remaining, self._get_players_building_hotels(), self._state)
				self._state.apply(result_of_auction)
				
		elif self._is_house_shortage(_AFTER_HOUSE_DEMOLITIONS, _BEFORE_HOTEL_BUILDS):
			# 2: Build hotels
			if not self._is_hotel_shortage(_OVERRIDE_TRUE):
				self._build_hotels()
			else:
				# Auction for the remaining hotels
				result_of_auction = HousingResolver._auction_hotel_builds(self._state.hotels_remaining, self._get_players_building_hotels(), self._state)
				self._state.apply(result_of_auction)

			# 3: Build houses
			if not self._is_house_shortage(_AFTER_HOUSE_DEMOLITIONS, _AFTER_HOTEL_BUILDS):
				self._build_houses()
			else:
				# Auction for the remaining houses
				result_of_auction = HousingResolver._auction_house_builds(self._state.houses_remaining, self._get_players_building_houses(), self._state)
				self._state.apply(result_of_auction)

			# 4: Demolish hotels
			self._settle_hotel_demolitions(_AFTER_HOUSE_BUILDS) # special case dealt with separately

		else:	# no shortage, so order doesn't matter
			self._build_and_demolish_all()


	# Convenience Methods

	# Returns a dict mapping players to a list of properties on which they indent to build houses on
	def _properties_to_build_houses_on(self):
		retval = dict()
		for (player, building_request) in self._player_building_requests.iteritems():
			properties = []
			for change in building_request.house_builds:
				properties.append(change.change_in_houses.keys()[0])

			retval[player] = properties
		return retval

	def _properties_to_build_hotels_on(self):
		retval = dict()
		for (player, building_request) in self._player_building_requests.iteritems():
			properties = []
			for change in building_request.hotel_builds:
				properties.append(change.change_in_houses.keys()[0])

			retval[player] = properties
		return retval