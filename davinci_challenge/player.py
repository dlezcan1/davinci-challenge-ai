class Player:
    def __init__( self, number: int, num_diarcs: int, num_triarcs: int ):
        """ Player constructor

            :param number: The player's number (must be 0 or 1)
            :param num_diarcs: The number of diarcs the player starts with
            :param num_triarcs: The number of triarcs the player starts with

        """
        if number not in [ 1, 2 ]:
            raise ValueError( "player number must be 0 or 1!" )

        # if

        if num_diarcs < 0 or num_triarcs < 0:
            raise ValueError( "num_diarcs and num_triarcs must be > 0!" )

        # if

        self.number = number
        self.diarcs = num_diarcs
        self.triarcs = num_triarcs

    # __init__

    def __repr__( self ):
        return f"Player{self.number}: diarcs={self.diarcs} | triarcs={self.triarcs}"


# class: Player

class AI( Player ):
    def __init__( self, number: int, num_diarcs: int, num_triarcs: int ):
        super().__init__( number, num_diarcs, num_triarcs )

    # __init__

    def __repr__(self):
        return "AI" + super().__repr__()

    # __repr__

    def playMove( self ):
        """ Plays the next player's move

            :returns: Move object for the next move to play
        """
        # TODO: AI implementation of move choice
        raise NotImplementedError("AI not implemented yet.")
        # return Board.Move( 0, Piece.DIARC, self )

    # playMove

# class: AI
