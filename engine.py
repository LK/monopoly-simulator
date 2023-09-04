import random
from gamestate import GameState
from roll import Roll
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from housingresolver import HousingResolver
from constants import *

class Engine(object):
  def __init__(self, num_players):
    self._state = GameState(num_players)

  def _wait(self):
    cmd = input('')
    if cmd == 'state':
      print()
      print(str(self._state))
    print()

  def run(self):
    num_players = len(self._state.players)
    idx = random.randint(0,num_players-1)
    while not self._completed():
      # cash = [player.cash for player in self._state.players]
      # print cash
      player = self._state.players[idx]
      idx = (idx + 1) % len(self._state.players)
      roll = Roll()
      print('%s rolled a %d%s' % (player.name, roll.value, ' (doubles)' if roll.is_doubles else ''))
      if player.jail_moves > 0 and roll.is_doubles:
        self._state.apply(GroupOfChanges(changes=[GameStateChange.leave_jail(player)]))
      elif player.jail_moves >= 2:
        self._state.apply(GroupOfChanges(changes=[GameStateChange.decrement_jail_moves(player)]))
        self._wait()
        continue
      elif player.jail_moves == 1:
        # TODO: Allow player to choose to use a "Get out of jail free" card
        pay_changes           = player.pay(self._state.bank, 50, self._state)
        leave_changes         = GroupOfChanges(changes=[GameStateChange.leave_jail(player)])
        self._state.apply(GroupOfChanges.combine([pay_changes, leave_changes]))

      self._take_turn(player, roll.value)

      num_rolls = 0
      max_rolls = 2
      while roll.is_doubles:
        roll = Roll()
        print('%s rolled a %d%s' % (player.name, roll.value, ' (doubles)' if roll.is_doubles else ''))
        num_rolls += 1
        if num_rolls > max_rolls:
          self._state.apply(GroupOfChanges(changes=[GameStateChange.send_to_jail(player)]))
          break
        self._take_turn(player, roll.value)

  def _take_turn(self, player, roll):
    position = (player.position + roll) % NUM_SQUARES
    self._state.apply(GroupOfChanges([GameStateChange.change_position(player, position, self._state.bank, self._state.squares)]))
    self._state.apply(self._state.squares[position].landed(player, roll, self._state))
    self._notify_all()

    self._wait()

  def _notify_all(self):
    player_building_requests = {}
    for player in self._state.players:
      notification_changes = player.respond_to_state(self._state)
      self._state.apply(notification_changes.non_building_changes)
      player_building_requests[player] = notification_changes.building_requests

    HousingResolver(player_building_requests, self._state)

  def _completed(self):
    remaining = 0
    for player in self._state.players:
       if player.is_in_game:
         remaining += 1

    return remaining <= 1

def main():
  engine = Engine(4)
  engine.run()


if __name__ == '__main__':
  main()
