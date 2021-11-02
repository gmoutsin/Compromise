import curses

from players import (
    RandomPlayer,
    GreedyPlayer,
    SmartGreedyPlayer,
    DeterminedPlayer,
    HumanPlayer,
)
from game import CompromiseGame


def main():
    pA = HumanPlayer()
    pB = SmartGreedyPlayer()
    g = CompromiseGame(pA, pB, 30, 5)
    curses.wrapper(g.fancy_play)

    # score = [0,0,0]
    # for i in range(100):
    # g.reset_game()
    # res = g.play()
    # if res[0] > res[1]:
    # score[0] += 1
    # elif res[1] > res[0]:
    # score[2] += 1
    # else:
    # score[1] += 1
    # print(score)


if __name__ == "__main__":
    main()
