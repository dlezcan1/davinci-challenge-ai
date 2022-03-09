import pygame as pg
import game


# TODO: sprites for multicolor Diarcs and Triarcs
class SpritePiece( pg.sprite.Sprite ):
    COLOR_EMPTY = (0, 0, 0)
    COLOR_PLAYER1 = (0, 0, 255)
    COLOR_PLAYER2 = (255, 0, 0)

    def __init__( self, x: int = 0, y: int = 0 ):
        super().__init__()

        self.image = pg.Surface( (100, 100) )
        self.player = None
        self.x, self.y = x, y
        self.hovered = False
        self.pieceType = None

    # __init__

    @property
    def rect( self ) -> pg.Rect:
        r = self.image.get_rect()
        r.x += self.x
        r.y += self.y
        return r

    # property: rect

    def blit( self, screen: pg.Surface, *args ):
        """ Render the Sprite"""
        if self.hovered:
            px_array = pg.PixelArray( self.image.copy() )
            if self.player is None:
                old_color = self.COLOR_EMPTY
            elif self.player == 1:
                old_color = self.COLOR_PLAYER1
            else:
                old_color = self.COLOR_PLAYER2
            new_color = tuple( min( 255, c + 50 ) for c in old_color )
            px_array.replace( old_color, new_color )
            image = px_array.surface.copy()
        else:
            image = self.image

        screen.blit( image, (self.x, self.y), *args )

    # blit

    def distanceFromCenter( self, x, y ):
        xc, yc = self.rect.center
        return (x - xc) ** 2 + (y - yc) ** 2

    # distanceFromCenter

    def update(
            self, player: int = None, x: int = None, y: int = None, rotation: float = None,
            hovered: bool = False ):
        # update player
        if (self.player is None) and (player in [ 1, 2 ]):
            self.player = player  # set the owner of the player
            color = self.COLOR_PLAYER1 if player == 1 else self.COLOR_PLAYER2

            px_array = pg.PixelArray( self.image )
            px_array.replace( self.COLOR_EMPTY, color )
            self.image = px_array.surface.copy()
            self.image.unlock()

        # if

        # update location
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        # update rotation
        if rotation is not None:
            self.image = pg.transform.rotate( self.image, rotation )

        # check if mouse is hovering
        self.hovered = hovered

    # update


# class: SpritePiece

class SpriteDiarc( SpritePiece ):
    def __init__( self, x: int = 0, y: int = 0, rotation: float = 0 ):
        super().__init__( x=x, y=y )

        self.image = pg.image.load( 'assets/diarc.png' )
        self.image = pg.transform.rotate( self.image, rotation )
        self.image = pg.transform.scale(
                self.image, (2 * self.image.get_width(), 2 * self.image.get_height()) )
        self.pieceType = game.Piece.DIARC

    # __init__


# class: SpriteDiarc

class SpriteTriarc( SpritePiece ):
    def __init__( self, x: int = 0, y: int = 0, rotation: float = 0 ):
        super().__init__( x=x, y=y )

        self.image = pg.image.load( 'assets/triarc.png' )
        self.image = pg.transform.rotate( self.image, rotation )
        self.image = pg.transform.scale(
                self.image, (2 * self.image.get_width(), 2 * self.image.get_height()) )
        self.pieceType = game.Piece.TRIARC

    # __init__

# class: SpriteTriarc
