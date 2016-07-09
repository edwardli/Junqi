# Edward Li (eal87@cornell.edu)
# jqmodels.py
# TODO: Add some indicator that siling has fallen for flag reveal. Allow for setup stage. Make winning conditions.

# IMPORTS
from jqconstants import *
import random

# CLASSES
class Board(object):
    """The game board. The board contains all visitable nodes, and references to all
    of the pieces on the board. It also contains methods to move and capture.
    
    ATTRIBUTES:
    _positions      a 2d list (a list of rows) containing references to every position.
    _turn           bool or None. Player 1's turn = True, Player 2's turn = False
    _prev_turn      None or the previous turn. while _turn is None
    """
    
    # GETTERS AND SETTERS
    def getPositions(self):
        """Returns: _positions DIRECTLY. Does not make a copy."""
        return self._positions
    
    def getTurn(self):
        return self._turn
    
    def getPrevTurn(self):
        return self._prev_turn
    
    def setPrevTurn(self, turn):
        assert type(turn) == bool or turn is None
        self._prev_turn = turn
    
    def setTurn(self, turn):
        assert type(turn) == bool or turn is None
        self._turn = turn
    
    
    # INITIALIZER
    def __init__(self, turn=None, randomize=False):
        # assert positions is a valid list a positions
        assert type(turn) == bool or turn is None
        
        self._positions = make_board()
        self._turn      = turn
        if type(turn) != bool:
            self._prev_turn = PLAYER2
        if randomize:
            self.randomInit()
    
    
    # METHODS
    # ideas for methods: move, attack, is_legal_move
    
    # MOVE AND CHECK MOVE
    def movePiece(self, start, end):    # future features: siling death flag reveal, more detailed return information
        """Returns: True if piece moved legally, False if requested move is illegal.
        
        Moves a piece from position start to position end, if legal. Adjusts turn.
        
        Precondition: start and end are lists of ints of length 2."""
        assert type(start) == list and type(end) == list
        assert len(start) == 2 and len(end) == 2            # incomplete assertion; did not assert ints
        print str(start)+' to '+str(end)
        
        origin  = self.getPositions()[start[1]][start[0]]
        dest = self.getPositions()[end[1]][end[0]]
        movetype = self._checkMoveType(origin,dest)
        
        if movetype == ILLEGAL:
            return False
        
        elif movetype == MOVE:
            dest.setPiece(origin.getPiece())
            origin.setPiece(None)
        
        else:   # attack
            if dest.getType() == BUNKER or origin.getPiece()[1] == dest.getPiece()[1]:
                return False

            piece1 = origin.getPiece()[0]
            piece2 = dest.getPiece()[0]
            
            if piece1 == BOMB or piece2 == BOMB:    # both destroyed if either is a bomb
                origin.setPiece(None)
                dest.setPiece(None)
            elif piece1 == 1 and piece2 == MINE:    # mine destroyed if attacker is a 1
                dest.setPiece(origin.getPiece())
                origin.setPiece(None)
            elif piece1 > piece2:   # last three elifs are normal fight circumstances
                dest.setPiece(origin.getPiece())
                origin.setPiece(None)
            elif piece1 < piece2:
                origin.setPiece(None)
            else:   # same value pieces
                origin.setPiece(None)
                dest.setPiece(None)
        
        self._prev_turn = self.getTurn()
        self.setTurn(None)
        return True
        
        
    def _checkMoveType(self, pos1, pos2):
        """Returns: Type of move about to be executed.
        
        Parameter pos1: position moving from
        Precondition: pos1 is a valid position
        
        Parameter pos2: position moving to
        Precondition: pos2 is a valid position
        """
        result = ILLEGAL
        valid_dests = []
        piece = pos1.getPiece()
        p1type = pos1.getType()
        x_coord = pos1.getCoords()[0]
        y_coord = pos1.getCoords()[1]
        if (piece is not None) and (piece[0] != MINE) and (piece[0] != FLAG):
            if p1type == HEADQUARTERS:
                pass    # valid_dests remains empty
            elif p1type == REGULAR:
                # only add positions that are within the board. check edges.
                if x_coord != len(self.getPositions()[0])-1:
                    valid_dests.append(self.getPositions()[y_coord][x_coord+1])
                if x_coord != 0:
                    valid_dests.append(self.getPositions()[y_coord][x_coord-1])
                if y_coord != len(self.getPositions())-1:
                    valid_dests.append(self.getPositions()[y_coord+1][x_coord])
                if y_coord != 0:
                    valid_dests.append(self.getPositions()[y_coord-1][x_coord])
            elif p1type == BUNKER:
                valid_dests.append(self.getPositions()[y_coord][x_coord+1])
                valid_dests.append(self.getPositions()[y_coord+1][x_coord+1])
                valid_dests.append(self.getPositions()[y_coord+1][x_coord])
                valid_dests.append(self.getPositions()[y_coord+1][x_coord-1])
                valid_dests.append(self.getPositions()[y_coord][x_coord-1])
                valid_dests.append(self.getPositions()[y_coord-1][x_coord-1])
                valid_dests.append(self.getPositions()[y_coord-1][x_coord])
                valid_dests.append(self.getPositions()[y_coord-1][x_coord+1])
            elif p1type == RAILROAD:   # railroad
                # railroad destinations
                if pos2.getType() == RAILROAD and self._existsPath(pos1, pos2):
                    valid_dests.append(pos2)
                # non-railroad destinations
                elif x_coord == 0:
                    if y_coord in [2,3,4,8,9,10]:
                        valid_dests.append(self.getPositions()[y_coord][x_coord+1])
                    if y_coord in [1,3,7,9]:
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord+1])
                    if y_coord in [3,5,9,11]:
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord+1])
                elif x_coord == 1 or x_coord == 3:
                    if y_coord in [1,7,11]:
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord])
                    if y_coord in [1,5,11]:
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord])
                elif x_coord == 2:
                    if y_coord in [1,7,11]:
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord-1])
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord])
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord+1])
                    if y_coord in [1,5,11]:
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord-1])
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord])
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord+1])
                else:   # x-coord == 4
                    if y_coord in [2,3,4,8,9,10]:
                        valid_dests.append(self.getPositions()[y_coord][x_coord-1])
                    if y_coord in [1,3,7,9]:
                        valid_dests.append(self.getPositions()[y_coord+1][x_coord-1])
                    if y_coord in [3,5,9,11]:
                        valid_dests.append(self.getPositions()[y_coord-1][x_coord-1])
            
            # if it's a valid move, modify the result appropriately
            if pos2 in valid_dests:
                if pos2.getPiece() is None:
                    result = MOVE
                else:
                    result = ATTACK
        
        return result
            
            
    def _existsPath(self, pos1, pos2):
        """Returns: True if there exists a clear path for a gongbing (1), false otherwise.
        
        Parameter pos1: the start position
        Precondition: pos1 is a valid position
        
        Parameter pos2: the end position
        Precondition: pos2 is a valid position
        """
        current_pos = pos1
        checked_pos = []
        options     = []
        is_one      = pos1.getPiece()[0] == 1
        
        while True: # loop most terminate eventually
            x_coord = current_pos.getCoords()[0]
            y_coord = current_pos.getCoords()[1]
            #print '(' + str(x_coord) + ', ' + str(y_coord) + ')'
            # for four points surrounding current_pos
            if x_coord < 4:
                potential_pos = self.getPositions()[y_coord][x_coord+1]
                if potential_pos.getType() == RAILROAD and potential_pos not in checked_pos:
                    if not ((not is_one) and (potential_pos.getCoords()[0] != pos1.getCoords()[0] and
                                              potential_pos.getCoords()[1] != pos1.getCoords()[1])):
                        if potential_pos is pos2:
                            return True
                        elif potential_pos.getPiece() == None:
                            options.append(potential_pos)
            if x_coord > 0:
                potential_pos = self.getPositions()[y_coord][x_coord-1]
                if potential_pos.getType() == RAILROAD and potential_pos not in checked_pos:
                    if not ((not is_one) and (potential_pos.getCoords()[0] != pos1.getCoords()[0] and
                                              potential_pos.getCoords()[1] != pos1.getCoords()[1])):
                        if potential_pos is pos2:
                            return True
                        elif potential_pos.getPiece() == None:
                            options.append(potential_pos)
            if y_coord < 11:
                potential_pos = self.getPositions()[y_coord+1][x_coord]
                if potential_pos.getType() == RAILROAD and potential_pos not in checked_pos:
                    if not ((not is_one) and (potential_pos.getCoords()[0] != pos1.getCoords()[0] and
                                              potential_pos.getCoords()[1] != pos1.getCoords()[1])):
                        if potential_pos is pos2:
                            return True
                        elif potential_pos.getPiece() == None:
                            options.append(potential_pos)
            if y_coord > 1:
                potential_pos = self.getPositions()[y_coord-1][x_coord]
                if potential_pos.getType() == RAILROAD and potential_pos not in checked_pos:
                    if not ((not is_one) and (potential_pos.getCoords()[0] != pos1.getCoords()[0] and
                                              potential_pos.getCoords()[1] != pos1.getCoords()[1])):
                        if potential_pos is pos2:
                            return True
                        elif potential_pos.getPiece() == None:
                            options.append(potential_pos)
            
            # check if destination is near; if not, move on
            if len(options) > 0:
                checked_pos.append(current_pos)
                current_pos = options.pop()
            else:
                return False
    
    def randomInit(self):
        """Randomizes the whole board.
        """
        self.randomInitP1()
        self.randomInitP2()
    
    
    def randomInitP1(self):
        """Randomizes the pieces of player 1.
        """
        bucket = PIECE_BUCKET[:]
        random.shuffle(bucket)
        for i in range(6):
            row = self.getPositions()[i]
            for position in row:
                if position.getType() != BUNKER:
                    position.setPiece([bucket.pop(), True])
                    
    def randomInitP2(self):
        """Randomizes the pieces of player 2.
        """
        bucket = PIECE_BUCKET[:]
        random.shuffle(bucket)
        for i in range(7,13):
            row = self.getPositions()[i]
            for position in row:
                if position.getType() != BUNKER:
                    position.setPiece([bucket.pop(), False])
    
                
    
    
class Position(object):
    """Represents a position. Contains the coordinates of the position as well as its
    type. Also classifies the rank of the piece on that position, if it exists.
    
    ATTRIBUTES:
    _coords         a list containing the position. Immutable.
    _type           int from 0..3. Immutable.
                    0 = headquarters, 1 = regular, 2 = railroad, 3 = bunker, 4 = mountain (inaccessible)
    _piece          List of size 2 or None. First elt is int 0..11 and second is bool, True or False.
                    0 = flag, 1-9 = ordinal pieces, 10 = mine, 11 = bomb. None = no piece
    """
    # GETTERS AND SETTERS
    def getCoords(self):
        """Returns: Coordinate list directly.
        """
        return self._coords
    
    def getType(self):
        return self._type
    
    def getPiece(self):
        return self._piece
    
    def getSide(self):
        return self._side
    
    def setPiece(self, piece):
        assert (type(piece) == list and len(piece) == 2) and (type(piece[0]) == int and type(piece[1]) == bool) or piece is None
        self._piece = piece
    
    
    # INITIALIZER
    def __init__(self, c, t, p=None):
        assert type(c) == list and len(c) == 2  # incomplete assert, does not check contents of c
        assert type(t) == int and 0 <= t <= 4
        
        self._coords = c
        self._type   = t
        self.setPiece(p)
    
    # STRING REPRESENTATION
    def __repr__(self):
        return "Piece "+(str(self._piece) if self._piece else 'X')+" at coords "+(str(self._coords))


# HELPER FUNCTIONS

# BOARD MAKER FUNCTIONS
def make_board():
    """Returns: A 2D of references to positions that in aggregate represent a board.
    Pieces are not included.
    """
    positions = []
    
    make_type1_row(positions,0)
    make_type2_row(positions,1)
    make_type3_row(positions,2)
    make_type4_row(positions,3)
    make_type3_row(positions,4)
    make_type2_row(positions,5)
    make_type5_row(positions,6)
    make_type2_row(positions,7)
    make_type3_row(positions,8)
    make_type4_row(positions,9)
    make_type3_row(positions,10)
    make_type2_row(positions,11)
    make_type1_row(positions,12)
    
    return positions


def make_type1_row(positions,row):
    """Appends a type 1 row (i.e. the first and last rows) of y-coordinate row to positions.
    
    Precondition: positions is a list
                  row is an int
    """
    type1_row = [Position([0,row],REGULAR), Position([1,row],HEADQUARTERS), Position([2,row],REGULAR),
                 Position([3,row],HEADQUARTERS), Position([4,row],REGULAR)]
    positions.append(type1_row)


def make_type2_row(positions,row):
    """Appends a type 2 row (i.e. full railroad rows) of y-coordinate row to positions.
    
    Precondition: positions is a list
                  row is an int
    """
    type2_row = [Position([0,row],RAILROAD), Position([1,row],RAILROAD), Position([2,row],RAILROAD),
                 Position([3,row],RAILROAD), Position([4,row],RAILROAD)]
    positions.append(type2_row)


def make_type3_row(positions,row):
    """Appends a type 3 row (i.e. rows 2,4,8,10) of y-coordinate row to positions.
    
    Precondition: positions is a list
                  row is an int
    """
    type3_row = [Position([0,row],RAILROAD), Position([1,row],BUNKER), Position([2,row],REGULAR),
                 Position([3,row],BUNKER), Position([4,row],RAILROAD)]
    positions.append(type3_row)


def make_type4_row(positions,row):
    """Appends a type 4 row (i.e. rows 3,9) of y-coordinate row to positions.
    
    Precondition: positions is a list
                  row is an int
    """
    type4_row = [Position([0,row],RAILROAD), Position([1,row],REGULAR), Position([2,row],BUNKER),
                 Position([3,row],REGULAR), Position([4,row],RAILROAD)]
    positions.append(type4_row)


def make_type5_row(positions,row):
    """Appends a type 5 row (i.e. row 6) of y-coordinate row to positions.
    
    Precondition: positions is a list
                  row is an int
    """
    type5_row = [Position([0,row],RAILROAD), Position([1,row],MOUNTAIN), Position([2,row],RAILROAD),
                 Position([3,row],MOUNTAIN), Position([4,row],RAILROAD)]
    positions.append(type5_row)