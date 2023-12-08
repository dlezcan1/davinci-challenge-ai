from typing import List

import pygame as pg
import math
import numpy as np

# package imports
import game
from game import Game, Board, Piece
import sprites

# colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (125, 125, 125)


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
        self.background.fill( COLOR_GRAY )

        # FPS clock
        self.clock = pg.time.Clock()

        # piece sprites
        self.diarcs = [ sprites.SpriteDiarc( x=-100, y=-100 ) for _ in
                        range( Board.NUM_DIARCS ) ]
        self.triarcs = [ sprites.SpriteTriarc( x=-100, y=-100 ) for _ in
                         range( Board.NUM_TRIARCS ) ]

        # build the board
        self.buildBoard()

        # setup the font
        self._titleFont = pg.font.SysFont( 'arialblack', 50 )
        self._elementFont = pg.font.SysFont( 'arialblack', 24 )

    # __init__

    @property
    def pieces( self ) -> List[ sprites.SpritePiece ]:
        return self.triarcs + self.diarcs

    # property: pieces

    def buildBoard( self ):
        """ Build the board for playing"""
        # image sizes
        dw, dh = self.diarcs[ 0 ].image.get_size()
        tw2, th2 = self.triarcs[ 0 ].image.get_size()

        # board parameters
        padding = 1
        top = (self.screen.get_height() - 5 * dh) // 2
        colsep = dh * math.cos( 60 )
        heightsep = (dh + padding) // 2

        # diarcs
        xloc_t = (self.screen.get_width() - dw) // 2
        yloc_t = top
        for i, diarc in enumerate( self.diarcs ):
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
                yl = yloc_t + (i - 42) // 2 * 2 * heightsep + dh // 2 - 10
                rotation = -v * 60

            elif 54 <= i < 64:  # rotated columns 2.5, 5.5 angled down
                xl = xloc_t - 3 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 54) // 2 * 2 * heightsep) + dh // 2 - 10
                rotation = v * 60


            elif 64 <= i < 74:  # rotated columns 2.5, 5.5 angled up
                xl = xloc_t - 3 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 64) // 2 * 2 * heightsep) + 2 * dh // 2 - 10
                rotation = -v * 60

            elif 74 <= i < 82:  # rotated columns 1.5, 6.5 angled down
                xl = xloc_t - 5 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 74) // 2 * 2 * heightsep) + 2 * dh // 2 - 10
                rotation = v * 60

            elif 82 <= i < 90:  # rotated columns 1.5, 6.5 angled up
                xl = xloc_t - 5 * (v * colsep) // 2 - 32
                yl = yloc_t + ((i - 82) // 2 * 2 * heightsep) + 3 * dh // 2 - 10
                rotation = -v * 60

            diarc.update( x=xl, y=yl, rotation=rotation )

        # for: diarcs

        # triarcs
        yloc_t += th2 // 4
        lcolsep = tw2 - 4
        rcolsep = tw2 // 4 - 10
        for i, triarc in enumerate( self.triarcs ):
            xl, yl, rotation = None, None, None
            v = 1 if i % 2 == 0 else -1
            if 0 <= i < 12:  # columns 3 and 4 out
                xl = xloc_t - (v > 0) * lcolsep + (v < 0) * rcolsep
                yl = yloc_t + (i - 0) // 2 * 2 * heightsep
                rotation = -v * 30

            elif 12 <= i < 22:  # columns 3 and 5 in
                xl = xloc_t - 5 * (
                            (v > 0) * lcolsep - (v < 0) * rcolsep) // 2 + 2 * tw2 // 3 - v * 2
                yl = yloc_t + (i - 12) // 2 * 2 * heightsep + dh // 2
                rotation = v * 30

            elif 22 <= i < 32:  # columns 2 and 6 out
                xl = xloc_t - 9 * ((v > 0) * lcolsep - (v < 0) * rcolsep) // 2 + 3 * tw2 // 2 + 2
                yl = yloc_t + (i - 22) // 2 * 2 * heightsep + dh // 2
                rotation = -v * 30

            elif 32 <= i < 40:  # columns 2 and 6 in
                xl = xloc_t - 13 * (
                        (v > 0) * lcolsep - (v < 0) * (rcolsep - 1)) // 2 + 5 * tw2 // 2 + v * 6 - (
                             v < 0) * 2
                yl = yloc_t + (i - 32) // 2 * 2 * heightsep + dh
                rotation = v * 30

            elif 40 <= i < 48:  # columns 1 and 7 out
                xl = xloc_t - 17 * (
                        (v > 0) * lcolsep - (v < 0) * (rcolsep - 2)) // 2 + 7 * tw2 // 2 - 1
                yl = yloc_t + (i - 40) // 2 * 2 * heightsep + dh
                rotation = -v * 30

            elif 48 <= i < 54:  # columns 1 and 7 in
                xl = xloc_t - 21 * (
                        (v > 0) * lcolsep - (v < 0) * (rcolsep - 3)) // 2 + 9 * tw2 // 2 + v * 2
                yl = yloc_t + (i - 48) // 2 * 2 * heightsep + 3 * dh // 2
                rotation = v * 30

            triarc.update( x=xl, y=yl, rotation=rotation )

        # for: diarcs

    # buildBoard

    def handleMouseEvent( self, event: pg.event.Event ):
        """ This is a function to handle the mouse event """
        if event.type == pg.MOUSEMOTION:
            (x, y) = event.pos

            # unhover all pieces
            for piece in self.pieces:
                piece.update( hovered=False )

            # check for colliding pieces
            update_piece, update_piece_idx = self.selectPiece( x, y )

            if update_piece is not None:
                update_piece.update( hovered=True )

            # if

        # if: MouseMotion

        if event.type == pg.MOUSEBUTTONDOWN:
            (x, y) = event.pos

            update_piece, update_piece_idx = self.selectPiece( x, y )

            # play the piece
            if update_piece is not None:
                self.playPiece( update_piece, update_piece_idx )

        # if: MouseButtonDown

    # handleMouseEvent

    def run( self ):
        """ Run the game """
        run = True
        while run:
            # handle the events
            for event in pg.event.get():
                self.clock.tick( self.FPS )  # control frame-rate
                # print( f"Current FPS: {self.clock.get_fps()}" )
                if event.type == pg.QUIT:
                    run = False

                elif event.type in [ pg.MOUSEWHEEL, pg.MOUSEMOTION, pg.MOUSEBUTTONUP,
                                     pg.MOUSEBUTTONDOWN ]:
                    self.handleMouseEvent( event )

                # render at the end of the loop
                self.render()

        # while
        pg.quit()

    # run

    def render( self ):
        # blit the background
        self.screen.blit( self.background, (0, 0) )

        # blit the game interface
        self.renderGameInterface()

        # blit the pieces onto the screen
        for idx, piece in enumerate(self.diarcs):
            piece.blit( self.screen )

            # TODO: remove | for debugging purposes only
            if piece.hovered:
                row, col = Board.getRowColumn( piece.pieceType, idx )
                rowcol_font = self._elementFont.render( f"Diarc: ({row}, {col})", True, COLOR_WHITE )
                self.screen.blit(
                    rowcol_font, (
                                (self.screen.get_width() - rowcol_font.get_width()) - 15,
                                self.screen.get_height() - 50) )
        # for: diarcs
        for idx, piece in enumerate( self.triarcs ):
            piece.blit( self.screen )

            # TODO: remove | for debugging purposes only
            if piece.hovered:
                row, col = Board.getRowColumn( piece.pieceType, idx )
                rowcol_font = self._elementFont.render( f"Triarc: ({row}, {col})", True, COLOR_WHITE )
                self.screen.blit(
                        rowcol_font, (
                                (self.screen.get_width() - rowcol_font.get_width()) - 15,
                                self.screen.get_height() - 50) )
        # for: diarcs

        pg.display.update()

    # render

    def playPiece( self, piece: sprites.SpritePiece, piece_index: int ):
        """ Play the current piece from the piece type and index """
        playerOnDeck = self.game.playerOnDeck

        # player the piece
        success = self.game.playPiece( piece_index, piece.pieceType )

        # update the board visualization
        if success:
            piece.update( player=playerOnDeck.number )

    # playPiece

    def selectPiece( self, x, y ):
        """ Get the current Piece under at position x, y"""
        # initialization
        min_dist = float( "inf" )
        select_piece = None
        select_piece_idx = None

        # go over triarcs
        for i, piece in enumerate( self.triarcs ):
            if piece.rect.collidepoint( x, y ):
                d = piece.distanceFromCenter( x, y )
                if d < min_dist:
                    min_dist = d
                    select_piece = piece
                    select_piece_idx = i

                # if
            # if
        # for

        # go over diarcs
        for i, piece in enumerate( self.diarcs ):
            if piece.rect.collidepoint( x, y ):
                d = piece.distanceFromCenter( x, y )
                if d < min_dist:
                    min_dist = d
                    select_piece = piece
                    select_piece_idx = i

                # if
            # if
        # for

        return select_piece, select_piece_idx

    def renderGameInterface( self ):
        """ Draw the scores and piece counts """
        # get screen size
        screen_W, screen_H = self.screen.get_size()

        # blit the title
        title = self._titleFont.render( "DaVinci's Challenge", True, COLOR_WHITE )
        self.screen.blit( title, ((screen_W - title.get_width()) // 2, 10) )

        # player piece counts and scores
        rect_buffer = (10, 15)
        player1Diarcs = self._elementFont.render(
                f"Diarcs: {self.game.player1.diarcs:2d}", True, COLOR_WHITE )
        player1Triarcs = self._elementFont.render(
                f"Triarcs: {self.game.player1.triarcs:2d}", True, COLOR_WHITE )
        player1Score = self._elementFont.render(
                f"Score: {self.game.player1Score:3d}", True, COLOR_WHITE )
        p1_maxWidth = max(
                [ player1Diarcs.get_width(), player1Triarcs.get_width(),
                  player1Score.get_width() ] )
        player1Rect = pg.Rect(
                10 - rect_buffer[ 0 ] // 2, 30 + title.get_height() - rect_buffer[ 1 ] // 2,
                p1_maxWidth + rect_buffer[ 0 ],
                player1Triarcs.get_height() + player1Triarcs.get_height() + player1Score.get_height() +
                rect_buffer[ 1 ] )

        player2Diarcs = self._elementFont.render(
                f"Diarcs: {self.game.player2.diarcs:2d}", True, COLOR_WHITE )
        player2Triarcs = self._elementFont.render(
                f"Triarcs: {self.game.player2.triarcs:2d}", True, COLOR_WHITE )
        player2Score = self._elementFont.render(
                f"Score: {self.game.player2Score:3d}", True, COLOR_WHITE )
        p2_maxWidth = max(
                [ player2Diarcs.get_width(), player2Triarcs.get_width(),
                  player2Score.get_width() ] )
        player2Rect = pg.Rect(
                screen_W - rect_buffer[ 0 ] // 2 - p2_maxWidth - 10,
                30 + title.get_height() - rect_buffer[ 1 ] // 2,
                p2_maxWidth + rect_buffer[ 0 ],
                player2Triarcs.get_height() + player2Triarcs.get_height() + player2Score.get_height() +
                rect_buffer[ 1 ] )

        # draw player piece counts and scores
        pg.draw.rect( self.screen, (0, 0, 255), player1Rect )
        self.screen.blit(
                player1Diarcs, tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player1Rect.topleft, rect_buffer,
                                (p1_maxWidth - player1Diarcs.get_width(), 0) ) ) )
        self.screen.blit(
                player1Triarcs, tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player1Rect.topleft, rect_buffer,
                                (p1_maxWidth - player1Triarcs.get_width(),
                                 player1Diarcs.get_height()) ) ) )
        self.screen.blit(
                player1Score,
                tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player1Rect.topleft, rect_buffer,
                                (p1_maxWidth - player1Score.get_width(),
                                 player1Diarcs.get_height() + player1Triarcs.get_height()) ) ) )

        pg.draw.rect( self.screen, (255, 0, 0), player2Rect )
        self.screen.blit(
                player2Diarcs, tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player2Rect.topleft, rect_buffer,
                                (p2_maxWidth - player2Diarcs.get_width(), 0) ) ) )
        self.screen.blit(
                player2Triarcs, tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player2Rect.topleft, rect_buffer,
                                (p2_maxWidth - player2Triarcs.get_width(),
                                 player2Diarcs.get_height()) ) ) )
        self.screen.blit(
                player2Score,
                tuple(
                        pos + buff // 2 + offset for pos, buff, offset in
                        zip(
                                player2Rect.topleft, rect_buffer,
                                (p2_maxWidth - player2Score.get_width(),
                                 player2Diarcs.get_height() + player2Triarcs.get_height()) ) ) )

    # renderGameInterface

# class: GameApplication
