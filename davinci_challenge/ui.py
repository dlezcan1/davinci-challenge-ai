import pygame as pg
import math

# package imports
from game import Game, Board
import sprites


# TODO: pygame game application
class GameApplication:
    WIDTH, HEIGHT = 750, 750
    FPS = 30  # frames per second

    def __init__( self ):
        pg.init()
        self.game = Game()  # create a new game

        # set-up screen
        self.screen = pg.display.set_mode( (self.WIDTH, self.HEIGHT) )
        pg.display.set_caption( "Da Vinci's Challenge" )

        # setup background
        self.background = pg.Surface( self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill( (125, 125, 125) )

        # FPS clock
        self.clock = pg.time.Clock()

        # piece sprites
        self.diarcs = [ sprites.SpriteDiarc( x=-100, y=-100 ) for _ in
                        range( Board.NUM_DIARCS ) ]
        self.triarcs = [ sprites.SpriteTriarc( x=-100, y=-100 ) for _ in
                         range( Board.NUM_TRIARCS ) ]

        # build the board
        self.buildBoard()

    # __init__

    def buildBoard( self ):
        """ Build the board for playing"""
        # image sizes
        dw, dh = self.diarcs[ 0 ].image.get_size()
        tw, th = self.triarcs[ 0 ].image.get_size()

        # board parameters
        padding = 1
        top = (self.screen.get_height() - 6 * th) // 2
        colsep = th * math.cos( 60 )
        heightsep = (th + padding) // 2

        # triarcs
        xloc_t = (self.screen.get_width() - tw) // 2
        yloc_t = top
        for i, triarc in enumerate( self.triarcs ):
            xl, yl, rotation = None, None, None
            v = 1 if i % 2 == 0 else -1
            if 0 <= i < 6:  # column 4
                xl = xloc_t
                yl = yloc_t + i * heightsep * 2
                rotation = None

            elif 6 <= i < 16:  # columns 3, 5
                xl = xloc_t - 1 * v * colsep
                yl = yloc_t + ((i - 6) // 2 * 2 + 1) * heightsep
                rotation = None

            elif 16 <= i < 24:  # columns 2, 6
                xl = xloc_t - 2 * v * colsep
                yl = yloc_t + ((i - 16) // 2 * 2 + 2) * heightsep
                rotation = None

            elif 24 <= i < 30:  # columns 1, 7
                xl = xloc_t - 3 * v * colsep
                yl = yloc_t + ((i - 24) // 2 * 2 + 3) * heightsep
                rotation = None

            elif 30 <= i < 42:  # rotated columns 3.5, 4.5 angled down
                xl = xloc_t - (v * colsep) // 2 -32
                yl = yloc_t + (i - 30) // 2 * 2 * heightsep - 10
                rotation = v * 60

            elif 42 <= i < 54:  # rotated columns 3.5, 4.5 angled up
                xl = xloc_t - (v * colsep) // 2 - 32
                yl = yloc_t + (i - 42) // 2 * 2 * heightsep + th//2 - 10
                rotation = -v * 60

            triarc.update( x=xl, y=yl, rotation=rotation )

        # for

    # buildBoard

    def run( self ):
        """ Run the game """
        run = True
        while run:
            # handle the events
            for event in pg.event.get():
                self.clock.tick( self.FPS )  # control framerate
                if event.type == pg.QUIT:
                    run = False

                # if
                self.render()

        # while
        pg.quit()

    # run

    def render( self ):
        self.screen.blit( self.background, (0, 0) )

        for piece in self.triarcs + self.diarcs:
            piece.blit( self.screen )

        pg.display.update()

    # render

# class: GameApplication
