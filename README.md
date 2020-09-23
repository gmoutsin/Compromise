# Compromise
###### A simple game to be used in machine learning teaching

## Rules

There are two versions of the game.

### Complex Game

There are 2 players and 3 3x3 grids. In the beginning of the turn each player receives a pool of pips and then places them on the grid in any combination. Players do this without seeing the choices of their opponent.

After the pips are placed, each player takes their move, i.e they choose one grid, one row and one column. This choise is given by 3 numbers, for example 123 refers to the first grid, the second row and the third column. Both players make this choice without knowing what their opponet chose.

Once both players choose, the choices are revealed. Then each grid, row and column that any player chose is "frozen". For example, if the first player chooses 123 and the second 213, then every position on the first and the second grids are frozen. Moreover the first and the second row in the third grid is frozen as well as the third row.

Then the pips in the non-frozen positions are collected and are added to the player's respective score. In the above example the pips at positions (3,3,1) and (3,3,2) are collected.

The game continues for a predetermined number of turns and the player with the most points win. There is an option in case of a tie to continue the game until one player scores more points than the other. 

### Simple Game

The rules are practically the same as in the complex version of the game. The only difference is that players do not choose where the pips should be placed, instead they are placed randomly.

### Gamble Game (to be added)

Just like the complex game with the only difference that the players do not choose the grids, rows and columns, this is chosen for them by the computer at random.

## Interface

### Player Classes

The script defined a player abstract class named `AbstractPlayer`. Any player class has to extend the abstract player class and define a method named `play`. This method takes as input the state of the game and outputs the player's move. The move has to be an array of length 3 and its elements can only be the numbers 0, 1 and 2.

The abstract player class defines another mathod called `placePips`. This method takes as input the state of the game and outputs a list of coordinates of where the pips should be placed. Each coordinate should be an array of length 3 and its elements can only be the numbers 0, 1 and 2. The method provided in  `AbstractPlayer` places the pips randomly.

#### Predefined Players

There are 5 predefined players. The class `HumanPlayer` provides a way for a human to play the game. The rest of the players in order of difficulty are:

1. `RandomPlayer`
1. `DeterminedPlayer`
1. `GreedyPlayer`
1. `SmartGreedyPlayer`

All of the predefined players classes, place pips randomly. A human can easily win a complex game against any of them.

### Game Class

The game functionality is defined in the class `CompromiseGame`. The constractor takes two players, the number of pips given to the players each round, the length of the game, whether it should be a simple or a complex game and whether to accept ties. The last two values default to a simple game and non acceptance of ties.

The method `resetGame` resets the variable and should be used after a game is finished and before a new one starts.

The method `newPlayers` resets the game and defines new players.

The method `play` plays the game and returns a 2-array with the score. Notice that if at least one of the players is an instance of the class `HumanPlayer`, this will throw an error.

The method `fancyPlay` should be used when at least one of the players is an instance of the class `HumanPlayer`. This method uses `curses` and I have tried it on linux and on Bash termimal on Windows 10. I'm not sure if it can be made to run natively in Windows and I hope it runs on macOS. The proper way to call this method is by wrapping it in `curses.wrapper`, see the script. Unless the script is modified, it will start a simple game with the first player being `HumanPlayer` and the second being `SmartGreedyPlayer`.

## Who has the rights for this game?

#### Short answer

I don't know.

#### Longish answer

This game is a modified version of a board game that a student created as an assignment for a board game design module in Warwick University. As such I do not know who has exactly what rights for this game. I am in the process of figuring this out, as well as finding the name of the student in order to give them credit. Until then assume that all rights are reserved.

The code was written solely by me and is shared under the GPL v3.0 licence.
