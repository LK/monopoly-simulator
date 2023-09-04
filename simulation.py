from engine import Engine
from gamestate import GameState
import multiprocessing
import argparse


def run_simulation(state):
  engine = Engine(state, interactive=False, stalemate_threshold=10000)
  return engine.run()


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('iterations', type=int)
  args = parser.parse_args()

  state = GameState()
  print(state.players)
  winners = {p.name: 0 for p in state.players}
  stalemates = 0

  def _result_callback(result: GameState):
    print(result)
    nonlocal stalemates, winners
    remaining_players = [p for p in result.players if p.is_in_game]
    if len(remaining_players) > 1:
      stalemates += 1
    else:
      winners[remaining_players[0].name] += 1

  def _error_callback(error):
    print('*** ERROR: %s' % error)
    print(error.__cause__)

  # with multiprocessing.Pool(processes=1) as pool:
  #   for _ in range(args.iterations):
  #     pool.apply_async(run_simulation, args=(state._copy(),),
  #                      callback=_result_callback, error_callback=_error_callback)

  #   pool.close()
  #   pool.join()

  _result_callback(run_simulation(state._copy()))

  print('Stats:')
  print('  Stalemates: %d' % stalemates)
  for player, wins in winners.items():
    print('  %s: %d' % (player, wins))


if __name__ == '__main__':
  main()
