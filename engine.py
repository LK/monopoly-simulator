from gamestate import GameState
from roll import Roll
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from housingresolver import HousingResolver
from constants import *
import argparse


class Engine(object):
  def __init__(self, load_from_file=None, interactive=True, stalemate_threshold=None):
    self._state = GameState(load_from_file=load_from_file)
    self._interactive = interactive
    self._stalemate_threshold = stalemate_threshold

  def _wait(self):
    if self._interactive:
      cmd = input('')
      if cmd == 'state':
        print()
        print(str(self._state))
      print()

  def run(self):
    steps = 0
    while not self._completed() and (steps < self._stalemate_threshold or self._stalemate_threshold is None):
      steps += 1
      # cash = [player.cash for player in self._state.players]
      # print cash
      player = self._state.players[self._state.current_player_index]
      roll = Roll()
      if self._interactive:
        print('%s rolled a %d%s' % (player.name, roll.value,
              ' (doubles)' if roll.is_doubles else ''))
      if player.jail_moves > 0 and roll.is_doubles:
        self._state.apply(GroupOfChanges(
          changes=[GameStateChange.leave_jail(player)]))
      elif player.jail_moves >= 2:
        self._state.apply(GroupOfChanges(
          changes=[GameStateChange.decrement_jail_moves(player)]))
        self._wait()
        continue
      elif player.jail_moves == 1:
        # TODO: Allow player to choose to use a "Get out of jail free" card
        pay_changes = player.pay(self._state.bank, 50, self._state)
        leave_changes = GroupOfChanges(
          changes=[GameStateChange.leave_jail(player)])
        self._state.apply(GroupOfChanges.combine([pay_changes, leave_changes]))

      self._take_turn(player, roll.value)

      num_rolls = 0
      max_rolls = 2
      while roll.is_doubles:
        roll = Roll()
        if self._interactive:
          print('%s rolled a %d%s' % (player.name, roll.value,
                ' (doubles)' if roll.is_doubles else ''))
        num_rolls += 1
        if num_rolls > max_rolls:
          self._state.apply(GroupOfChanges(
            changes=[GameStateChange.send_to_jail(player)]))
          break
        self._take_turn(player, roll.value)

      # Set to next player
      next_changes = GroupOfChanges(
        changes=[GameStateChange.set_next_player(self._state)]
      )
      self._state.apply(next_changes)

    return self._state

  def _take_turn(self, player, roll):
    position = (player.position + roll) % NUM_SQUARES
    self._state.apply(GroupOfChanges([GameStateChange.change_position(
      player, position, self._state.bank, self._state.squares)]))
    self._state.apply(self._state.squares[position].landed(
      player, roll, self._state))
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
  parser = argparse.ArgumentParser(prog='Monopoly Simulator')
  parser.add_argument('-l', '--load-from-file', help='Name of JSON file to load from. If none provided, the simulator will start a new game.')
  args = parser.parse_args()

  engine = Engine(load_from_file=args.load_from_file)
  engine.run()


if __name__ == '__main__':
  main()
