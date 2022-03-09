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
    NUM_DIARCS = 54
    NUM_TRIARCS = 90

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

    def playPiece( self, move: Move ):
        """ Player plays a piece on the board

            Operation will not be successful if any are true:
                - location is already taken
                - player does not have enough of pieces of type "piece"

            :param move: Move object that is being performed

            :return: boolean of whether operation was successful
        """

        valid_move = self.isValidMove(move)  # operation successful or not
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

    def isFilled( self ):
        """ Check whether the board is filled"""
        return not any(
                map(
                        lambda p: p == 0,
                        self.diarcs + self.triarcs ) )  # check if any board pieces empty

    # isFilled

    def isValidMove( self, move: Move ):
        """ Check if the move is valid """
        if move.piece is Piece.DIARC and self.diarcs[move.location] == 0 and move.player.diarcs > 0:
            return True

        elif move.piece is Piece.TRIARC and self.triarcs[move.location] == 0 and move.player.triarcs > 0:
            return True

        else:
            return False

    # isValidMove


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

    def checkScore( self, location: int, piece: Piece, player: Player ):
        """ Function to check if a play was a scoring play

            :param location: integer location of the piece placed
            :param piece: type of Piece that was played
            :param player: the player that played the piece

            :return: total score that was added
        """
        # TODO: implement score checking
        return 0

    # checkScore

    def isValidMove( self, move: Board.Move ):
        """ Check if move is valid"""
        # check board if move is valid
        return self.board.isValidMove(move)

    # isValidMove

    def play( self ):
        """ Plays the game

        """
        # TODO: implement game playing
        raise NotImplementedError("play is not implemented here.")
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
