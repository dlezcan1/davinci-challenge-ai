from enum import Enum
from dataclasses import dataclass

from typing import (
    List,
    Tuple,
)

# package imports
from player import Player


class Piece( Enum ):
    DIARC = 0
    TRIARC = 1


# enum class: Pieces


class Board:
    """ Class implementation of the board game

        Indexing of the board starts from (0,0) for both pieces to be from the top-right to the board
        and increase going down and to the left
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
        if (
            (move.piece is Piece.DIARC)
            and (self.diarcs[move.location ] == 0)
            and (move.player.diarcs > 0)
        ):
            return True
        
        if (
            (move.piece is Piece.TRIARC)
            and (self.triarcs[move.location ] == 0)
            and (move.player.triarcs > 0)
        ):
            return True

        return False

    # isValidMove

    @staticmethod
    def getRowColumn( piece: Piece, location: int ):
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
            if 0 <= location < 6:  # column 6
                col = 6
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
                row = 2 * ((location - 82) // 2) + 1

        # if: diarc
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

        # elif: triarc

        return row, col

    # getRowColumn

    @staticmethod
    def rowColumnToIndex( piece: Piece, row: int, col: int ):
        """ Convert the row-column format to a list index

            :returns list index of the point. None if not found

        """
        location = None

        if col == 0:
            if piece is Piece.DIARC:
                location = 2 * row + 24
            elif piece is Piece.TRIARC:
                location = 2 * row + 48
        # if
        elif col == 1:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 74
                else:  # angled up
                    location = row + 82 - 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 40
        # elif
        elif col == 2:
            if piece is Piece.DIARC:
                location = 2 * row + 16
            elif piece is Piece.TRIARC:
                location = 2 * row + 32
        # elif
        elif col == 3:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 54
                else:  # angled up
                    location = row + 64 - 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 22
        # elif
        elif col == 4:
            if piece is Piece.DIARC:
                location = 2 * row + 6
            elif piece is Piece.TRIARC:
                location = 2 * row + 12
        # elif
        elif col == 5:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 30
                else:  # angled up
                    location = row + 42 - 1
            elif piece is Piece.TRIARC:
                location = 2 * row
        # elif
        elif col == 6:
            if piece is Piece.DIARC:
                location = row
            elif piece is Piece.TRIARC:
                location = 2 * row + 1
        # elif
        elif col == 7:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 30 + 1
                else:  # angled up
                    location = row + 42 - 1 + 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 12 + 1
        # elif
        elif col == 8:
            if piece is Piece.DIARC:
                location = 2 * row + 6 + 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 22 + 1
        # elif
        elif col == 9:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 54 + 1
                else:  # angled up
                    location = row + 64 - 1 + 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 32 + 1
        # elif
        elif col == 10:
            if piece is Piece.DIARC:
                location = 2 * row + 16 + 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 40 + 1
        # elif
        elif col == 11:
            if piece is Piece.DIARC:
                if row % 2 == 0:  # angled down
                    location = row + 74 + 1
                else:  # angled up
                    location = row + 82 - 1 + 1
            elif piece is Piece.TRIARC:
                location = 2 * row + 48 + 1
        # elif
        elif col == 12 and piece is Piece.DIARC:
            location = 2 * row + 24 + 1

        # elif: DIARC

        return location

    # rowColumnToIndex

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
    
    def _checkListofLocationsScores(
            self, 
            check_piece_row_columns: List[Tuple[Piece, int, int]], 
            player: Player = None,
        ):
        check_indices = [ 
            Board.rowColumnToIndex( piece, row, col ) 
            for piece, row, col in
            check_piece_row_columns
        ]

        # check if
        does_score = True
        for idx, (piece, row, col) in zip(check_indices, check_piece_row_columns):
            if idx is None:  # not a valid piece
                does_score = False
                break

            # if

            player_piece_num = self.board.diarcs[idx] if piece is Piece.DIARC else self.board.triarcs[idx]

            if (
                (player is not None) 
                and ( player_piece_num != player.number)
            ):  # not a piece already played by other players
                does_score = False
                break

            # if
            elif (
                (player is None)
                and self.board.diarcs[idx] not in [self.player1.number, self.player2.number]
            ):
                does_score = False
                break

            # elif
            
        # for

        return does_score

    def checkScore( self, move: Board.Move ):
        """ Function to check if a play was a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """
        if not self.isValidMove(move):
            return 0
        
        score = 0
        if move.piece is Piece.DIARC:
            score += self.checkScoreDiarcPiece( move )

        else:
            score += self.checkScoreTriarcPiece( move )

        return score

    # checkScore

    def checkScoreDiarcPiece( self, move: Board.Move ):
        """ Function ot check if a Diarc placement is a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """
        score = 0

        # add scores
        score += self.checkScoreDiarcPiece_Triangle( move )
        score += self.checkScoreDiarcPiece_Eye( move )
        score += self.checkScoreDiarcPiece_Gem( move )
        score += self.checkScoreDiarcPiece_Flower( move )
        score += self.checkScoreDiarcPiece_Circle( move )
        score += self.checkScoreDiarcPiece_Hourglass( move )
        score += self.checkScoreDiarcPiece_Diamond( move )

        return score

    # checkScoreDiarcPiece

    def checkScoreDiarcPiece_Circle( self, move: Board.Move ):
        """ Check if any points are added from Circle arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        # TODO: implement valid moves

        # check valid moves
        score = 0

        return score

    # checkScoreDiarcPiece_Circle

    def checkScoreDiarcPiece_Diamond( self, move: Board.Move ):
        """ Check if any points are added from Diamond arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        row, col = self.board.getRowColumn(move.piece, move.location)

        if col % 2 == 0:
            check_locations = [
                (Piece.TRIARC, row, 11 - col),
                (Piece.TRIARC, row, 12 - col),
            ]

        else: # diagonal triarc
            if col < 6:
                if row % 2 == 0: # bottom-left to top-right slanted dirarc
                    check_locations = [
                        (Piece.TRIARC, row//2 - 1, col),
                        (Piece.TRIARC, row//2, col),
                    ]
                else:
                    check_locations = [
                        (Piece.TRIARC, row, 11 - col),
                        (Piece.TRIARC, row, 12 - col),
                    ]

            elif col > 6:
                if row % 2 == 0:
                    check_locations = [
                        (Piece.TRIARC, row//2 - 1, 12 - col),
                        (Piece.TRIARC, row//2, 11 - col),
                    ]

                else: # bottom-left to top-right slanted dirarc
                    check_locations = [
                        (Piece.TRIARC, (row - 1)//2, 11 - col),
                        (Piece.TRIARC, (row - 1)//2, 12 - col),
                    ]

        # check valid moves
        score = 0
        if self._checkListofLocationsScores(check_locations, player=move.player):
            score += self.POINT_DIAMOND

        return score

    # checkScoreDiarcPiece_Diamond

    def checkScoreDiarcPiece_Eye( self, move: Board.Move ):
        """ Check if any points are added from Eye arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        # TODO: implement valid moves

        # check valid moves
        score = 0

        return score

    # checkScoreDiarcPiece_Eye

    def checkScoreDiarcPiece_Flower( self, move: Board.Move ):
        """ Check if any points are added from Flower arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        # TODO: implement valid moves

        # check valid moves
        score = 0

        return score

    # checkScoreDiarcPiece_Flower

    def checkScoreDiarcPiece_Gem( self, move: Board.Move ):
        """ Check if any points are added from Gem arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        # TODO: implement valid moves

        # check valid moves
        score = 0

        return score

    # checkScoreDiarcPiece_Gem

    def checkScoreDiarcPiece_Hourglass( self, move: Board.Move ):
        """ Check if any points are added from Hourglass arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        # TODO: implement valid moves

        # check valid moves
        score = 0

        return score

    # checkScoreDiarcPiece_Hourglass

    def checkScoreDiarcPiece_Triangle( self, move: Board.Move ):
        """ Check if any points are added from Triangle arrangement
            after placing a Diarc

        """
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        elif move.piece is not Piece.DIARC:
            return 0

        # elif

        row, col = Board.getRowColumn( move.piece, move.location )

        # check for triangles
        if col % 2 == 0:  # straight up and down
            if col == 6: # middle of board
                check_locations = [
                    [ (Piece.DIARC, 2 * row, col - 1), (Piece.DIARC, 2 * row + 1, col - 1) ],
                    [ (Piece.DIARC, 2 * row, col + 1), (Piece.DIARC, 2 * row + 1, col + 1) ]
                ]
            # if
            elif col < 6: # right-side of board
                check_locations = [
                    [ (Piece.DIARC, 2 * row, col + 1), (Piece.DIARC, 2 * row + 1, col + 1) ],
                    [ (Piece.DIARC, 2 * row + 1, col - 1), (Piece.DIARC, 2 * row + 2, col - 1) ]
                ]
            # elif
            else:  # col > 6 : left-side of board
                check_locations = [
                    [ (Piece.DIARC, 2 * row + 1, col - 1), (Piece.DIARC, 2 * row + 2, col - 1) ],
                    [ (Piece.DIARC, 2 * row, col + 1), (Piece.DIARC, 2 * row + 1, col + 1) ]
                ]
            # else

        else:  # angled to left and right
            # angled bottom-left to top-right, right-side
            if row % 2 == 1 and col < 6:
                check_locations = [
                    [ (Piece.DIARC, row - 1, col), (Piece.DIARC, row // 2, col + 1) ],
                    [ (Piece.DIARC, row + 1, col), (Piece.DIARC, row // 2, col - 1) ]
                ]

            # angled bottom-right to top-left, right-side
            elif row % 2 == 0 and col < 6:
                check_locations = [
                    [ (Piece.DIARC, row - 1, col), (Piece.DIARC, row // 2 - 1, col - 1) ],
                    [ (Piece.DIARC, row + 1, col), (Piece.DIARC, row // 2, col + 1) ],
                ]

            # angled bottom-left to top-right, left-side
            elif row % 2 == 1 and col > 6:
                check_locations = [
                    [ (Piece.DIARC, row - 1, col), (Piece.DIARC, row // 2, col - 1) ],
                    [ (Piece.DIARC, row + 1, col), (Piece.DIARC, row // 2, col + 1) ],
                ]

            # angled bottom-right to top-left: left-side
            elif row % 2 == 0 and col > 6:
                check_locations = [
                    [ (Piece.DIARC, row - 1, col), (Piece.DIARC, row // 2 - 1, col + 1) ],
                    [ (Piece.DIARC, row + 1, col), (Piece.DIARC, row // 2, col - 1) ],
                ]

            else:
                check_locations = [ ]
        # if

        # check each of the locations
        score = 0
        for triangle_check in check_locations:

            # add points if there is a score
            if self._checkListofLocationsScores(triangle_check, player=move.player):
                score += Game.POINT_TRIANGLE

            # if
        # for

        return score

    # checkScoreDiarcPiece_Triangle

    def checkScoreTriarcPiece( self, move: Board.Move ):
        """ Function ot check if a Triarc placement is a scoring play

            :param move: Board.Move of the move to be queried

            :return: total score of a particular move
        """
        score = 0

        # add scores
        score += self.checkScoreTriarcPiece_Diamond(move)   # TODO: diamond score check
        score += self.checkScoreTriarcPiece_Gem(move)       # TODO: gem score check
        score += self.checkScoreTriarcPiece_Pyramid(move)   # TODO: pyramid score check
        score += self.checkScoreTriarcPiece_Hourglass(move) # TODO: hourglass score check
        score += self.checkScoreTriarcPiece_Star(move)      # TODO: star score check

        return score

    # checkScoreTriarcPiece

    def checkScoreTriarcPiece_Diamond( self, move: Board.Move ):
        # TODO
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        
        if move.piece is not Piece.TRIARC:
            return 0

        # if
        
        score = 0
        return score

    # checkScoreTriarcPiece_Diamond

    def checkScoreTriarcPiece_Gem( self, move: Board.Move ):
        # TODO
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        
        if move.piece is not Piece.TRIARC:
            return 0

        # if
        
        score = 0
        return score

    # checkScoreTriarcPiece_Gem

    def checkScoreTriarcPiece_Hourglass( self, move: Board.Move ):
        # TODO
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        
        if move.piece is not Piece.TRIARC:
            return 0

        # if
        
        score = 0
        return score

    # checkScoreTriarcPiece_Gem

    def checkScoreTriarcPiece_Pyramid( self, move: Board.Move ):
        # TODO
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        
        if move.piece is not Piece.TRIARC:
            return 0

        # if
        
        score = 0
        return score

    # checkScoreTriarcPiece_Pyramid

    def checkScoreTriarcPiece_Star( self, move: Board.Move ):
        # TODO
        # check if it is a valid move
        if not self.board.isValidMove( move ):
            return 0

        # if
        
        if move.piece is not Piece.TRIARC:
            return 0

        # if
        
        score = 0
        return score

    # checkScoreTriarcPiece_Star

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
        score_update = self.checkScore( move )
        success = self.board.playPiece( move )

        # piece was played
        if success:
            if self.playerOnDeck.number == 1:
                self.player1Score += score_update

            else:
                self.player2Score += score_update

            print( f"Player: {self.playerOnDeck.number} | score update = {score_update}" )
            # update the player turn
            self.updateTurn()

        # if

        return success

    # playPiece

    def updateTurn( self ):
        """ Function to update the turn counter """
        self.turn = self.turn % 2 + 1

    # updateTurn



# class: Game
