from engine import Engine
from gamestate import GameState
import multiprocessing
import argparse
import tqdm
import sys
import random
from functools import partial
from dataclasses import dataclass, field
import constants
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Analyzer(ABC, Generic[T]):
  NAME = 'Analyzer'

  @classmethod
  @abstractmethod
  def extract(cls, state: GameState) -> T:
    pass

  @classmethod
  @abstractmethod
  def analyze(cls, results: list[T]):
    pass


class WinRateAnalyzer(Analyzer):
  NAME = 'Win Rate Analyzer'

  @classmethod
  def extract(cls, state: GameState) -> str:
    remaining_players = [p for p in state.players if p.is_in_game]
    if len(remaining_players) == 1:
      return remaining_players[0].name
    else:
      return None

  @classmethod
  def analyze(cls, results: list[str]):
    win_counts = {}
    for result in results:
      win_counts[result] = win_counts.get(result, 0) + 1

    win_percentages = {k: v / len(results) for k, v in win_counts.items()}
    win_confidences = {  # todo: from copilot, validate
      k: 1.96 * (v * (1 - v) / len(results))**0.5 for k, v in win_percentages.items()}

    print('Stalemate: %d (%.2f%% ± %.2f%%)' % (
      win_counts.get(None, 0),
      win_percentages.get(None, 0) * 100,
      win_confidences.get(None, 0) * 100))

    if None in win_percentages:
      del win_percentages[None]

    for player in sorted(win_percentages.keys()):
      print('%s: %d (%.2f%% ± %.2f%%)' % (
        player, win_counts.get(player, 0),
        win_percentages.get(player, 0) * 100,
        win_confidences.get(player, 0) * 100))


analyzers = [WinRateAnalyzer]


def run_simulation(state, seed, stalemate_threshold):
  random.seed(seed)
  state.randomize()
  engine = Engine(state, interactive=False,
                  stalemate_threshold=stalemate_threshold)
  res = engine.run()

  return [analyzer.extract(res) for analyzer in analyzers]

  # print()
  # print('Stalemates with 4 railroads: %d (%.2f%%)' % (
  #   len(stalemates_with_4_railroads),
  #   len(stalemates_with_4_railroads) / len(results) * 100))

  # for result in results:
  #   if result.winner != None and result.railroads[result.winner] != 4:
  #     print(f'Won without 4 railroads: {result.seed}')

  #   if result.winner == None and len([x for x in result.railroads.values() if x == 4]) > 0:
  #     print(f'Stalemate with 4 railroads: {result.seed}')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('iterations', type=int)
  parser.add_argument('-l', '--load-from-file',
                      help='Name of JSON file to load from. If none provided, the simulator will start a new game.')
  parser.add_argument('-s', '--seed', type=int,
                      help='Random seed to use. Disables parallelization and enables logging.')
  parser.add_argument('-t', '--stalemate-threshold', type=int, default=1000,
                      help='Number of moves after which a stalemate is declared.')
  args = parser.parse_args()

  if args.load_from_file:
    initial_state = GameState(load_from_file=args.load_from_file)
  else:
    initial_state = GameState()

  completed = 0
  results = []

  if args.seed:
    random.seed(args.seed)
    initial_state.randomize()
    engine = Engine(initial_state, interactive=False,
                    stalemate_threshold=args.stalemate_threshold)
    result = engine.run()
    print(f'Result: {result}')
    return

  # Create tqdm progress bar
  pbar = tqdm.tqdm(total=args.iterations)

  def _result_callback(seed, result: GameState):
    nonlocal completed
    completed += 1

    results.append(result)

    # Update progress bar
    pbar.update(1)

  def _error_callback(seed, error, *args, **kwargs):
    print("Seed: %d" % seed)
    print('*** ERROR: %s' % error)
    print(error.__cause__)
    sys.exit(1)

  with multiprocessing.Pool() as pool:
    for _ in range(args.iterations):
      seed = random.randint(0, 1000000000)
      pool.apply_async(run_simulation, args=(initial_state._copy(), seed, args.stalemate_threshold),
                       callback=partial(_result_callback, seed), error_callback=partial(_error_callback, seed))

    pool.close()
    pool.join()

  pbar.close()

  for i, analyzer in enumerate(analyzers):
    print(f'===== {analyzer.NAME} =====')
    analyzer.analyze([r[i] for r in results])


if __name__ == '__main__':
  main()
