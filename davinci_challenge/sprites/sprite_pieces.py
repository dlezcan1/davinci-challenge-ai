import pygame as pg


# TODO: sprites for multicolor Diarcs and Triarcs
class SpritePiece( pg.sprite.Sprite ):
    def __init__( self, x: int = 0, y: int = 0 ):
        super().__init__()

        self.image = pg.Surface( (100, 100) )
        self.player = None
        self.x, self.y = x, y

    # __init__

    def blit( self, screen: pg.Surface, *args ):
        """ Render the Sprite"""
        screen.blit( self.image, (self.x, self.y), *args )

    # blit

    def update( self, player: int = None, x: int = None, y: int = None, rotation: float = None ):
        # update player
        if (self.player is None) and (player in [ 1, 2 ]):
            self.player = player  # set the owner of the player
            color = (0, 0, 255) if player == 1 else (255, 0, 0)

            px_array = pg.PixelArray( self.image )
            px_array.replace( (0, 0, 0), color )
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

    # update


# class: SpritePiece

class SpriteDiarc( SpritePiece ):
    def __init__( self, x: int = 0, y: int = 0, rotation: float = 0 ):
        super().__init__( x=x, y=y )

        self.image = pg.image.load( 'assets/diarc.png' )
        self.image = pg.transform.rotate( self.image, rotation )
        self.image = pg.transform.scale(
                self.image, (2 * self.image.get_width(), 2 * self.image.get_height()) )

    # __init__


# class: SpriteDiarc

class SpriteTriarc( SpritePiece ):
    def __init__( self, x: int = 0, y: int = 0, rotation: float = 0 ):
        super().__init__( x=x, y=y )

        self.image = pg.image.load( 'assets/triarc.png' )
        self.image = pg.transform.rotate( self.image, rotation )
        self.image = pg.transform.scale(
                self.image, (2 * self.image.get_width(), 2 * self.image.get_height()) )

    # __init__

# class: SpriteTriarc
