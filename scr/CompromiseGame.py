import curses
import random
import re
import math


class AbstractPlayer:
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        return [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]

    def placePips(
        self, my_state, opp_state, my_score, opp_score, turn, length, num_pips
    ):
        return [
            [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]
            for i in range(num_pips)
        ]


class RandomPlayer(AbstractPlayer):
    pass


class GreedyPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, num_pips):
        res = [-1, -1, -1]
        first = [0, 0, 0]
        for k in range(3):
            s = 0
            for i in range(3):
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


class OutOfGridException(Exception):
    pass


class HumanPlayer(AbstractPlayer):
    @staticmethod
    def getPosFromMouse(mx, my):
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
                "getPosFromMouse: Invalid coordinates " + str([a, b, c])
            )
        if (a + 1) * (b + 1) * (c + 1) == 0:
            raise OutOfGridException(
                "getPosFromMouse: Invalid coordinates " + str([a, b, c])
            )
        return [a, b, c]

    def printNumber(self, k, i, j, n, color):
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

    def setParams(
        self, screenref, color_default, color_highlight, colour_neutral, play_order
    ):
        self.screen = screenref
        self.color = color_default
        self.color_highlight = color_highlight
        self.color_neutral = colour_neutral
        self.order = play_order

    def flushPlacements(self):
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

    def placePips(
        self, my_state, opp_state, my_score, opp_score, turn, length, num_pips
    ):
        res = [None for i in range(num_pips)]
        placed = 0
        self.flushPlacements()
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
                self.flushPlacements()
                self.screen.addstr(
                    9, 50, "Need " + str(num_pips) + ", placed 0  ", self.color
                )
                self.screen.addstr(10, 50, "Place your pips        ", self.color)
                self.screen.addstr(11, 50, "                       ", self.color)
                for k in range(3):
                    for i in range(3):
                        for j in range(3):
                            self.printNumber(i, k, j, my_state[k][i][j], self.color)
            if key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                if placed < num_pips:
                    try:
                        k, i, j = HumanPlayer.getPosFromMouse(mx, my)
                        placed += 1
                        self.placements[k][i][j] += 1
                        self.printNumber(
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
                    for m in range(self.placements[k][i][j]):
                        res[indx] = [i, k, j]
                        indx += 1
        return res


class CompromiseGame:
    def __init__(
        self, player_a, player_b, num_pips, length, game_type="s", no_ties=True
    ):
        # in practice the if the game type is not "s" or "g" then it is complex
        self.no_ties = no_ties
        self.type = game_type
        self.green_move = None
        self.red_move = None
        self.game_length = length
        self.turn = 0
        self.red_player = player_a
        self.green_player = player_b
        self.new_pips = num_pips
        self.green_score = 0
        self.red_score = 0
        self.green_pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.red_pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.green_disposable = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.red_disposable = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

    def resetGame(self):
        self.turn = 0
        self.green_move = None
        self.red_move = None
        self.green_score = 0
        self.red_score = 0
        self.green_pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.red_pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.green_disposable = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.red_disposable = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        self.red_player = player_a
        self.green_player = player_b
        self.resetGame()

    def prepareDisposable(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.green_disposable[i][j][k] = self.green_pips[i][j][k]
                    self.red_disposable[i][j][k] = self.red_pips[i][j][k]

    def roundStart(self):
        self.turn += 1
        if self.type == "s":
            for i in range(0, self.new_pips):
                self.red_pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
                self.green_pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
        else:
            self.prepare_disposable()
            green_placing = self.green_player.place_pips(
                self.green_disposable,
                self.red_disposable,
                self.green_score,
                self.red_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.prepare_disposable()
            red_placing = self.red_player.place_pips(
                self.red_disposable,
                self.green_disposable,
                self.red_score,
                self.green_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            for p in green_placing:
                self.green_pips[p[0]][p[1]][p[2]] += 1
            for p in red_placing:
                self.red_pips[p[0]][p[1]][p[2]] += 1

    def getMoves(self):
        if self.type == "g":
            self.red_move = [
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(0, 2),
            ]
            self.green_move = [
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(0, 2),
            ]
        else:
            self.prepareDisposable()
            self.red_move = self.red_player.play(
                self.red_disposable,
                self.green_disposable,
                self.red_score,
                self.green_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.prepareDisposable()
            self.green_move = self.green_player.play(
                self.green_disposable,
                self.red_disposable,
                self.green_score,
                self.red_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            if not isinstance(self.green_move, list):
                raise Exception(
                    "Green Player's move is not a list: " + str(self.green_move)
                )
            if not isinstance(self.red_move, list):
                raise Exception(
                    "Red Player's move is not a list: " + str(self.red_move)
                )
            if not len(self.green_move) == 3:
                raise Exception(
                    "Green Player's move's length has to be 3: " + str(self.green_move)
                )
            if not len(self.red_move) == 3:
                raise Exception(
                    "Red Player's move's length has to be 3: " + str(self.red_move)
                )
            for i in range(3):
                if self.green_move[i] > 2 or self.green_move[i] < 0:
                    raise Exception(
                        "Green Player's move is not between 0 and 2: "
                        + str(self.green_move)
                    )
                if self.red_move[i] > 2 or self.red_move[i] < 0:
                    raise Exception(
                        "Red Player's move is not between 0 and 2: "
                        + str(self.red_move)
                    )

    def updateScore(self):
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    if not (
                        i == self.red_move[0]
                        or i == self.green_move[0]
                        or j == self.red_move[1]
                        or j == self.green_move[1]
                        or k == self.red_move[2]
                        or k == self.green_move[2]
                    ):
                        self.red_score = self.red_score + self.red_pips[i][j][k]
                        self.green_score = self.green_score + self.green_pips[i][j][k]
                        self.red_pips[i][j][k] = 0
                        self.green_pips[i][j][k] = 0
        self.green_move = None
        self.red_move = None

    def playRound(self):
        self.roundStart()
        self.getMoves()
        self.updateScore()

    def play(self):
        while self.turn < self.game_length or (
            self.no_ties and self.red_score == self.green_score
        ):
            self.playRound()
        return [self.red_score, self.green_score]

    def fancyStatePrint(self, stdscr):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    if self.red_pips[k][i][j] > 0:
                        if self.red_pips[k][i][j] < 10:
                            s = " " + str(self.red_pips[k][i][j])
                        else:
                            s = str(self.red_pips[k][i][j])
                        stdscr.addstr(
                            i + 3, 25 * k + 6 * j + 8, s, curses.color_pair(1)
                        )
                    else:
                        stdscr.addstr(
                            i + 3,
                            25 * k + 6 * j + 8,
                            " .",
                        )
                    if self.green_pips[k][i][j] > 0:
                        if self.green_pips[k][i][j] < 10:
                            s = str(self.green_pips[k][i][j]) + " "
                        else:
                            s = str(self.green_pips[k][i][j])
                        stdscr.addstr(s, curses.color_pair(2))
                    else:
                        stdscr.addstr(
                            ". ",
                        )
                    # if self.green_pips[k][i][j] > 0:
                    # stdscr.addstr('{}'.format(self.green_pips[k][i][j]),curses.color_pair(2))
                    # else:
                    # stdscr.addstr(". ")
        stdscr.refresh()

    def fancyStateHighlight(self, stdscr):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    if not (
                        k == self.red_move[0]
                        or k == self.green_move[0]
                        or i == self.red_move[1]
                        or i == self.green_move[1]
                        or j == self.red_move[2]
                        or j == self.green_move[2]
                    ):
                        if self.red_pips[k][i][j] > 0:
                            if self.red_pips[k][i][j] < 10:
                                s = " " + str(self.red_pips[k][i][j])
                            else:
                                s = str(self.red_pips[k][i][j])
                            stdscr.addstr(
                                i + 3, 25 * k + 6 * j + 8, s, curses.color_pair(3)
                            )
                        else:
                            stdscr.addstr(
                                i + 3, 25 * k + 6 * j + 8, " .", curses.color_pair(5)
                            )
                        if self.green_pips[k][i][j] > 0:
                            if self.green_pips[k][i][j] < 10:
                                s = str(self.green_pips[k][i][j]) + " "
                            else:
                                s = str(self.green_pips[k][i][j])
                            stdscr.addstr(s, curses.color_pair(4))
                        else:
                            stdscr.addstr(". ", curses.color_pair(5))
        stdscr.refresh()

    def fancyPrintMoves(self, stdscr):
        stdscr.addstr(
            8,
            20,
            str(self.red_move[0] + 1)
            + str(self.red_move[1] + 1)
            + str(self.red_move[2] + 1),
            curses.color_pair(1),
        )
        stdscr.addstr(
            9,
            20,
            str(self.green_move[0] + 1)
            + str(self.green_move[1] + 1)
            + str(self.green_move[2] + 1),
            curses.color_pair(2),
        )

    def fancyDeleteMoves(self, stdscr):
        stdscr.addstr(8, 20, "   ")
        stdscr.addstr(9, 20, "   ")

    def fancyPrintScore(self, stdscr):
        rs = ""
        # gs = ""
        # if self.green_score < 100:
        # if self.green_score < 10:
        # gs = "  " + str(self.green_score)
        # else:
        # gs = " " + str(self.green_score)
        # else:
        # gs = str(self.green_score)
        gs = str(self.green_score)
        if self.red_score < 100:
            if self.green_score < 10:
                rs = "  " + str(self.red_score)
            else:
                rs = " " + str(self.red_score)
        else:
            rs = str(self.red_score)
        stdscr.addstr(9, 37, rs, curses.color_pair(1))
        stdscr.addstr(" - ")
        stdscr.addstr(gs, curses.color_pair(2))

    def fancyRoundStart(self, stdscr):
        self.turn += 1
        if self.type == "s":
            for i in range(0, self.new_pips):
                self.red_pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
                self.green_pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
        else:
            self.prepare_disposable()
            self.fancy_state_print(stdscr)
            red_placing = self.red_player.place_pips(
                self.red_disposable,
                self.green_disposable,
                self.red_score,
                self.green_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.prepare_disposable()
            self.fancy_state_print(stdscr)
            green_placing = self.green_player.place_pips(
                self.green_disposable,
                self.red_disposable,
                self.green_score,
                self.red_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            for p in green_placing:
                self.green_pips[p[0]][p[1]][p[2]] += 1
            for p in red_placing:
                self.red_pips[p[0]][p[1]][p[2]] += 1

    def fancyPlayRound(self, stdscr):
        self.fancyRoundStart(stdscr)
        self.fancyStatePrint(stdscr)
        self.getMoves()
        self.fancyPrintMoves(stdscr)
        self.fancyStateHighlight(stdscr)
        stdscr.getkey()
        self.updateScore()
        self.fancyDeleteMoves(stdscr)
        self.fancyPrintScore(stdscr)
        self.fancyStatePrint(stdscr)
        stdscr.getkey()

    def fancyPlay(self, stdscr):
        curses.mousemask(1)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)
        if isinstance(self.green_player, HumanPlayer):
            self.green_player.setParams(
                stdscr,
                curses.color_pair(2),
                curses.color_pair(4),
                curses.color_pair(0),
                1,
            )
        if isinstance(self.red_player, HumanPlayer):
            self.red_player.setParams(
                stdscr,
                curses.color_pair(1),
                curses.color_pair(3),
                curses.color_pair(0),
                0,
            )
        stdscr.clear()
        stdscr.addstr(8, 8, "Red move:   ", curses.color_pair(1))
        stdscr.addstr(9, 8, "Green move: ", curses.color_pair(2))
        stdscr.addstr(8, 30, "Round: ")
        stdscr.addstr(9, 30, "Score: ")
        self.fancyStatePrint(stdscr)
        # while True:
        # key = stdscr.getch()
        # stdscr.addstr(0,0,str(key) + "   ")
        while self.turn < self.game_length or (
            self.no_ties and self.red_score == self.green_score
        ):
            stdscr.addstr(8, 39, "      ")
            stdscr.addstr(8, 39, str(self.turn + 1) + " / " + str(self.game_length))
            self.fancyPlayRound(stdscr)
        if self.red_score > self.green_score:
            stdscr.addstr(9, 50, "Player 1 won!       ", curses.color_pair(1))
        elif self.red_score < self.green_score:
            stdscr.addstr(9, 50, "Player 2 won!       ", curses.color_pair(2))
        else:
            stdscr.addstr(9, 50, "Game tied!          ", curses.color_pair(0))
        stdscr.getkey()


if __name__ == "__main__":
    pA = HumanPlayer()
    pB = SmartGreedyPlayer()
    g = CompromiseGame(pA, pB, 30, 5)
    curses.wrapper(g.fancyPlay)

    # score = [0,0,0]
    # for i in range(100):
    # g.resetGame()
    # res = g.play()
    # if res[0] > res[1]:
    # score[0] += 1
    # elif res[1] > res[0]:
    # score[2] += 1
    # else:
    # score[1] += 1
    # print(score)
