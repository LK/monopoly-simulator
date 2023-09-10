from gamestate import GameState
from player import Player
from roll import Roll
from groupofchanges import GroupOfChanges
from gamestatechange import GameStateChange
from housingresolver import HousingResolver
from constants import *
import argparse


class Engine(object):
  def __init__(self, game_state, interactive=True, stalemate_threshold=None):
    self._state = game_state
    self._interactive = interactive
    self._stalemate_threshold = stalemate_threshold
    self._state.interactive = self._interactive

  def _wait(self):
    cmd = input('> ')
    if cmd == 'state':
      print()
      print(str(self._state))
    print()

  def run(self):
    steps = 0
    while not self._completed() and (self._stalemate_threshold is None or steps < self._stalemate_threshold):
      steps += 1
      player = self._state.players[self._state.current_player_index]

      self._notify_all()

      # Roll dice
      if self._interactive:
        print('Rolling {name}...'.format(name=player.name))
      num_rolls = 0
      while True:
        num_rolls += 1
        if self._roll(player, num_rolls):
          break

      self._notify_all()
      if self._interactive:
        self._wait()

      # Set to next player
      next_changes = GroupOfChanges(
        changes=[GameStateChange.set_next_player(self._state)]
      )
      self._state.apply(next_changes)

    return self._state

  # Rolls the dice and resolves the roll. roll_index is what number
  # roll this is, 1 to 3. Returns whether the rolling part of this turn is
  # over. You should keep rolling until it returns True
  def _roll(self, player: Player, roll_index: int) -> bool:
    roll = Roll()
    if self._interactive:
      print('%s rolled a %d%s' % (player.name, roll.value,
            ' (doubles)' if roll.is_doubles else ''))

    if roll.is_doubles and roll_index == MAX_DOUBLES:
      self._state.apply(GroupOfChanges(
        changes=[GameStateChange.send_to_jail(player)]))
      return True

    # Handle if player is in jail
    left_jail = False
    if player.jail_moves > 0 and roll.is_doubles:
      self._state.apply(GroupOfChanges(
        changes=[GameStateChange.leave_jail(player)]))
      left_jail = True
    elif player.jail_moves >= 2:
      self._state.apply(GroupOfChanges(
        changes=[GameStateChange.decrement_jail_moves(player)]))
      return True
    elif player.jail_moves == 1:
      pay_changes = player.pay(self._state.bank, 50, self._state)
      leave_changes = GroupOfChanges(
        changes=[GameStateChange.leave_jail(player)])
      self._state.apply(GroupOfChanges.combine([pay_changes, leave_changes]))
      left_jail = True

    # Move player and resolve where they landed
    position = (player.position + roll.value) % NUM_SQUARES
    self._state.apply(
      GroupOfChanges([
        GameStateChange.change_position(
          player, position, self._state.bank, self._state.squares,
          cause=GameStateChange.Cause.ROLL)
      ])
    )
    self._state.apply(self._state.squares[position].landed(
      player, roll.value, self._state))
    return not roll.is_doubles or left_jail

  def _notify_all(self):
    if self._interactive:
      print('Notifying players...')
    player_building_changes = {}
    for player in self._state.players:
      non_building_changes, building_changes = player.respond_to_state(self._state)
      if non_building_changes:
        self._state.apply(non_building_changes)
      if building_changes:
        player_building_changes[player] = building_changes

    housing_resolver = HousingResolver(player_building_changes, self._state)
    housing_resolver.resolve()

  def _completed(self):
    remaining = 0
    for player in self._state.players:
      if player.is_in_game:
        remaining += 1

    return remaining <= 1


def main():
  parser = argparse.ArgumentParser(prog='Monopoly Simulator')
  parser.add_argument('-l', '--load-from-file',
                      help='Name of JSON file to load from. If none provided, the simulator will start a new game.')
  args = parser.parse_args()

  state = GameState(load_from_file=args.load_from_file)
  state.randomize()

  print('Initial game state:')
  print(str(state))

  # Run game
  engine = Engine(state, stalemate_threshold=1000)
  engine.run()


if __name__ == '__main__':
  main()
