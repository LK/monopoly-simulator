'''
Author:   Lenny Khazan
Created:  

Description:
	A GameStateChange represents a state transition for the GameState. This class
	defines all the possible legal transitions between two GameStates that comply with
	the rules of Monopoly. They are implemented as static methods that return
	an instance of GameStateChange.
'''

from square import Square
from gamestate import GameState
from gotojail import GoToJail
from color_property import ColorProperty
from card import Card

class GameStateChange(object):
	def __init__(self, change_in_cash={}, new_position={}, added_props={}, removed_props={}, card_drawn={}, card_replaced={}, change_in_jail_moves={}, change_in_jail_free_count={}, is_in_game={}, change_in_houses={}, change_in_houses_remaining=0, change_in_hotels_remaining=0, is_mortgaged={}, description=''):
		self._change_in_cash            	= change_in_cash
		self._new_position              	= new_position
		self._added_props          				= added_props
		self._removed_props        				= removed_props
		self._card_drawn									= card_drawn
		self._card_replaced								= card_replaced
		self._change_in_jail_moves				= change_in_jail_moves
		self._change_in_jail_free_count		= change_in_jail_free_count
		self._is_in_game									= is_in_game
		self._change_in_houses						= change_in_houses
		self._change_in_houses_remaining	= change_in_houses_remaining
		self._change_in_hotels_remaining	= change_in_hotels_remaining
		self._is_mortgaged								= is_mortgaged
		self._description									= description

	@property
	def change_in_cash(self):
		return self._change_in_cash
		
	@property
	def new_position(self):
		return self._new_position
		
	@property
	def added_props(self):
		return self._added_props
	
	@property
	def removed_props(self):
		return self._removed_props

	@property
	def card_drawn(self):
		return self._card_drawn
	
	@property
	def card_replaced(self):
		return self._card_replaced
	
	@property
	def change_in_jail_moves(self):
		return self._change_in_jail_moves

	@property
	def change_in_jail_free_count(self):
		return self._change_in_jail_free_count

	@property
	def is_in_game(self):
		return self._is_in_game
	
	@property
	def change_in_houses(self):
		return self._change_in_houses

	@property
	def change_in_houses_remaining(self):
		return self._change_in_houses_remaining
	
	@property
	def change_in_hotels_remaining(self):
		return self._change_in_hotels_remaining
	
	@property
	def is_mortgaged(self):
		return self._is_mortgaged
	
	@property
	def description(self):
		return self._description
	

	@staticmethod
	def combine(self, changes): # TODO: Deprecated - remove combine()
		combined = GameStateChange()
		for change in changes:
			# Merge change_in_cash
			for player, change_in_cash in change._change_in_cash.iteritems():
				if player not in combined._change_in_cash:
					combined._change_in_cash[player] = 0
				combined._change_in_cash[player] += change_in_cash

			# Merge new_position
			for player, new_position in change._new_position.iteritems():
				combined._new_position[player] = new_position

			# Merge added_props
			for player, props in change._added_props.iteritems():
				if player not in combined._added_props:
					combined._added_props[player] = []
				
				for prop in props:
					if prop in combined._removed_props[player]:
						combined._removed_props[player].remove(prop)

					if prop not in combined._added_props[player]:
						combined._added_props[player].append(prop)

			# Merge removed_props
			for player, props in change._removed_props.iteritems():
				if player not in combined._removed_props:
					combined._removed_props[player] = []
				
				for prop in props:
					if prop in combined._added_props[player]:
						combined._added_props[player].remove(prop)

					if prop not in combined._removed_props[player]:
						combined._removed_props[player].append(prop)

			# Merge change_in_jail_moves
			for player, change_in_jail_moves in change._change_in_jail_moves.iteritems():
				if player not in combined._change_in_jail_moves:
					combined._change_in_jail_moves[player] = 0
				combined._change_in_jail_moves[player] += change_in_jail_moves

			# Merge change_in_jail_free_count
			for player, change_in_jail_free_count in change._change_in_jail_free_count.iteritems():
				if player not in combined._change_in_jail_free_count:
					combined._change_in_jail_free_count[player] = 0
				combined._change_in_jail_free_count[player] += change_in_jail_free_count

			# Merge is_in_game
			for player, is_in_game in change._is_in_game.iteritems():
				combined._is_in_game[player] = is_in_game

			# Merge change_in_houses
			for color_prop, change_in_houses in change._change_in_houses.iteritems():
				if player not in combined._change_in_houses:
					combined._change_in_houses[color_prop] = 0
				combined._change_in_houses[color_prop] += change_in_houses

			# Merge is_mortgaged
			for prop, is_mortgaged in change._is_mortgaged.iteritems():
				combined._is_mortgaged[prop] = is_mortgaged

		return combined

	def total_houses_built(self): # TODO: Deprecated - remove total_houses_built()
		return sum(self.change_in_houses.values())

	# -------------

	# Legal transitions between GameStates

	# TODO: Raise exceptions when the parameters passed in are invalid or try to do something illegal

	@staticmethod
	def transfer_money(player_from, player_to, amount):
		return GameStateChange(change_in_cash={ player_from: -amount, player_to: +amount }, description=player_from.name + ' paid ' + str(amount) + ' to ' + player_to.name)

	@staticmethod
	def transfer_property(player_from, player_to, prop):
		return GameStateChange(added_props={ player_to: [prop] }, removed_props={ player_from: [prop] }, description=player_from.name + ' transferred ' + prop.name + ' to ' + player_to.name)

	@staticmethod
	def buy_property(player, prop, mortgaged=False, bank):
		transfer_money = transfer_money(player, bank, prop.price)
		transfer_property = transfer_property(bank, player, prop)
		return GameStateChange(change_in_cash=transfer_money.change_in_cash, added_props=transfer_property.added_props, removed_props=transfer_property.removed_props, is_mortgaged={ prop: mortgaged }, description=player_from.name + ' purchased ' + prop.name + ' (mortgaged)' if mortgaged else '')

	@staticmethod
	def change_position(player, new_position, bank):
		max_roll = 12
		if player.position >= (Square.INDEX[Square.GO] - max_roll) % GameState.NUM_SQUARES and new_position < (Square.INDEX[Square.GO] - max_roll) % GameState.NUM_SQUARES:
			return GameStateChange(new_position={ player: new_position }, change_in_cash:{ player: +200, bank: -200 }, description=player.name + ' moved to ' + str(new_position))
		else:
			return GameStateChange(new_position={ player: new_position }, description=player.name + ' moved to ' + str(new_position), ' passing GO')

	 # TODO: Need to get a reference to player (owner of property) for mortgage(),
	 # unmortgage(), build_house(), build_hotel(), demolish_house(),
	 # demolish_hotel()
	@staticmethod
	def mortgage(prop, bank):
		return GameStateChange(is_mortgaged={ prop: True }, change_in_cash={ player: +prop.price / 2, bank: -prop.price / 2 }, description=prop.name + ' was mortgaged')
	
	@staticmethod
	def unmortgage(prop, bank):
		return GameStateChange(is_mortgaged={ prop: False }, change_in_cash={ player: (-prop.price / 2) * 1.1, bank: (prop.price / 2) * 1.1 }, description=prop.name  + ' was unmortgaged')
	
	@staticmethod
	def build(prop, player, bank):
		if prop.num_houses == ColorProperty.NUM_HOUSES_BEFORE_HOTEL:
			# Build a hotel
			return GameStateChange(change_in_houses={ prop: +1 }, change_in_cash={ player: -prop.house_price, bank: +prop.house_price }, change_in_houses_remaining=+ColorProperty.NUM_HOUSES_BEFORE_HOTEL, change_in_hotels_remaining=-1, description=player.name + ' built a hotel on ' + prop.name)
		else:
			# Build a house
			return GameStateChange(change_in_houses={ prop: +1 }, change_in_cash={ player: -prop.house_price, bank: +prop.house_price }, change_in_houses_remaining=-1, description=player.name + ' built a house on ' + prop.name)

	@staticmethod
	def demolish(prop, player, bank):
		if prop.has_hotel():
			# Demolish a hotel
			return GameStateChange(change_in_houses={ prop: -1 }, change_in_cash={ player: +prop.house_price / 2, bank: -prop.house_price / 2 }, change_in_houses_remaining=-ColorProperty.NUM_HOUSES_BEFORE_HOTEL, change_in_hotels_remaining=+1, description=player.name + ' demolished a hotel on ' + prop.name)
		else:
			# Demolish a house
			return GameStateChange(change_in_houses={ prop: -1 }, change_in_cash={ player: +prop.house_price / 2, bank: -prop.house_price / 2 }, change_in_houses_remaining=+1, description=player.name + ' demolished a house on ' + prop.name)

	@staticmethod
	def draw_card(deck, player):
		next_card = deck.peek()
		if next_card == Card.LMBDA_GET_OUT_OF_JAIL_FREE:
			# Do not replace the "Get out of jail free" card
			return GameStateChange(card_drawn={ deck: next_card }, change_in_jail_free_count={ player: +1 }, description=player.name + ' drew a Get Out of Jail Free card')
		else:
			return GameStateChange(card_drawn={ deck: next_card }, card_replaced={ deck: next_card }, description=player.name + ' drew a card')

	@staticmethod
	def decrement_jail_card_count(player, deck):
		# TODO: How does the caller know which deck to return "Get out of jail free" to?
		return GameStateChange(card_replaced={ deck: Card.LMBDA_GET_OUT_OF_JAIL_FREE }, change_in_jail_free_count={ player: -1 }, description=player.name + ' used a Get Out of Jail Free card')

	@staticmethod
	def send_to_jail(player):
		return GameStateChange(new_position={ player: Square.INDEX[Square.JAIL] }, change_in_jail_moves={ player: +GoToJail.JAIL_MOVES }, description=player.name + ' went to jail')

	@staticmethod
	def decrement_in_jail_moves(player):
		return GameStateChange(change_in_jail_moves={ player: -1 }, description=player.name + ' spent a turn in jail')

	@staticmethod
	def leave_jail(player):
		return GameStateChange(change_in_jail_moves={ player: -player.jail_moves }, description=player.name + ' left jail')

	@staticmethod
	def eliminate(player_eliminated, player_eliminator):
		# Eliminated player's properties get completely demolished
		# TODO: Add money from taking down houses
		demolitions = { }
		for prop in player_eliminated.props:
			if isinstance(prop, ColorProperty):
				demolitions[prop] = -prop.num_houses

		return GameStateChange(is_in_game={ player_eliminated: False }, change_in_cash={ player_eliminated: -player_eliminated.cash, player_eliminator: +player_eliminated.cash }, removed_props={ player_eliminated: player_eliminated.props }, added_props={ player_eliminator: player_eliminated.props }, change_in_jail_free_count={ player_eliminated: -player_eliminated.jail_free_count, player_eliminator: +player_eliminated.jail_free_count }, change_in_houses=demolitions, description=player_eliminated.name + ' lost to ' + player_eliminator.name)
