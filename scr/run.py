"""
run.py

initialises and runs an instance of compromise_game.CompromiseGame
"""

import curses

import compromise_game as cg


def main():
    """main function that sets up environment and starts the game"""
    player_a = cg.HumanPlayer()
    player_b = cg.SmartGreedyPlayer()
    num_pips = 30
    game_rounds = 5
    game = cg.CompromiseGame(player_a, player_b, num_pips, game_rounds)
    curses.wrapper(game.fancy_play)

    # score = [0,0,0]
    # for i in range(100):
    # game.reset_game()
    # res = game.play()
    # if res[0] > res[1]:
    # score[0] += 1
    # elif res[1] > res[0]:
    # score[2] += 1
    # else:
    # score[1] += 1
    # print(score)


if __name__ == "__main__":
    main()
