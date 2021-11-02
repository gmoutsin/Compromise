import curses

import compromise_game as cg


def main():
    pA = cg.HumanPlayer()
    pB = cg.SmartGreedyPlayer()
    g = cg.CompromiseGame(pA, pB, 30, 5)
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
