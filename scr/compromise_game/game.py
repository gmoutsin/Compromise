import copy
import curses
import random
import itertools
from dataclasses import dataclass
from .engines import HumanPlayer, AbstractPlayer


def grid_ref_to_pixel_ref(grid, row, col):
    """turns row, col on a given grid to pixel x, y for wiriting with curses"""
    return (25 * grid) + (6 * col) + 8, row + 3


@dataclass
class Player:
    """dataclass that represents everything the game knows about a player"""

    engine: AbstractPlayer
    left_align: bool = False
    score: int = 0
    move: list[list[int]] = None
    pips: list[list[int]] = None

    def place_random_pip(self):
        """increment a random pip"""
        self.pips[random.randint(0, 2)][random.randint(0, 2)][random.randint(0, 2)] += 1

    def get_random_move(self):
        """generate a random game move"""
        self.move = [random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)]

    def get_engine_move(self, turn, game_len, new_pips, other):
        """pass game state to player engine and return engine calculated move"""
        self.move = self.engine.play(
            copy.deepcopy(self.pips),
            copy.deepcopy(other.pips),
            self.score,
            other.score,
            turn,
            game_len,
            new_pips,
        )

    def update_score(self, grid, row, col):
        """move pips in a given grid reference to own score"""
        self.score += self.pips[grid][row][col]
        self.pips[grid][row][col] = 0

    def formatted_value(self, grid, row, col):
        """string formatted output for own pips in a given grid reference"""
        value = self.pips[grid][row][col]
        if self.left_align:
            return f"{value:<2}"
        return f"{value:2}"


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

        self.red = Player(player_a)
        self.green = Player(player_b, True)  # set left_right = True
        self.new_pips = num_pips

        # initialise variables
        self.reset_game()

    def reset_game(self):
        """reset player and game variables"""
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
        """reset game and replace player engines"""
        self.red.engine = player_a
        self.green.engine = player_b
        self.reset_game()

    def round_start(self):
        """start a new game round, place player pips and increment turn"""
        self.turn += 1
        if self.type == "s":
            for _ in range(self.new_pips):
                self.red.place_random_pip()
                self.green.place_random_pip()
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
        """get and validate player moves (random or engine)"""
        if self.type == "g":
            self.red.get_random_move()
            self.green.get_random_move()
        else:
            self.red.get_engine_move(
                self.turn, self.game_length, self.new_pips, self.green
            )
            self.green.get_engine_move(
                self.turn, self.game_length, self.new_pips, self.red
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
        """play previously genergated/validated player moves"""
        for grid, row, col in itertools.product(range(3), repeat=3):
            if not (
                grid == self.red.move[0]
                or grid == self.green.move[0]
                or row == self.red.move[1]
                or row == self.green.move[1]
                or col == self.red.move[2]
                or col == self.green.move[2]
            ):
                self.red.update_score(grid, row, col)
                self.green.update_score(grid, row, col)
        self.green.move = None
        self.red.move = None

    def play_round(self):
        """do a whole round:
        - place player pips
        - get player moves
        - play those moves
        """
        self.round_start()
        self.get_moves()
        self.update_score()

    def play(self):
        """play the whole game. Keep track of how many turns have been played"""
        while self.turn < self.game_length or (
            self.no_ties and self.red.score == self.green.score
        ):
            self.play_round()
        return [self.red.score, self.green.score]

    def fancy_state_print(self, stdscr):
        """formated game state output using curses"""
        for grid, row, col in itertools.product(range(3), repeat=3):
            pixel_x, pixel_y = grid_ref_to_pixel_ref(grid, row, col)
            if self.red.pips[grid][row][col] > 0:
                stdscr.addstr(
                    pixel_y,
                    pixel_x,
                    self.red.formatted_value(grid, row, col),
                    curses.color_pair(1),
                )
            else:
                stdscr.addstr(
                    pixel_y,
                    pixel_x,
                    " .",
                )
            if self.green.pips[grid][row][col] > 0:
                stdscr.addstr(
                    self.green.formatted_value(grid, row, col), curses.color_pair(2)
                )
            else:
                stdscr.addstr(". ")
            # if self.green.pips[k][i][j] > 0:
            # stdscr.addstr('{}'.format(self.green.pips[k][i][j]),curses.color_pair(2))
            # else:
            # stdscr.addstr(". ")
        stdscr.refresh()

    def fancy_state_highlight(self, stdscr):
        """highlight non-frozen grid squares"""
        for grid, row, col in itertools.product(range(3), repeat=3):
            pixel_x, pixel_y = grid_ref_to_pixel_ref(grid, row, col)
            if not (
                grid == self.red.move[0]
                or grid == self.green.move[0]
                or row == self.red.move[1]
                or row == self.green.move[1]
                or col == self.red.move[2]
                or col == self.green.move[2]
            ):
                if self.red.pips[grid][row][col] > 0:
                    stdscr.addstr(
                        pixel_y,
                        pixel_x,
                        self.red.formatted_value(grid, row, col),
                        curses.color_pair(3),
                    )
                else:
                    stdscr.addstr(pixel_y, pixel_x, " .", curses.color_pair(5))
                if self.green.pips[grid][row][col] > 0:
                    stdscr.addstr(
                        self.green.formatted_value(grid, row, col), curses.color_pair(4)
                    )
                else:
                    stdscr.addstr(". ", curses.color_pair(5))
        stdscr.refresh()

    def fancy_print_moves(self, stdscr):
        """formatted output of player moves using curses"""
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
        """hide player moves from the screen, using curses"""
        stdscr.addstr(8, 20, "   ")
        stdscr.addstr(9, 20, "   ")

    def fancy_print_score(self, stdscr):
        """formatted output of player scores, using curses"""
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
        self.round_start()

    def fancy_play_round(self, stdscr):
        """do a whole round:
        - place player pips
        - get player moves
        - play those moves

        while also doing formatted curses output and input
        """
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
        """play the whole game. Keep track of how many turns have been played

        while also doing formatted curses output and input
        """
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
