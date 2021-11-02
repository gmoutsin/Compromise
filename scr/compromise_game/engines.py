"""
classes for engines to play compromise_game
"""

import random
import curses
import math
import re


class OutOfGridException(Exception):
    pass


class AbstractPlayer:
    """minimal abstract player class"""

    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        return [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]

    def place_pips(
        self, my_state, opp_state, my_score, opp_score, turn, length, num_pips
    ):
        return [
            [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
            for _ in range(num_pips)
        ]


class RandomPlayer(AbstractPlayer):
    pass


class GreedyPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        res = [-1, -1, -1]
        first = [0, 0, 0]
        for grid in range(3):
            s = 0
            for row in range(3):
                for j in range(3):
                    s += my_state[k][i][j] - opp_state[k][i][j]
            first[k] = s
        second = [0, 0, 0]
        for k in range(3):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += my_state[i][k][j] - opp_state[i][k][j]
            second[k] = s
        third = [0, 0, 0]
        for k in range(3):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += my_state[i][j][k] - opp_state[i][j][k]
            third[k] = s
        m = min(first)
        res[0] = [i for i, j in enumerate(first) if j == m][0]
        m = min(second)
        res[1] = [i for i, j in enumerate(second) if j == m][0]
        m = min(third)
        res[2] = [i for i, j in enumerate(third) if j == m][0]
        return res


class SmartGreedyPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        res = [-1, -1, -1]
        tmpres = [-1, -1, -1]
        locked = [False, False, False]
        mins = [0, 0, 0]
        sums = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        tmpTuples = None
        while not (locked[0] and locked[1] and locked[2]):
            for k in range(3):
                s = 0
                for i in range(3):
                    for j in range(3):
                        s += my_state[k][i][j] - opp_state[k][i][j]
                sums[0][k] = s
            for k in range(3):
                s = 0
                for i in range(3):
                    for j in range(3):
                        s += my_state[i][k][j] - opp_state[i][k][j]
                sums[1][k] = s
            for k in range(3):
                s = 0
                for i in range(3):
                    for j in range(3):
                        s += my_state[i][j][k] - opp_state[i][j][k]
                sums[2][k] = s
            for i in range(3):
                mins[i] = min(sums[i])
                tmpres[i] = sums[i].index(min(sums[i]))
            tmpTuples = [[i, x] for i, x in enumerate(mins) if not locked[i]]
            m = [-1, math.inf]
            for t in tmpTuples:
                if t[1] < m[1]:
                    m = t
            blockIndx = m[0]
            res[blockIndx] = tmpres[blockIndx]
            locked[blockIndx] = True
            if locked[0]:
                for i in range(3):
                    for j in range(3):
                        my_state[res[0]][i][j] = 0
                        opp_state[res[0]][i][j] = 0
            if locked[1]:
                for i in range(3):
                    for j in range(3):
                        my_state[i][res[1]][j] = 0
                        opp_state[i][res[1]][j] = 0
            if locked[2]:
                for i in range(3):
                    for j in range(3):
                        my_state[i][j][res[2]] = 0
                        opp_state[i][j][res[2]] = 0
        return res


class DeterminedPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        c1 = [-1, -1]
        c2 = [-1, -1]
        c3 = [-1, -1]
        p1 = -1
        p2 = -1
        p3 = -1
        v = -math.inf
        while (-1 in c1) or (-1 in c2) or (-1 in c3):
            for i in range(0, 3):
                for j in range(0, 3):
                    for k in range(0, 3):
                        if my_state[i][j][k] - opp_state[i][j][k] > v:
                            v = my_state[i][j][k] - opp_state[i][j][k]
                            p1 = i
                            p2 = j
                            p3 = k
                            my_state[i][j][k] = -100
            if c1[0] == -1:
                c1[0] = p1
            else:
                if c1[1] == -1:
                    c1[1] = p1
            if c2[0] == -1:
                c2[0] = p2
            else:
                if c2[1] == -1:
                    c2[1] = p2
            if c3[0] == -1:
                c3[0] = p3
            else:
                if c3[1] == -1:
                    c3[1] = p2
            v = -math.inf
        for i in range(3):
            if not i in c1:
                p1 = i
            if not i in c2:
                p2 = i
            if not i in c3:
                p3 = i
        return [p1, p2, p3]


class HumanPlayer(AbstractPlayer):
    @staticmethod
    def get_pos_from_mouse(mx, my):
        b = c = -1
        a = max(-1, my - 3)
        if mx >= 8 and mx <= 26:
            b = 0
        elif mx >= 33 and mx <= 51:
            b = 1
        elif mx >= 58 and mx <= 76:
            b = 2
        tmp = mx - 8 - 25 * b
        if tmp < 6:
            c = 0
        elif tmp < 12:
            c = 1
        elif tmp < 18:
            c = 2
        if a > 2:
            raise OutOfGridException(
                "get_pos_from_mouse: Invalid coordinates " + str([a, b, c])
            )
        if (a + 1) * (b + 1) * (c + 1) == 0:
            raise OutOfGridException(
                "get_pos_from_mouse: Invalid coordinates " + str([a, b, c])
            )
        return [a, b, c]

    def print_number(self, k, i, j, n, color):
        if n == 0:
            if self.order == 0:
                s = " ."
            else:
                s = ". "
            self.screen.addstr(
                k + 3, 25 * i + 6 * j + 8 + 2 * self.order, s, self.color_neutral
            )
            return
        if n < 10:
            s = " " + str(n)
        else:
            s = str(n)
        self.screen.addstr(k + 3, 25 * i + 6 * j + 8 + 2 * self.order, s, color)

    def __init__(self):
        self.screen = None
        self.color = None
        self.color_highlight = None
        self.color_neutral = None
        self.order = -1
        self.placements = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

    def set_params(
        self, screenref, color_default, color_highlight, colour_neutral, play_order
    ):
        self.screen = screenref
        self.color = color_default
        self.color_highlight = color_highlight
        self.color_neutral = colour_neutral
        self.order = play_order

    def flush_placements(self):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    self.placements[k][i][j] = 0

    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        self.screen.addstr(8, 50, "Pick your move: ", self.color)
        curses.echo()
        s = str(self.screen.getstr(8, 67, 15))
        while re.match("[b]['][123][123][123]", s, flags=0) is None:
            self.screen.addstr(8, 67, "          ", self.color)
            self.screen.addstr(9, 50, "Invalid input!", self.color)
            s = str(self.screen.getstr(8, 67, 15))
        curses.noecho()
        self.screen.addstr(8, 50, "                        ", self.color)
        self.screen.addstr(9, 50, "                        ", self.color)
        return [int(s[2]) - 1, int(s[3]) - 1, int(s[4]) - 1]

    def place_pips(
        self, my_state, opp_state, my_score, opp_score, turn, length, num_pips
    ):
        res = [None for i in range(num_pips)]
        placed = 0
        self.flush_placements()
        self.screen.addstr(10, 50, "Place your pips", self.color)
        while True:
            key = self.screen.getch()
            if key == 10 and placed == num_pips:
                # enter key
                self.screen.addstr(9, 50, "                             ", self.color)
                self.screen.addstr(10, 50, "                       ", self.color)
                self.screen.addstr(11, 50, "                       ", self.color)
                break
            if key == 114 or key == 82:
                # R key
                placed = 0
                self.flush_placements()
                self.screen.addstr(
                    9, 50, "Need " + str(num_pips) + ", placed 0  ", self.color
                )
                self.screen.addstr(10, 50, "Place your pips        ", self.color)
                self.screen.addstr(11, 50, "                       ", self.color)
                for k in range(3):
                    for i in range(3):
                        for j in range(3):
                            self.print_number(i, k, j, my_state[k][i][j], self.color)
            if key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                if placed < num_pips:
                    try:
                        k, i, j = HumanPlayer.get_pos_from_mouse(mx, my)
                        placed += 1
                        self.placements[k][i][j] += 1
                        self.print_number(
                            k,
                            i,
                            j,
                            my_state[i][k][j] + self.placements[k][i][j],
                            self.color_highlight,
                        )
                        self.screen.addstr(
                            9,
                            50,
                            "Need " + str(num_pips) + ", placed " + str(placed),
                            self.color,
                        )
                        if placed == num_pips:
                            self.screen.addstr(
                                10, 50, "Press Enter to accept", self.color
                            )
                            self.screen.addstr(11, 50, "or R to reset", self.color)
                    except OutOfGridException:
                        pass
        indx = 0
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    for _ in range(self.placements[k][i][j]):
                        res[indx] = [i, k, j]
                        indx += 1
        return res
