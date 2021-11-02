import copy
import curses
import random
import itertools
from dataclasses import dataclass
from .players import HumanPlayer, AbstractPlayer


def increment_random_pip(pips):
    """randomly increment a pip in a given list"""
    pips[random.randint(0, 2)][random.randint(0, 2)][random.randint(0, 2)] += 1


@dataclass
class Player:
    color: str
    move: list[list[int]]
    pips: list[list[int]]
    score: int
    engine: AbstractPlayer


class CompromiseGame:
    """the compromise game class

    keeps track of game state and contains all game logic
    """

    def __init__(
        self, player_a, player_b, num_pips, length, game_type="s", no_ties=True
    ):
        # in practice the if the game type is not "s" or "g" then it is complex

        # game settings
        self.no_ties = no_ties
        self.type = game_type
        self.game_length = length

        self.red = Player("red", None, None, 0, player_a)
        self.green = Player("green", None, None, 0, player_b)
        self.new_pips = num_pips

        # initialise variables
        self.reset_game()

    def reset_game(self):
        self.turn = 0
        self.green.move = None
        self.red.move = None
        self.green.score = 0
        self.red.score = 0
        self.green.pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]
        self.red.pips = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

    def new_players(self, player_a, player_b):
        self.red.engine = player_a
        self.green.engine = player_b
        self.reset_game()

    def round_start(self):
        self.turn += 1
        if self.type == "s":
            for _ in range(self.new_pips):
                increment_random_pip(self.red.pips)
                increment_random_pip(self.green.pips)
        else:
            green_placing = self.green.engine.place_pips(
                copy.deepcopy(self.green.pips),
                copy.deepcopy(self.red.pips),
                self.green.score,
                self.red.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            red_placing = self.red.engine.place_pips(
                copy.deepcopy(self.red.pips),
                copy.deepcopy(self.green.pips),
                self.red.score,
                self.green.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )

            for grid, row, col in green_placing:
                self.green.pips[grid][row][col] += 1

            for grid, row, col in red_placing:
                self.red.pips[grid][row][col] += 1

    def get_moves(self):
        if self.type == "g":
            self.red.move = [
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(0, 2),
            ]
            self.green.move = [
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(0, 2),
            ]
        else:
            self.red.move = self.red.engine.play(
                copy.deepcopy(self.red.pips),
                copy.deepcopy(self.green.pips),
                self.red.score,
                self.green.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.green.move = self.green.engine.play(
                copy.deepcopy(self.green.pips),
                copy.deepcopy(self.red.pips),
                self.green.score,
                self.red.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            if not isinstance(self.green.move, list):
                raise Exception(
                    "Green Player's move is not a list: " + str(self.green.move)
                )
            if not isinstance(self.red.move, list):
                raise Exception(
                    "Red Player's move is not a list: " + str(self.red.move)
                )
            if not len(self.green.move) == 3:
                raise Exception(
                    "Green Player's move's length has to be 3: " + str(self.green.move)
                )
            if not len(self.red.move) == 3:
                raise Exception(
                    "Red Player's move's length has to be 3: " + str(self.red.move)
                )
            for i in range(3):
                if self.green.move[i] > 2 or self.green.move[i] < 0:
                    raise Exception(
                        "Green Player's move is not between 0 and 2: "
                        + str(self.green.move)
                    )
                if self.red.move[i] > 2 or self.red.move[i] < 0:
                    raise Exception(
                        "Red Player's move is not between 0 and 2: "
                        + str(self.red.move)
                    )

    def update_score(self):
        for grid, row, col in itertools.product(range(3), repeat=3):
            if not (
                grid == self.red.move[0]
                or grid == self.green.move[0]
                or row == self.red.move[1]
                or row == self.green.move[1]
                or col == self.red.move[2]
                or col == self.green.move[2]
            ):
                self.red.score = self.red.score + self.red.pips[grid][row][col]
                self.green.score = self.green.score + self.green.pips[grid][row][col]
                self.red.pips[grid][row][col] = 0
                self.green.pips[grid][row][col] = 0
        self.green.move = None
        self.red.move = None

    def play_round(self):
        self.round_start()
        self.get_moves()
        self.update_score()

    def play(self):
        while self.turn < self.game_length or (
            self.no_ties and self.red.score == self.green.score
        ):
            self.play_round()
        return [self.red.score, self.green.score]

    def fancy_state_print(self, stdscr):
        for grid, row, col in itertools.product(range(3), repeat=3):
            if self.red.pips[grid][row][col] > 0:
                if self.red.pips[grid][row][col] < 10:
                    value = " " + str(self.red.pips[grid][row][col])
                else:
                    value = str(self.red.pips[grid][row][col])
                stdscr.addstr(
                    row + 3,
                    (25 * grid) + (6 * col) + 8,
                    value,
                    curses.color_pair(1),
                )
            else:
                stdscr.addstr(
                    row + 3,
                    (25 * grid) + (6 * col) + 8,
                    " .",
                )
            if self.green.pips[grid][row][col] > 0:
                if self.green.pips[grid][row][col] < 10:
                    value = str(self.green.pips[grid][row][col]) + " "
                else:
                    value = str(self.green.pips[grid][row][col])
                stdscr.addstr(value, curses.color_pair(2))
            else:
                stdscr.addstr(". ")
            # if self.green.pips[k][i][j] > 0:
            # stdscr.addstr('{}'.format(self.green.pips[k][i][j]),curses.color_pair(2))
            # else:
            # stdscr.addstr(". ")
        stdscr.refresh()

    def fancy_state_highlight(self, stdscr):
        for grid, row, col in itertools.product(range(3), repeat=3):
            if not (
                grid == self.red.move[0]
                or grid == self.green.move[0]
                or row == self.red.move[1]
                or row == self.green.move[1]
                or col == self.red.move[2]
                or col == self.green.move[2]
            ):
                if self.red.pips[grid][row][col] > 0:
                    if self.red.pips[grid][row][col] < 10:
                        value = " " + str(self.red.pips[grid][row][col])
                    else:
                        value = str(self.red.pips[grid][row][col])
                    stdscr.addstr(
                        row + 3,
                        (25 * grid) + (6 * col) + 8,
                        value,
                        curses.color_pair(3),
                    )
                else:
                    stdscr.addstr(
                        row + 3, (25 * grid) + (6 * col) + 8, " .", curses.color_pair(5)
                    )
                if self.green.pips[grid][row][col] > 0:
                    if self.green.pips[grid][row][col] < 10:
                        value = str(self.green.pips[grid][row][col]) + " "
                    else:
                        value = str(self.green.pips[grid][row][col])
                    stdscr.addstr(value, curses.color_pair(4))
                else:
                    stdscr.addstr(". ", curses.color_pair(5))
        stdscr.refresh()

    def fancy_print_moves(self, stdscr):
        stdscr.addstr(
            8,
            20,
            str(self.red.move[0] + 1)
            + str(self.red.move[1] + 1)
            + str(self.red.move[2] + 1),
            curses.color_pair(1),
        )
        stdscr.addstr(
            9,
            20,
            str(self.green.move[0] + 1)
            + str(self.green.move[1] + 1)
            + str(self.green.move[2] + 1),
            curses.color_pair(2),
        )

    @staticmethod
    def fancy_delete_moves(stdscr):
        stdscr.addstr(8, 20, "   ")
        stdscr.addstr(9, 20, "   ")

    def fancy_print_score(self, stdscr):
        red_score = ""
        # gs = ""
        # if self.green.score < 100:
        # if self.green.score < 10:
        # gs = "  " + str(self.green.score)
        # else:
        # gs = " " + str(self.green.score)
        # else:
        # gs = str(self.green.score)
        green_score = str(self.green.score)
        if self.red.score < 100:
            if self.green.score < 10:
                red_score = "  " + str(self.red.score)
            else:
                red_score = " " + str(self.red.score)
        else:
            red_score = str(self.red.score)
        stdscr.addstr(9, 37, red_score, curses.color_pair(1))
        stdscr.addstr(" - ")
        stdscr.addstr(green_score, curses.color_pair(2))

    def fancy_round_start(self, stdscr):
        self.turn += 1
        if self.type == "s":
            for _ in range(0, self.new_pips):
                self.red.pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
                self.green.pips[random.randint(0, 2)][random.randint(0, 2)][
                    random.randint(0, 2)
                ] += 1
        else:
            self.fancy_state_print(stdscr)
            red_placing = self.red.engine.place_pips(
                copy.deepcopy(self.red.pips),
                copy.deepcopy(self.green.pips),
                self.red.score,
                self.green.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            self.fancy_state_print(stdscr)
            green_placing = self.green.engine.place_pips(
                copy.deepcopy(self.green.pips),
                copy.deepcopy(self.red.pips),
                self.green.score,
                self.red.score,
                self.turn,
                self.game_length,
                self.new_pips,
            )
            for grid, row, col in green_placing:
                self.green.pips[grid][row][col] += 1
            for grid, row, col in red_placing:
                self.red.pips[grid][row][col] += 1

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
        if isinstance(self.green.engine, HumanPlayer):
            self.green.engine.set_params(
                stdscr,
                curses.color_pair(2),
                curses.color_pair(4),
                curses.color_pair(0),
                1,
            )
        if isinstance(self.red.engine, HumanPlayer):
            self.red.engine.set_params(
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
            self.no_ties and self.red.score == self.green.score
        ):
            stdscr.addstr(8, 39, "      ")
            stdscr.addstr(8, 39, str(self.turn + 1) + " / " + str(self.game_length))
            self.fancy_play_round(stdscr)
        if self.red.score > self.green.score:
            stdscr.addstr(9, 50, "Player 1 won!       ", curses.color_pair(1))
        elif self.red.score < self.green.score:
            stdscr.addstr(9, 50, "Player 2 won!       ", curses.color_pair(2))
        else:
            stdscr.addstr(9, 50, "Game tied!          ", curses.color_pair(0))
        stdscr.getkey()
