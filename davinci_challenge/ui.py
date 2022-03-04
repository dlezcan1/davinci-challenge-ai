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
                # break

            elif 30 <= i < 42:  # rotated columns 3.5, 4.5 angled down
                xl = xloc_t - (v * colsep) // 2 - 32
                yl = yloc_t + (i - 30) // 2 * 2 * heightsep - 10
                rotation = v * 60

            elif 42 <= i < 54:  # rotated columns 3.5, 4.5 angled up
                xl = xloc_t - (v * colsep) // 2 - 32
                yl = yloc_t + (i - 42) // 2 * 2 * heightsep + th // 2 - 10
                rotation = -v * 60

            elif 54 <= i < 64:  # rotated columns 2.5, 5.5 angled down
                xl = xloc_t - 3 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 54) // 2 * 2 * heightsep) + th // 2 - 10
                rotation = v * 60


            elif 64 <= i < 74:  # rotated columns 2.5, 5.5 angled up
                xl = xloc_t - 3 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 64) // 2 * 2 * heightsep) + 2 * th // 2 - 10
                rotation = -v * 60

            elif 74 <= i < 82:  # rotated columns 1.5, 6.5 angled down
                xl = xloc_t - 5 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 74) // 2 * 2 * heightsep) + 2 * th // 2 - 10
                rotation = v * 60

            elif 82 <= i < 90:  # rotated columns 1.5, 6.5 angled up
                xl = xloc_t - 5 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 82) // 2 * 2 * heightsep) + 3 * th // 2 - 10
                rotation = -v * 60

            triarc.update( x=xl, y=yl, rotation=rotation )

        # for: triarcs

        # diarcs
        yloc_t += dh // 4
        lcolsep = dw - 4
        rcolsep = dw // 4 - 10
        for i, diarc in enumerate( self.diarcs ):
            xl, yl, rotation = None, None, None
            v = 1 if i % 2 == 0 else -1
            if 0 <= i < 12:  # columns 3 and 4 out
                xl = xloc_t - (v > 0) * lcolsep + (v < 0) * rcolsep
                yl = yloc_t + (i - 0) // 2 * 2 * heightsep
                rotation = -v * 30

            elif 12 <= i < 22:  # columns 3 and 5 in
                xl = xloc_t - 5 * ((v > 0) * lcolsep - (v < 0) * rcolsep) // 2 + 2 * dw // 3 - v * 2
                yl = yloc_t + (i - 12) // 2 * 2 * heightsep + th // 2
                rotation = v * 30

            elif 22 <= i < 32:  # columns 2 and 6 out
                xl = xloc_t - 9 * ((v > 0) * lcolsep - (v < 0) * rcolsep) // 2 + 3 * dw // 2 + 2
                yl = yloc_t + (i - 22) // 2 * 2 * heightsep + th // 2
                rotation = -v * 30

            elif 32 <= i < 40:  # columns 2 and 6 in
                xl = xloc_t - 13 * (
                            (v > 0) * lcolsep - (v < 0) * (rcolsep-1)) // 2 + 5 * dw // 2 + v*6 - (v < 0)*2
                yl = yloc_t + (i - 32) // 2 * 2 * heightsep + th
                rotation = v * 30

            elif 40 <= i < 48:  # columns 1 and 7 out
                xl = xloc_t - 17 * ((v > 0) * lcolsep - (v < 0)*(rcolsep-2))//2 + 7*dw//2 -1
                yl = yloc_t + (i - 40) // 2 * 2 * heightsep + th
                rotation = -v*30

            elif 48 <= i < 54:  # columns 1 and 7 in
                xl = xloc_t - 21 * ((v > 0)*lcolsep - (v < 0) * (rcolsep-3))//2 + 9*dw//2 + v*2
                yl = yloc_t + (i - 48)//2 * 2 * heightsep + 3*th//2
                rotation = v*30

            diarc.update( x=xl, y=yl, rotation=rotation )

        # for: diarcs

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
