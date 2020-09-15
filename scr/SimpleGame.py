import curses
import abc
import random
import re
import math


class AbstractPlayer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        return


class RandomPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        return [random.randint(0,2),random.randint(0,2),random.randint(0,2)]


class GreedyPlayer(AbstractPlayer):
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        res = [-1,-1,-1]
        first = [0,0,0]
        for k in range(3):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += my_state[k][i][j] - opp_state[k][i][j]
            first[k] = s
        second = [0,0,0]
        for k in range(3):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += my_state[i][k][j] - opp_state[i][k][j]
            second[k] = s
        third = [0,0,0]
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
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        res = [-1,-1,-1]
        tmpres = [-1,-1,-1]
        locked = [False,False,False]
        mins = [0,0,0]
        sums = [[0,0,0],[0,0,0],[0,0,0]]
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
            tmpTuples = [[i,x] for i, x in enumerate(mins) if not locked[i]]
            m = [-1,math.inf]
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
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        c1 = [-1, -1]
        c2 = [-1, -1]
        c3 = [-1, -1]
        p1 = -1
        p2 = -1
        p3 = -1
        v = -math.inf
        while (-1 in c1) or (-1 in c2) or (-1 in c2):
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
        return [p1,p2,p3]
        

class HumanPlayer(AbstractPlayer):
    def __init__(self):
        self.screen = None
        self.color = None
    def set_params(self, scr, clr):
        self.screen = scr
        self.color = clr
    def play(self, my_state, opp_state, my_score, opp_score, turn, length, nPips):
        self.screen.addstr(8, 50 , "Pick your move: ", self.color)
        curses.echo()
        s = str(self.screen.getstr(8,67, 15))
        while re.match("[b]['][123][123][123]", s, flags=0) is None:
            self.screen.addstr(8, 67 , "          ", self.color)
            self.screen.addstr(9, 50 , "Invalid input!", self.color)
            s = str(self.screen.getstr(8,67, 15))
        curses.noecho()
        self.screen.addstr(8, 50 , "                        ", self.color)
        self.screen.addstr(9, 50 , "                        ", self.color)
        return [int(s[2])-1,int(s[3])-1,int(s[4])-1]


class Game:
    def __init__(self, playerA, playerB, nPips = 12, length = 10):
        if not (isinstance(playerA, AbstractPlayer)):
            raise Exception("Green Player is not of valid type: " + str(type(playerA)))
        if not (isinstance(playerB, AbstractPlayer)):
            raise Exception("Red Player is not of valid type: " + str(type(playerB)))
        self.green_move = None
        self.red_move = None
        self.game_length = length
        self.turn = 0
        self.green_player = playerA
        self.red_player = playerB
        self.new_pips = nPips
        self.green_score = 0
        self.red_score = 0
        self.green_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.green_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

    def restart_game(self):
        self.turn = 0
        self.green_move = None
        self.red_move = None
        self.green_score = 0
        self.red_score = 0
        self.green_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.green_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

    def new_players(self, playerA, playerB):
        if not (isinstance(playerA, AbstractPlayer)):
            raise Exception("Green Player is not of valid type: " + str(type(playerA)))
        if not (isinstance(playerB, AbstractPlayer)):
            raise Exception("Red Player is not of valid type: " + str(type(playerB)))
        self.turn = 0
        self.green_move = None
        self.red_move = None
        self.green_score = 0
        self.red_score = 0
        self.green_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_pips = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.green_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.red_disposable = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

    def prepare_disposable(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.green_disposable[i][j][k] = self.green_pips[i][j][k]
                    self.red_disposable[i][j][k] = self.red_pips[i][j][k]

    def round_start(self):
        self.turn += 1
        for i in range(0, self.new_pips):
            self.red_pips[random.randint(0, 2)][random.randint(0, 2)][random.randint(0, 2)] += 1
            self.green_pips[random.randint(0, 2)][random.randint(0, 2)][random.randint(0, 2)] += 1

    def get_moves(self):
        self.prepare_disposable()
        self.green_move = self.green_player.play(self.green_disposable, self.red_disposable, self.green_score, self.red_score, self.turn, self.game_length, self.new_pips)
        self.prepare_disposable()
        self.red_move = self.red_player.play(self.red_disposable,self.green_disposable, self.red_score, self.green_score, self.turn, self.game_length, self.new_pips)
        if not isinstance(self.green_move, list):
            raise Exception("Green Player's move is not a list: " + str(self.green_move))
        if not isinstance(self.red_move, list):
            raise Exception("Red Player's move is not a list: " + str(self.red_move))
        if not len(self.green_move) == 3:
            raise Exception("Green Player's move's length has to be 3: " + str(self.green_move))
        if not len(self.red_move) == 3:
            raise Exception("Red Player's move's length has to be 3: " + str(self.red_move))
        for i in range(3):
            if self.green_move[i] > 2 or self.green_move[i] < 0:
                raise Exception("Green Player's move is not between 0 and 2: " + str(self.green_move))
            if self.red_move[i] > 2 or self.red_move[i] < 0:
                raise Exception("Red Player's move is not between 0 and 2: " + str(self.red_move))

    def update_score(self):
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    if not (i == self.red_move[0] or i == self.green_move[0] or j == self.red_move[1] or j == self.green_move[1] or k == self.red_move[2] or k == self.green_move[2]):
                        self.red_score = self.red_score + self.red_pips[i][j][k]
                        self.green_score = self.green_score + self.green_pips[i][j][k]
                        self.red_pips[i][j][k] = 0
                        self.green_pips[i][j][k] = 0
        self.green_move = None
        self.red_move = None

    def play_round(self):
        self.round_start()
        self.get_moves()
        self.update_score()

    def play(self):
        while self.turn < self.game_length:
            self.play_round()
        return [self.green_score, self.red_score]

    def fancy_state_print(self, stdscr):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    if self.red_pips[k][i][j] > 0:
                        if self.red_pips[k][i][j] < 10:
                            s = " " + str(self.red_pips[k][i][j])
                        else:
                            s = str(self.red_pips[k][i][j])
                        stdscr.addstr(i+3, 25*k + 6*j + 8 , s,curses.color_pair(1))
                    else:
                        stdscr.addstr(i+3, 25*k + 6*j + 8 , " .",)
                    if self.green_pips[k][i][j] > 0:
                        if self.green_pips[k][i][j] < 10:
                            s = str(self.green_pips[k][i][j]) + " "
                        else:
                            s = str(self.green_pips[k][i][j])
                        stdscr.addstr( s,curses.color_pair(2))
                    else:
                        stdscr.addstr( ". ",)
                    # if self.green_pips[k][i][j] > 0:
                        # stdscr.addstr('{}'.format(self.green_pips[k][i][j]),curses.color_pair(2))
                    # else:
                        # stdscr.addstr(". ")
        stdscr.refresh()

    def fancy_state_highlight(self, stdscr):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    if not (k == self.red_move[0] or k == self.green_move[0] or i == self.red_move[1] or i == self.green_move[1] or j == self.red_move[2] or j == self.green_move[2]):
                        if self.red_pips[k][i][j] > 0:
                            if self.red_pips[k][i][j] < 10:
                                s = " " + str(self.red_pips[k][i][j])
                            else:
                                s = str(self.red_pips[k][i][j])
                            stdscr.addstr(i+3, 25*k + 6*j + 8 , s,curses.color_pair(3))
                        else:
                            stdscr.addstr(i+3, 25*k + 6*j + 8 , " .",curses.color_pair(5))
                        if self.green_pips[k][i][j] > 0:
                            if self.green_pips[k][i][j] < 10:
                                s = str(self.green_pips[k][i][j]) + " "
                            else:
                                s = str(self.green_pips[k][i][j])
                            stdscr.addstr(s,curses.color_pair(4))
                        else:
                            stdscr.addstr(". ",curses.color_pair(5))
        stdscr.refresh()

    def fancy_print_moves(self, stdscr):
        stdscr.addstr(8, 20 ,str(self.red_move[0]+1)+str(self.red_move[1]+1)+str(self.red_move[2]+1),curses.color_pair(1))
        stdscr.addstr(9, 20 ,str(self.green_move[0]+1)+str(self.green_move[1]+1)+str(self.green_move[2]+1),curses.color_pair(2))

    def fancy_delete_moves(self, stdscr):
        stdscr.addstr(8, 20 ,"   ")
        stdscr.addstr(9, 20 ,"   ")

    def fancy_print_score(self, stdscr):
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
        stdscr.addstr(9, 37 , rs, curses.color_pair(1))
        stdscr.addstr(" - ")
        stdscr.addstr(gs, curses.color_pair(2))

    def fancy_play_round(self, stdscr):
        self.round_start()
        self.fancy_state_print(stdscr)
        self.get_moves()
        self.fancy_print_moves(stdscr)
        self.fancy_state_highlight(stdscr)
        stdscr.getkey()
        self.update_score()
        self.fancy_delete_moves(stdscr)
        self.fancy_print_score(stdscr)
        stdscr.getkey()

    def fancy_play(self, stdscr):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)
        if isinstance(self.green_player, HumanPlayer):
            self.green_player.set_params(stdscr, curses.color_pair(2))
        if isinstance(self.red_player, HumanPlayer):
            self.red_player.set_params(stdscr, curses.color_pair(1))
        stdscr.clear()
        stdscr.addstr(8, 8 , "Red move:   ", curses.color_pair(1))
        stdscr.addstr(9, 8 , "Green move: ", curses.color_pair(2))
        stdscr.addstr(8, 30 , "Round: ")
        stdscr.addstr(9, 30 , "Score: ")
        while self.turn < self.game_length:
            stdscr.addstr(8, 39 , "      ")
            stdscr.addstr(8, 39 , str(self.turn + 1) + " / " + str(self.game_length))
            self.fancy_play_round(stdscr)



if __name__ == "__main__":
    pA = HumanPlayer()
    pB = DeterminedPlayer()
    g = Game(pA, pB, 12, 10)
    curses.wrapper(g.fancy_play)
