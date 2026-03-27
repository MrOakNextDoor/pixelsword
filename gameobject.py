
# Libraries
from functools import lru_cache
from typing import Any, Tuple
import pygame

# Constants
DEFAULT_IMAGE = pygame.Surface((64, 64))
DEFAULT_IMAGE.set_colorkey((0, 0, 0, 0))
DEFAULT_IMAGE.fill((255, 0, 255, 0))

# NOTE:
# Adding *args and **kwds allows me to reduce the amount of copy-pasting I need to do in the future.
# It also allows classes that give more args and keyword args to use functions that take less.
# For example, if I had a Renderer that took "is_good_function," I won't have to copy is_good_function 
# to the GameObject and Collection.
# Though for future updates, we would have to use args[index] and kwds[key]

# Code
class GameObject(pygame.sprite.Sprite):
    def __init__(self, 
        texture: pygame.Surface | None = None,
        renderer: Renderer | None = None,
        position: pygame.math.Vector2 | Tuple[float, float] = (0, 0), 
        scale: pygame.math.Vector2 | Tuple[float, float] = (64, 64), 
        rotation: float = 0.0,
        *groups: pygame.sprite.AbstractGroup[pygame.sprite._SpriteSupportsGroup],
        **kwds: Any) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)

        # Variables
        self.renderer = renderer
        self.position = position # Position refers to the centre of the character, unlike pygame's top-left.
        self.scale = scale
        self.rotation = rotation
        self.texture = texture # Moved texture here because it needs scale and rotation to set the self.image.

    # Attributes
    @property
    def renderer(self) -> Renderer:
        return self._renderer
    
    @renderer.setter
    def renderer(self, r: Renderer | None) -> None:
        self._renderer = Renderer() if r is None else r

    @property
    def texture(self) -> pygame.Surface:
        return self._texture
    
    @texture.setter
    def texture(self, s: pygame.Surface | None):
        if s is None:
            self._texture = DEFAULT_IMAGE    # Ensures that the GameObject always has something to render.
        else:
            self._texture = s

    @property
    def position(self) -> pygame.math.Vector2:
        return self._position

    @position.setter
    def position(self, p: pygame.math.Vector2 | Tuple[float, float]) -> None:
        self._position = pygame.math.Vector2(p)

    @property
    def scale(self) -> pygame.math.Vector2:
        return self._scale

    @scale.setter
    def scale(self, s: pygame.math.Vector2 | Tuple[float, float])  -> None:
        self._scale = pygame.math.Vector2(s)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, r: float) -> None:
        self._rotation = r % 360

    @property
    def rect(self) -> pygame.Rect:
        # The rect basically acts as the bounding box/hitbox for the GameObject.
        # Q: Why did I go through all the trouble to implement the rect attribute?
        # A: When I get lazy for other games, I could use the default draw() method of pygame.sprite.Group.
        # pygame.Surface.blit() uses the topleft corner of a Sprite's image to draw stuff.
        # This attribute effectively re-writes Sprite.rect, making it immutable.
        # We don't need the rects anyway since we only use it for sprite.Group's default draw().
        return self.image.get_rect(center=self.position) # type: ignore
    
    @rect.setter
    def rect(self, r) -> None: # type: ignore
        raise Exception('GameObject.rect not settable.')

    @property
    def image(self) -> pygame.Surface:
        # Similar to GameObject.rect, image is also immutable.
        return self.renderer.transform(self.texture, tuple(self.scale), self.rotation)
    
    @image.setter
    def image(self, i) -> None: # type: ignore
        raise Exception('GameObject.image not settable.')

    # Functions
    def update(self, *args: Any, **kwds: Any) -> None:
        pass

    def draw(self, 
        dest: pygame.Surface,
        draw_hitbox: bool = False,
        *args: Any, 
        **kwds: Any) -> None:
        """Draws a GameObject onto a destination surface. It makes use of the Rendere supplied during __init__().
        This function may be called by Collection.

        Args:
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): If true, draws GameObject.rect.
        """
        self.renderer(gameobject=self, dest=dest, draw_hitbox=draw_hitbox, *args, **kwds)

class Collection(pygame.sprite.Group):
    def __init__(self, *gameobjects: Any | GameObject | Collection, **kwds: Any) -> None:
        super().__init__(*gameobjects)

    def update(self) -> None:
        """Updates the GameObjects in this Collection by calling their update() functions.
        """
        for sprite in self:
            sprite.update()

    def render(self, 
        dest: pygame.Surface, 
        draw_hitbox: bool=False,
        *args: Any, 
        **kwds: Any) -> None:
        """Renders all of the GameObjects in this Collection. More customisable than the standard Group.draw()

        Args:
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): If true, draws the hitboxes of the GameObject.
        """
        for sprite in self:
            sprite.draw(dest=dest, draw_hitbox=draw_hitbox, *args, **kwds)

class Renderer:
    def __init__(self, *args: Any, **kwds: Any) -> None:
        self.hitbox_colour: pygame.typing.ColorLike = (255, 0, 0, 0)
        self.hitbox_width: int = 2

    def __call__(self, gameobject: GameObject, dest: pygame.Surface, draw_hitbox: bool=False, *args: Any, **kwds: Any) -> None:
        """Blits GameObjects onto a destination surface. This is the standard rendering.

        Args:
            gameobject (GameObject): GameObject to be blitted.
            dest (pygame.Surface): Destination surface.
            draw_hitbox (bool): draw_hitbox (bool): If true, draws GameObject.rect.
        """
        if dest.get_rect().colliderect(gameobject.rect):
            # Prevents rendering when the GameObject is not in view.
            dest.blit(gameobject.image, gameobject.rect)
            if draw_hitbox:
                pygame.draw.rect(dest, self.hitbox_colour, gameobject.rect, self.hitbox_width)

    @lru_cache(maxsize=1024)
    def transform(self, source: pygame.Surface, scale: Tuple[float, float], rotation: float, *args: Any, **kwds: Any) -> pygame.Surface:
        """Standard transformation for Surfaces. Scale is done before rotation to maintain its proportions.

        Args:
            source (pygame.Surface): The Surface to be transformed.
            scale (pygame.math.Vector2 | Tuple[float, float]): Scale of Surface.
            rotation (float): Rotation of Surface.

        Returns:
            pygame.Surface: Transformed Surface.
        """
        # This function is cached because I'm guessing a thousand transformations per frame can't be good for your health.

        # Scale happens before rotation so that the gameobject retains its proportions.
        # A renderer subclass is used if we want to transformation in weird ways (e.g. for a fake 3D effect).
        return pygame.transform.rotate(pygame.transform.scale(source, scale), rotation)

# Don't delete: this is the peak code. このコード最高すぎだよ！
# class FlatRenderer(Renderer):
#     def transform(self, source, scale, rotation) -> pygame.Surface:
#         surf = super().transform(source, scale, rotation)
#         return pygame.transform.scale(surf, (surf.get_width(), surf.get_height()//2))

# Testing
if __name__ == "__main__":
    # t = GameObject()
    pass