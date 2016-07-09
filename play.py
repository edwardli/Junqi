from jqconstants import *
import jqmodels
import pygame
import sys


class Junqi(object):
    """The controller class for the Junqi app.
    
    INSTANCE ATTRIBUTES:
        _view: the game view
        _board: the game board
        _pieces: the game pieces, in list form
        _pos_rects: a list rects for all positions
        _piece_images: loaded images of all pieces
        
        _game: the BACKEND game board and all associated positions
        
        _prev_pressed: whether or not the left mouse button was pressed in the previous frame. True or False.
        _selected: current selected piece. None, or coords of selected piece.
    """
    def __init__(self):
        print 'Initializing pygame...'
        pygame.init()
        print 'Setting up display...'
        pygame.display.set_caption('Junqi')
        self._view = pygame.display.set_mode((B_WIDTH,B_HEIGHT))
        print 'Loading board...'
        self._board = pygame.image.load('images/junqiboard.jpg')
        self._game  = jqmodels.Board(randomize=True)
        
        # fancy list flattening from http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        print 'Loading piece images...'
        self._piece_images = [pygame.image.load('images/jq00.jpg'),pygame.image.load('images/jq01.jpg'),pygame.image.load('images/jq02.jpg'),
                              pygame.image.load('images/jq03.jpg'),pygame.image.load('images/jq04.jpg'),pygame.image.load('images/jq05.jpg'),
                              pygame.image.load('images/jq06.jpg'),pygame.image.load('images/jq07.jpg'),pygame.image.load('images/jq08.jpg'),
                              pygame.image.load('images/jq09.jpg'),pygame.image.load('images/jq10.jpg'),pygame.image.load('images/jq11.jpg')]
        self._pieces = []
        self._pos_rects = self._setupRects()
        self._prev_pressed = False
        self._selected = None
        
        

    def update(self):
        """Updates all backend.
        """
        # piece selection
        lmb = pygame.mouse.get_pressed()[0]
        if lmb and not self._prev_pressed:
            if self._game.getTurn() is None:
                self._game.setTurn(not self._game.getPrevTurn())
                self._game.setPrevTurn(None)
            else:
                mouse_pos = pygame.mouse.get_pos()
                for rect in self._pos_rects:
                    if rect[0].collidepoint(mouse_pos):
                        if self._selected is not None:
                            result = self._game.movePiece(self._selected,rect[1])
                            self._selected = None
                        else:
                            self._selected = rect[1]
        
        self._prev_pressed = lmb
        
    def draw(self):
        """Clears the window and redraws board, pieces. Then updates the display.
        """
        self._pieces = [item for sublist in self._game.getPositions() for item in sublist]
        
        self._view.fill(BLACK)
        self._view.blit(self._board,(0,0))
        
        for piece in self._pieces:
            if piece.getPiece() is not None:
                x_px = X_CTR[piece.getCoords()[0]]
                y_px = Y_CTR[piece.getCoords()[1]]
                
                side       = piece.getPiece()[1]
                rank       = piece.getPiece()[0]
                if self._game.getTurn() == side:
                    surface    = self._piece_images[rank]
                    rect       = surface.get_rect(center=(x_px,y_px))
                    self._view.blit(surface, rect)
                else:
                    rect = pygame.Rect(x_px-PIECE_WIDTH/2.0,y_px-PIECE_HEIGHT/2.0,PIECE_WIDTH,PIECE_HEIGHT)
                    pygame.draw.rect(self._view, (0,0,255) if side else (0,255,0), rect)
                    
                
        
        if self._selected is not None:
            rect = pygame.Rect(X_CTR[self._selected[0]]-PIECE_WIDTH/2.0,Y_CTR[self._selected[1]]-PIECE_HEIGHT/2.0,
                               PIECE_WIDTH,PIECE_HEIGHT)
            pygame.draw.rect(self._view, (255,0,255), rect, 5)
        
    # HELPER FUNCTIONS
    def _setupRects(self):
        """Sets up invisible rects for each position
        """
        rect_list = []
        for row in range(13):
            for column in range(5):
                x_px = X_CTR[column] - PIECE_WIDTH/2.0
                y_px = Y_CTR[row] - PIECE_HEIGHT/2.0
                rect = pygame.Rect(x_px,y_px,PIECE_WIDTH,PIECE_HEIGHT)
                rect_list.append([rect,[column,row]])
        return rect_list



if __name__ == '__main__':
    game = Junqi()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game.update()
        game.draw()
        pygame.display.flip()