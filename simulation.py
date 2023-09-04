from engine import Engine
from gamestate import GameState
import multiprocessing
import argparse
import tqdm
import sys


def extract(result):
  remaining_players = [p for p in result.players if p.is_in_game]
  if len(remaining_players) > 1:
    return 'Stalemate'
  else:
    return remaining_players[0].name


def run_simulation(state):
  engine = Engine(state, interactive=False, stalemate_threshold=1000)
  return extract(engine.run())


def analyze(results):
  win_counts = {}
  for result in results:
    # remaining_players = [p for p in result.players if p.is_in_game]
    # if len(remaining_players) > 1:
    #   win_counts['Stalemate'] = win_counts.get('Stalemate', 0) + 1
    # else:
    #   winner = remaining_players[0]
    #   win_counts[winner.name] = win_counts.get(winner.name, 0) + 1

    win_counts[result] = win_counts.get(result, 0) + 1

  win_percentages = {k: v / len(results) for k, v in win_counts.items()}
  win_confidences = {
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
  args = parser.parse_args()

  if args.load_from_file:
    initial_state = GameState(load_from_file=args.load_from_file)
  else:
    initial_state = GameState()

  completed = 0
  results = []

  # Create tqdm progress bar
  pbar = tqdm.tqdm(total=args.iterations)

  def _result_callback(result: GameState):
    nonlocal completed
    completed += 1

    results.append(result)
    # remaining_players = [p for p in result.players if p.is_in_game]
    # if len(remaining_players) > 1:
    #   stalemates += 1
    # else:
    #   winners[remaining_players[0].name] += 1

    # Update progress bar
    pbar.update(1)

  def _error_callback(error):
    print('*** ERROR: %s' % error)
    print(error.__cause__)
    sys.exit(1)

  with multiprocessing.Pool() as pool:
    for _ in range(args.iterations):
      pool.apply_async(run_simulation, args=(initial_state._copy(),),
                       callback=_result_callback, error_callback=_error_callback)

    pool.close()
    pool.join()

  pbar.close()

  analyze(results)


if __name__ == '__main__':
  main()
