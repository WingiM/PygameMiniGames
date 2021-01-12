# PygameMiniGames
Pygame project for Yandex Lyceum 2020-2021. Includes 5 mini-games for two players: Airhockey, Sea Battle, Tic Tac Toe, Sumo and Steal The Diamond

To install all required libraries use "pip install -r requirements.txt" command in cmd.exe (Windows)

The main file to start is main.py.

Also you can edit constants.py to change some game experience.

You can change images and sounds used in the games by replacing them in "data"/"sounds" directories. 
If you want to keep the original ones you can just add your images or sounds into the directories and change the names in constants.py

Guides:
1. Sea Battle:
The meaning of symbols in the arrangement: "." means an empty space, "#" means a ship/ship part. A complete arrangement has no oblique or angular ships.
Also it must include 4 one-tiled, 3 two-tiled, 2 three-tiled and 1 four-tiled ships.

2. Air Hockey:
Left player controls his stick by pressing WASD buttons, right player controls with arrow keys. The objective is to score a puck into your opponent's goal.

3. Sumo:
Player on the top can move by pressing W button, the bottom one is controlled by pressing Up. The goal is to push your opponent out of the field.

4. Steal The Diamond:
Left player can move his hand by pressing W button and the right one by pressing Up button. The goal is to steal the diamond faster than your opponent.
