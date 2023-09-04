from engine import Engine
from gamestate import GameState
import multiprocessing
import argparse
import tqdm
import sys
import random
from functools import partial


def extract(result):
  remaining_players = [p for p in result.players if p.is_in_game]
  cash = [p.cash for p in remaining_players]
  if len(remaining_players) > 1:
    return 'Stalemate', cash
  else:
    return remaining_players[0].name, cash


def run_simulation(state, seed):
  random.seed(seed)
  state.randomize()
  engine = Engine(state, interactive=False, stalemate_threshold=1000)
  return extract(engine.run())


def analyze(results):
  win_counts = {}
  for result, _ in results:
    win_counts[result] = win_counts.get(result, 0) + 1

  win_percentages = {k: v / len(results) for k, v in win_counts.items()}
  win_confidences = {  # todo: from copilot, validate
    k: 1.96 * (v * (1 - v) / len(results))**0.5 for k, v in win_percentages.items()}

  print('Stalemate: %d (%.2f%% ± %.2f%%)' % (
    win_counts.get('Stalemate', 0),
    win_percentages.get('Stalemate', 0) * 100,
    win_confidences.get('Stalemate', 0) * 100))
  for player in sorted(win_percentages.keys()):
    if player == 'Stalemate':
      continue
    print('%s: %d (%.2f%% ± %.2f%%)' % (
      player, win_counts.get(player, 0),
      win_percentages.get(player, 0) * 100,
      win_confidences.get(player, 0) * 100))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('iterations', type=int)
  parser.add_argument('-l', '--load-from-file',
                      help='Name of JSON file to load from. If none provided, the simulator will start a new game.')
  parser.add_argument('-s', '--seed', type=int,
                      help='Random seed to use. Disables parallelization and enables logging.')
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
    engine = Engine(initial_state, interactive=False, stalemate_threshold=1000)
    result = engine.run()
    print('Result:')
    print(extract(result))
    sys.exit(0)

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
      pool.apply_async(run_simulation, args=(initial_state._copy(), seed),
                       callback=partial(_result_callback, seed), error_callback=partial(_error_callback, seed))

    pool.close()
    pool.join()

  pbar.close()

  analyze(results)


if __name__ == '__main__':
  main()
