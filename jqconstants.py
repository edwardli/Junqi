# Edward Li (eal87@cornell.edu)
# jqconstants.py

"""BOARD CONSTANTS"""
B_WIDTH     = 690
B_HEIGHT    = 555

"""POSITION TYPES"""
HEADQUARTERS = 0
REGULAR      = 1
BUNKER       = 2
RAILROAD     = 3
MOUNTAIN     = 4

"""PIECE TYPES"""
FLAG = 0
MINE = 10
BOMB = 11
# Pieces 1-9 are simply referred to by their numbers.

PIECE_BUCKET    = [0,1,1,1,2,2,2,3,3,3,4,4,5,5,6,6,7,7,8,9,10,10,10,11,11]

"""TURNS"""
PLAYER1 = True
PLAYER2 = False

"""MOVE TYPES"""
ILLEGAL = 0
MOVE    = 1
ATTACK  = 2

"""DISPLAY"""
BLACK   = (0,0,0)
X_CTR   = [25,112.5,200,287.5,375]
Y_CTR   = [540,498,456,414,372,330,277.5,225,183,141,99,57,15]
PIECE_WIDTH = 58
PIECE_HEIGHT = 38