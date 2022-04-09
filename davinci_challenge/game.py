from enum import Enum
from dataclasses import dataclass

# package imports
from player import Player


class Piece( Enum ):
    DIARC = 0
    TRIARC = 1


# enum class: Pieces


class Board:
    """ Class implementation of the board game

    """
    # Parameters of the Board
    # number of pieces
    NUM_PIECES = 144
    NUM_TRIARCS = 54
    NUM_DIARCS = 90

    @dataclass
    class Move:
        """ Move
            :param location: integer location of where to put the piece
            :param piece: which type of Piece to play
            :param player: the player that is playing it
        """
        location: int
        piece: Piece
        player: Player

    # dataclass: Move

    def __init__( self ):
        # initialize board locations
        self.triarcs = [ 0 ] * Board.NUM_TRIARCS
        self.diarcs = [ 0 ] * Board.NUM_DIARCS

    # __init__

    def isFilled( self ):
        """ Check whether the board is filled"""
        return not any(
                map(
                        lambda p: p == 0,
                        self.diarcs + self.triarcs ) )  # check if any board pieces empty

    # isFilled

    def isValidMove( self, move: Move ):
        """ Check if the move is valid """
        if move.piece is Piece.DIARC and self.diarcs[
            move.location ] == 0 and move.player.diarcs > 0:
            return True
        elif move.piece is Piece.TRIARC and self.triarcs[
            move.location ] == 0 and move.player.triarcs > 0:
            return True
        else:
            return False

    # isValidMove

    def getRowColumn( self, piece: Piece, location: int ):
        """ Get the row and the column of the piece

            Diarc columns span from 0-12 (13 columns)
            Order:
                 0: 1 x 3 x straight
                 1: 2 x 4 x angled
                 2: 1 x 4 x straight
                 3: 2 x 5 x angled
                 4: 1 x 5 x straight
                 5: 2 x 5 x angled
                 6: 1 x 6 x straignt
                 7: 2 x 5 x angled
                 8: 1 x 5 x straight
                 9: 2 x 5 x angled
                10: 1 x 4 x straight
                11: 2 x 4 x angled
                12: 1 x 4 x straight

            Triarc columns span from 0-11 (12 columns)
            Order:
                 0: 3 x right
                 1: 4 x left
                 2: 4 x right
                 3: 5 x left
                 4: 5 x right
                 5: 6 x left
                 6: 6 x right
                 7: 5 x left
                 8: 5 x right
                 9: 4 x left
                10: 4 x right
                11: 3 x left

            :param piece: the piece to get the row and column of
            :param location: the index of the piece

            :returns: (row, column) of the piece's location

        """
        row, col = None, None
        if piece is Piece.DIARC:
            if 0 <= location < 6:  # column 7
                col = 7
                row = location

            elif 6 <= location < 16:  # columns 4 and 8
                col = 4 if location % 2 == 0 else 8
                row = (location - 6) // 2

            elif 16 <= location < 24:  # columns 2 and 10
                col = 2 if location % 2 == 0 else 10
                row = (location - 16) // 2

            elif 24 <= location < 30:  # columns 0 and 12
                col = 0 if location % 2 == 0 else 12
                row = (location - 24) // 2

            elif 30 <= location < 42:  # columns 5 and 7 angled down
                col = 5 if location % 2 == 0 else 7
                row = 2 * ((location - 30) // 2)

            elif 42 <= location < 54:  # columns 5 and 7 angled up
                col = 5 if location % 2 == 0 else 7
                row = 2 * ((location - 42) // 2) + 1

            elif 54 <= location < 64:  # columns 3 and 9 angled down
                col = 3 if location % 2 == 0 else 9
                row = 2 * ((location - 54) // 2)

            elif 64 <= location < 74:  # columns 3 and 9 angled up
                col = 3 if location % 2 == 0 else 9
                row = 2 * ((location - 64) // 2) + 1

            elif 74 <= location < 82:  # columns 1 and 11 angled down
                col = 1 if location % 2 == 0 else 11
                row = 2 * ((location - 74) // 2)

            elif 82 <= location < 90:  # columns 1 and 11 angled up
                col = 1 if location % 2 == 0 else 11
                row = 2 * ((location - 74) // 2) + 1

        # if
        elif piece is Piece.TRIARC:
            if 0 <= location < 12:  # columns 5 and 6
                col = 5 if location % 2 == 0 else 6
                row = location // 2

            elif 12 <= location < 22:  # columns 4 and 7
                col = 4 if location % 2 == 0 else 7
                row = (location - 12) // 2

            elif 22 <= location < 32:  # columns 3 and 8
                col = 3 if location % 2 == 0 else 8
                row = (location - 22) // 2

            elif 32 <= location < 40:  # columns 2 and 9
                col = 2 if location % 2 == 0 else 9
                row = (location - 32) // 2

            elif 40 <= location < 48:  # columns 1 and 10
                col = 1 if location % 2 == 0 else 10
                row = (location - 40) // 2

            elif 48 <= location < 54:  # columns 0 and 11
                col = 0 if location % 2 == 0 else 11
                row = (location - 48) // 2

        # elif

        return row, col

    # getRowColumn

    def playPiece( self, move: Move ):
        """ Player plays a piece on the board

            Operation will not be successful if any are true:
                - location is already taken
                - player does not have enough of pieces of type "piece"

            :param move: Move object that is being performed

            :return: boolean of whether operation was successful
        """

        valid_move = self.isValidMove( move )  # operation successful or not
        if move.piece is Piece.DIARC and valid_move:
            self.diarcs[ move.location ] = move.player.number
            move.player.diarcs -= 1  # remove a piece from their hand

        # if
        elif move.piece is Piece.TRIARC and valid_move:
            self.triarcs[ move.location ] = move.player.number
            move.player.triarcs -= 1  # remove a piece from their hand

        # elif

        return valid_move

    # playPiece


# class: Board

class Game:
    # pieces each player starts off with
    START_DIARCS = Board.NUM_DIARCS // 2
    START_TRIARCS = Board.NUM_TRIARCS // 2

    # Point worths for each type of pattern
    POINT_TRIANGLE = 1
    POINT_DIAMOND = 1
    POINT_GEM = 5
    POINT_EYE = 5
    POINT_PYRAMID = 10
    POINT_HOURGLASS = 15
    POINT_STAR = 10
    POINT_CIRCLE = 25
    POINT_FLOWER = 25

    def __init__( self ):
        self.board = Board()

        # instantiate players
        self.player1 = Player( 1, Game.START_DIARCS, Game.START_TRIARCS )
        self.player2 = Player( 2, Game.START_DIARCS, Game.START_TRIARCS )

        # initialize the player scores
        self.player1Score = 0
        self.player2Score = 0

        # start player turn keeping
        self.turn = 1

    # __init__

    @property
    def playerOnDeck( self ):
        if self.turn == 1:
            return self.player1
        else:
            return self.player2

    # property: playerOnDeck

    def checkScore( self, move: Board.Move ):
        """ Function to check if a play was a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """

        # check triangles
        if move.piece is Piece.DIARC:
            value = self.checkScoreDiarcPiece( move )

        else:
            value = self.checkScoreTriarcPiece( move )

        return value

    # checkScore

    def checkScoreDiarcPiece( self, move: Board.Move ):
        """ Function ot check if a Diarc placement is a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """
        loc = move.location

        # check for triangles
        check_indices = [ ]

        return 0

    # checkScoreDiarcPiece

    def checkScoreTriarcPiece( self, move: Board.Move ):
        """ Function ot check if a Triarc placement is a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """
        return 0

    # checkScoreTriarcPiece

    def isValidMove( self, move: Board.Move ):
        """ Check if move is valid"""
        # check board if move is valid
        return self.board.isValidMove( move )

    # isValidMove

    def play( self ):
        """ Plays the game

        """
        # TODO: implement game playing
        raise NotImplementedError( "play is not implemented here." )
        while not self.board.isFilled():
            self.updateTurn()

        # while

    # play

    def playPiece( self, location: int, piece: Piece ):
        """ Play a piece """
        move = Board.Move( location, piece, self.playerOnDeck )
        success = self.board.playPiece( move )
        # check turn
        # update the turn
        if success:
            self.updateTurn()

        return success

    # playPiece

    def updateTurn( self ):
        """ Function to update the turn counter """
        self.turn = self.turn % 2 + 1

    # updateTurn

# class: Game
