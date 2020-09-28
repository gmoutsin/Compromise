# Compromise
###### A simple game to be used in machine learning teaching

## Rules

There are three versions of the game.

### Complex Game

There are two players and 3 3x3 grids. In the beginning of each turn each player receives the same amount of pips and then places them on the grid in on any location and any combination. Players do this without seeing the choices of their opponent. After the pips are placed, the board will look something like this:

![pre-move](https://raw.githubusercontent.com/gmoutsin/Compromise/master/pictures/premove.png)

Then each player is asked to choose a move, i.e they choose one grid, one row and one column. This choice is given by 3 numbers, for example 123 refers to the first grid, the second row and the third column. Both players make this choice without knowing what their opponent chose.

Once both players choose, the choices are revealed. Then each grid, row and column that any player chose is "frozen". For example, if the first player chooses 123 and the second 213, then every position on the 1st and the 2nd grids are frozen. Moreover the 1st and the 2nd rows in every grid are frozen as well as the 3rd column of every grid. The non-frozen position will be highlighted:

![post-move](https://raw.githubusercontent.com/gmoutsin/Compromise/master/pictures/postmove.png)

Then the pips in the non-frozen positions are removed from the game and they are added to the player's respective score. In the above example the pips at positions (3,3,1) and (3,3,2) are collected:

![pre-move](https://raw.githubusercontent.com/gmoutsin/Compromise/master/pictures/score.png)

The game continues for a predetermined number of turns and the player with the most points win. Notice that pips are not removed between turns, only the pips that are scored are removed. There is an option in case of a tie to continue the game until one player scores more points than the other. 

### Simple Game

The rules are practically the same as in the complex version of the game. The only difference is that players do not choose where the pips should be placed, instead they are placed randomly.

### Gamble Game (to be added)

Just like the complex game with the only difference that the players do not choose the grids, rows and columns, this is chosen for them by the computer at random.

## Interface

### Player Classes

The script defined a player abstract class named `AbstractPlayer`. Any player class has to extend the abstract player class. This method takes as input the state of the game and outputs the player's move. The move has to be an array of length 3 and its elements can only be the numbers 0, 1 and 2. The method provided in  `AbstractPlayer` chooses a random move.

The abstract player class defines another method called `placePips`. This method takes as input the state of the game and outputs a list of coordinates of where the pips should be placed. Each coordinate should be an array of length 3 and its elements can only be the numbers 0, 1 and 2. The method provided in  `AbstractPlayer` places the pips randomly.

#### Predefined Players

There are 5 predefined players. The class `HumanPlayer` provides a way for a human to play the game. The pips are placed using the mouse and the placement is reset by pressing r. The move is should be a string of three numbers between 1 and 3 without any delimiters.

The rest of the players in order of difficulty are:

1. `RandomPlayer`
1. `DeterminedPlayer`
1. `GreedyPlayer`
1. `SmartGreedyPlayer`

All of the predefined players classes, place pips randomly. A human can easily win a complex game against any of them.

### Game Class

The game functionality is defined in the class `CompromiseGame`. The constructor takes two players, the number of pips given to the players each round, the length of the game, the type of the game (simple, complex or gamble, `"s"`, `"c"` or `"g"` respectively) and whether to accept ties. The last two values default to a simple game and non-acceptance of ties.

The method `resetGame` resets the variable and should be used after a game is finished and before a new one starts.

The method `newPlayers` resets the game and defines new players.

The method `play` plays the game and returns a 2-array with the score. Notice that if at least one of the players is an instance of the class `HumanPlayer`, this will throw an error.

The method `fancyPlay` should be used when at least one of the players is an instance of the class `HumanPlayer`. This method uses `curses` and I have tried it on linux and on Bash terminal on Windows 10. I'm not sure if it can be made to run natively in Windows and I hope it runs on macOS. The proper way to call this method is by wrapping it in `curses.wrapper`, see the script. Unless the script is modified, it will start a simple game with the first player being `HumanPlayer` and the second being `SmartGreedyPlayer`.

## Who has the rights for this game?

#### Short answer

I don't know.

#### Longer answer

This game is a modified version of a board game that a student created as an assignment for a board game design module in Warwick University. As such I do not know who has exactly what rights for this game. I am in the process of figuring this out, as well as finding the name of the student in order to give them credit. Until then assume that all rights are reserved.

The code was written solely by me and is shared under the GPL v3.0 license.



