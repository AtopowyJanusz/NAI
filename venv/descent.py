# zródło problemu : https://www.codingame.com/ide/puzzle/the-descent ; zadanie wykonane przez Patrycję Bednarską

import sys
import math

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.


while True:
    height_of_mountain = {}
    for i in range(8):
        mountain_h = int(input())
        mountain_name = i
        height_of_mountain[i] = mountain_h
    sorted_height = sorted(height_of_mountain, key=height_of_mountain.get, reverse=True)
    object_to_shoot = sorted_height[0]

    print(object_to_shoot)