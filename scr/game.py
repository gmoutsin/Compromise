import curses
import random
from players import HumanPlayer


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

    def reset_game(self):
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

    def new_players(self, player_a, player_b):
        self.red_player = player_a
        self.green_player = player_b
        self.reset_game()

    def prepare_disposable(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.green_disposable[i][j][k] = self.green_pips[i][j][k]
                    self.red_disposable[i][j][k] = self.red_pips[i][j][k]

    def round_start(self):
        self.turn += 1
        if self.type == "s":
            for _ in range(0, self.new_pips):
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

    def get_moves(self):
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
            self.prepare_disposable()
            self.red_move = self.red_player.play(
                self.red_disposable,
                self.green_disposable,
                self.red_score,
                self.green_score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.prepare_disposable()
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

    def update_score(self):
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

    def play_round(self):
        self.round_start()
        self.get_moves()
        self.update_score()

    def play(self):
        while self.turn < self.game_length or (
            self.no_ties and self.red_score == self.green_score
        ):
            self.play_round()
        return [self.red_score, self.green_score]

    def fancy_state_print(self, stdscr):
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

    def fancy_state_highlight(self, stdscr):
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

    def fancy_print_moves(self, stdscr):
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

    def fancy_delete_moves(self, stdscr):
        stdscr.addstr(8, 20, "   ")
        stdscr.addstr(9, 20, "   ")

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
        stdscr.addstr(9, 37, rs, curses.color_pair(1))
        stdscr.addstr(" - ")
        stdscr.addstr(gs, curses.color_pair(2))

    def fancy_round_start(self, stdscr):
        self.turn += 1
        if self.type == "s":
            for _ in range(0, self.new_pips):
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

    def fancy_play_round(self, stdscr):
        self.fancy_round_start(stdscr)
        self.fancy_state_print(stdscr)
        self.get_moves()
        self.fancy_print_moves(stdscr)
        self.fancy_state_highlight(stdscr)
        stdscr.getkey()
        self.update_score()
        self.fancy_delete_moves(stdscr)
        self.fancy_print_score(stdscr)
        self.fancy_state_print(stdscr)
        stdscr.getkey()

    def fancy_play(self, stdscr):
        curses.mousemask(1)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)
        if isinstance(self.green_player, HumanPlayer):
            self.green_player.set_params(
                stdscr,
                curses.color_pair(2),
                curses.color_pair(4),
                curses.color_pair(0),
                1,
            )
        if isinstance(self.red_player, HumanPlayer):
            self.red_player.set_params(
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
        self.fancy_state_print(stdscr)
        # while True:
        # key = stdscr.getch()
        # stdscr.addstr(0,0,str(key) + "   ")
        while self.turn < self.game_length or (
            self.no_ties and self.red_score == self.green_score
        ):
            stdscr.addstr(8, 39, "      ")
            stdscr.addstr(8, 39, str(self.turn + 1) + " / " + str(self.game_length))
            self.fancy_play_round(stdscr)
        if self.red_score > self.green_score:
            stdscr.addstr(9, 50, "Player 1 won!       ", curses.color_pair(1))
        elif self.red_score < self.green_score:
            stdscr.addstr(9, 50, "Player 2 won!       ", curses.color_pair(2))
        else:
            stdscr.addstr(9, 50, "Game tied!          ", curses.color_pair(0))
        stdscr.getkey()
