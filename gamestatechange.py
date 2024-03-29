'''
Author:   Lenny Khazan
Created:

Description:
  A GameStateChange represents a state transition for the GameState. This class
  defines all the possible legal transitions between two GameStates that comply with
  the rules of Monopoly. They are implemented as static methods that return
  an instance of GameStateChange.
'''

from color_property import ColorProperty
from constants import *
from groupofchanges import GroupOfChanges


class GameStateChange(object):
  class Cause:
    ROLL = 'roll'
    RENT = 'rent'

  def __init__(self, change_in_cash={}, new_position={}, added_props={}, removed_props={},
               card_drawn={}, card_replaced={}, change_in_jail_moves={}, change_in_jail_free_count={},
               is_in_game={}, change_in_houses={}, change_in_houses_remaining=0,
               change_in_hotels_remaining=0, is_mortgaged={}, next_player=None,
               description='', cause=None):
    self._change_in_cash = {}
    for player in list(change_in_cash.keys()):
      self._change_in_cash[player] = change_in_cash[player]

    self._new_position = {}
    for player in list(new_position.keys()):
      self._new_position[player] = new_position[player]

    self._added_props = {}
    for player in list(added_props.keys()):
      self._added_props[player] = added_props[player]

    self._removed_props = {}
    for player in list(removed_props.keys()):
      self._removed_props[player] = removed_props[player]

    self._card_drawn = {}
    for deck, card in card_drawn.items():
      self._card_drawn[deck] = card

    self._card_replaced = {}
    for deck, card in card_replaced.items():
      self._card_replaced[deck] = card

    self._change_in_jail_moves = {}
    for player in list(change_in_jail_moves.keys()):
      self._change_in_jail_moves[player] = change_in_jail_moves[player]

    self._change_in_jail_free_count = {}
    for player in list(change_in_jail_free_count.keys()):
      self._change_in_jail_free_count[player] = change_in_jail_free_count[player]

    self._is_in_game = {}
    for player in list(is_in_game.keys()):
      self._is_in_game[player] = is_in_game[player]

    self._change_in_houses = {}
    for prop in list(change_in_houses.keys()):
      self._change_in_houses[prop] = change_in_houses[prop]

    self._change_in_houses_remaining = change_in_houses_remaining
    self._change_in_hotels_remaining = change_in_hotels_remaining

    self._is_mortgaged = {}
    for prop in list(is_mortgaged.keys()):
      self._is_mortgaged[prop] = is_mortgaged[prop]

    self._next_player = next_player
    self._description = description
    self._cause = cause

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
  def next_player(self):
    return self._next_player

  @property
  def description(self):
    return self._description

  @property
  def cause(self):
    return self._cause

  @staticmethod
  def combine(self, changes):  # TODO: Deprecated - remove combine()
    combined = GameStateChange()
    for change in changes:
      # Merge change_in_cash
      for player, change_in_cash in change._change_in_cash.items():
        if player not in combined._change_in_cash:
          combined._change_in_cash[player] = 0
        combined._change_in_cash[player] += change_in_cash

      # Merge new_position
      for player, new_position in change._new_position.items():
        combined._new_position[player] = new_position

      # Merge added_props
      for player, props in change._added_props.items():
        if player not in combined._added_props:
          combined._added_props[player] = []

        for prop in props:
          if prop in combined._removed_props[player]:
            combined._removed_props[player].remove(prop)

          if prop not in combined._added_props[player]:
            combined._added_props[player].append(prop)

      # Merge removed_props
      for player, props in change._removed_props.items():
        if player not in combined._removed_props:
          combined._removed_props[player] = []

        for prop in props:
          if prop in combined._added_props[player]:
            combined._added_props[player].remove(prop)

          if prop not in combined._removed_props[player]:
            combined._removed_props[player].append(prop)

      # Merge change_in_jail_moves
      for player, change_in_jail_moves in change._change_in_jail_moves.items():
        if player not in combined._change_in_jail_moves:
          combined._change_in_jail_moves[player] = 0
        combined._change_in_jail_moves[player] += change_in_jail_moves

      # Merge change_in_jail_free_count
      for player, change_in_jail_free_count in change._change_in_jail_free_count.items():
        if player not in combined._change_in_jail_free_count:
          combined._change_in_jail_free_count[player] = 0
        combined._change_in_jail_free_count[player] += change_in_jail_free_count

      # Merge is_in_game
      for player, is_in_game in change._is_in_game.items():
        combined._is_in_game[player] = is_in_game

      # Merge change_in_houses
      for color_prop, change_in_houses in change._change_in_houses.items():
        if player not in combined._change_in_houses:
          combined._change_in_houses[color_prop] = 0
        combined._change_in_houses[color_prop] += change_in_houses

      # Merge is_mortgaged
      for prop, is_mortgaged in change._is_mortgaged.items():
        combined._is_mortgaged[prop] = is_mortgaged

    return combined

  def total_houses_built(self):  # TODO: Deprecated - remove total_houses_built()
    return sum(self.change_in_houses.values())

  # -------------

  # Legal transitions between GameStates

  # TODO: Raise exceptions when the parameters passed in are invalid or try to do something illegal

  @staticmethod
  def transfer_money(player_from, player_to, amount, cause=None):
    return GameStateChange(change_in_cash={player_from: -amount, player_to: +amount},
                           description=player_from.name + ' paid ' + str(amount) + ' to ' + player_to.name, cause=cause)

  @staticmethod
  def transfer_property(player_from, player_to, prop):
    return GameStateChange(added_props={player_to: [prop]},
                           removed_props={player_from: [prop]},
                           description=player_from.name + ' transferred ' + prop.name + ' to ' + player_to.name)

  @staticmethod
  def buy_property(prop, player, bank, mortgaged=False):
    transfer_property = GameStateChange.transfer_property(bank, player, prop)
    description = player.name + ' purchased ' + prop.name
    transfer_money = None
    if mortgaged:
      transfer_money = GameStateChange.transfer_money(
        player, bank, 0.5 * prop.price)
      description += ' mortgaged'
    else:
      transfer_money = GameStateChange.transfer_money(player, bank, prop.price)
      description += ' in full'
    return GameStateChange(change_in_cash=transfer_money.change_in_cash,
                           added_props=transfer_property.added_props,
                           removed_props=transfer_property.removed_props,
                           is_mortgaged={prop: mortgaged},
                           description=description)

  # TODO: Remove argument 'squares' when we no longer need to print the square name out
  @staticmethod
  def change_position(player, new_position, bank, squares, cause=None):
    max_roll = 12
    description = player.name + ' moved to ' + squares[new_position].name
    if player.position >= (INDEX[GO] - max_roll) % NUM_SQUARES and new_position < (INDEX[GO] - max_roll) % NUM_SQUARES:
      # Player passed GO
      # TODO: Declare a constant for GO money (200)
      return GameStateChange(new_position={player: new_position},
                             change_in_cash={player: +200, bank: -200},
                             description=description + ' passing ' + GO, cause=cause)
    else:
      # Normal position change
      return GameStateChange(new_position={player: new_position},
                             description=description, cause=cause)

  @staticmethod
  def mortgage(prop, state):
    owner = state.get_owner(prop)
    return GameStateChange(is_mortgaged={prop: True},
                           change_in_cash={owner: +prop.price /
                                           2, state.bank: -prop.price / 2},
                           description=owner.name + ' mortgaged ' + prop.name)

  @staticmethod
  def unmortgage(prop, state):
    owner = state.get_owner(prop)
    fee = round(1.1 * prop.price / 2.0)
    return GameStateChange(is_mortgaged={prop: False},
                           change_in_cash={owner: -fee, state.bank: +fee},
                           description=owner.name + ' unmortgaged ' + prop.name)

  @staticmethod
  def build(prop, state, pending_changes: GroupOfChanges = None):
    new_owner = pending_changes.new_owner(prop) if pending_changes != None else None
    owner = state.get_owner(prop) if new_owner == None else new_owner
    delta_houses = pending_changes.net_houses_on(prop) if pending_changes != None else 0
    new_num_houses = prop.num_houses + delta_houses
    if new_num_houses == NUM_HOUSES_BEFORE_HOTEL:
      # Build a hotel
      return GameStateChange(change_in_houses={prop: +1},
                             change_in_cash={
          owner: -prop.house_price, state.bank: +prop.house_price},
          change_in_houses_remaining=+NUM_HOUSES_BEFORE_HOTEL,
          change_in_hotels_remaining=-1,
          description=owner.name + ' built a hotel on ' + prop.name)
    else:
      # Build a house
      return GameStateChange(change_in_houses={prop: +1},
                             change_in_cash={
          owner: -prop.house_price, state.bank: +prop.house_price},
          change_in_houses_remaining=-1,
          description=owner.name + ' built a house on ' + prop.name)

  @staticmethod
  def demolish(prop, state):
    owner = state.get_owner(prop)
    if prop.has_hotel():
      # Demolish a hotel
      return GameStateChange(change_in_houses={prop: -1},
                             change_in_cash={
          owner: +prop.house_price / 2, state.bank: -prop.house_price / 2},
          change_in_houses_remaining=-NUM_HOUSES_BEFORE_HOTEL,
          change_in_hotels_remaining=+1,
          description=owner.name + ' demolished a hotel on ' + prop.name)
    else:
      # Demolish a house
      return GameStateChange(change_in_houses={prop: -1},
                             change_in_cash={
          owner: +prop.house_price / 2, state.bank: -prop.house_price / 2},
          change_in_houses_remaining=+1,
          description=owner.name + ' demolished a house on ' + prop.name)

  @staticmethod
  def draw_card(deck, player):
    next_card = deck.peek()
    if next_card == LMBDA_GET_OUT_OF_JAIL_FREE:
      # Do not replace the "Get out of jail free" card
      return GameStateChange(card_drawn={deck: next_card},
                             change_in_jail_free_count={player: +1},
                             description=player.name + ' drew a Get Out of Jail Free card')
    else:
      return GameStateChange(card_drawn={deck: next_card},
                             card_replaced={deck: next_card},
                             description=player.name + ' drew a card')

  @staticmethod
  def decrement_jail_card_count(player, deck):
    # TODO: How does the caller know which deck to return "Get out of jail free" to?
    return GameStateChange(card_replaced={deck: LMBDA_GET_OUT_OF_JAIL_FREE},
                           change_in_jail_free_count={player: -1},
                           description=player.name + ' used a Get Out of Jail Free card')

  @staticmethod
  def send_to_jail(player):
    return GameStateChange(new_position={player: INDEX[JAIL]},
                           change_in_jail_moves={player: +JAIL_MOVES},
                           description=player.name + ' went to jail')

  @staticmethod
  def decrement_jail_moves(player):
    return GameStateChange(change_in_jail_moves={player: -1},
                           description=player.name + ' spent a turn in jail')

  @staticmethod
  def leave_jail(player):
    return GameStateChange(change_in_jail_moves={player: -player.jail_moves},
                           description=player.name + ' left jail')

  @staticmethod
  def set_next_player(state):
    # Change to next non-eliminated player
    for i in range(len(state.players)):
      j = (state.current_player_index + i + 1) % (len(state.players))
      if state.players[j].is_in_game:
        return GameStateChange(next_player=j,
                               description='Set current player to ' + state.players[j].name)
    raise Exception('No players left in the game')

  @staticmethod
  def eliminate(player_eliminated, player_eliminator, state):
    # Eliminated player's properties get completely demolished
    demolitions = {}
    for prop in player_eliminated.props:
      if isinstance(prop, ColorProperty):
        demolitions[prop] = -prop.num_houses

    house_money = 0
    for prop, num_houses in demolitions.items():
      house_money += prop.house_price * 0.5 * -num_houses  # num_houses is negative

    change_in_houses_remaining = 0
    for prop, num_houses in demolitions.items():
      change_in_houses_remaining += -num_houses  # num_houses is negative

    # If player is eliminated to the bank, properties become unmortgaged,
    # and Jail Free cards are not tranferred to the bank
    is_mortgaged = {}
    change_in_jail_free_count = {
      player_eliminated: -player_eliminated.jail_free_count}
    if player_eliminator == state.bank:
      # Unmortgage properties, but do not give the bank Jail Free cards
      for prop in player_eliminated.props:
        is_mortgaged[prop] = False
    else:
      # Do not unmortgage properties, but give player_eliminator Jail Free
      # cards
      change_in_jail_free_count[player_eliminator] = + \
        player_eliminated.jail_free_count

    return GameStateChange(new_position={player_eliminated: -1},
                           is_in_game={player_eliminated: False},
                           change_in_cash={player_eliminated: -player_eliminated.cash,
                                           player_eliminator: +player_eliminated.cash + house_money},
                           removed_props={
        player_eliminated: player_eliminated.props},
        added_props={
        player_eliminator: player_eliminated.props},
        change_in_jail_free_count=change_in_jail_free_count,
        change_in_houses=demolitions,
        change_in_houses_remaining=change_in_houses_remaining,
        is_mortgaged=is_mortgaged,
        description=player_eliminated.name + ' lost to ' + player_eliminator.name)
