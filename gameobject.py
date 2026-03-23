
# Libraries
from functools import cache
from pygame import math as pmath, Rect, sprite, Surface
from typing import Any, Tuple

# Constants
DEFAULT_RENDERER = NotImplemented
DEFAULT_IMAGE = NotImplemented

# Code
class GameObject(sprite.Sprite):
    def __init__(self, 
        image: Surface = DEFAULT_IMAGE,
        renderer: Renderer = DEFAULT_RENDERER,
        position: pmath.Vector2 | Tuple[float, float] = (0, 0), 
        scale: pmath.Vector2 | Tuple[float, float] = (16, 16), 
        rotation: float = 0,
        *groups: sprite.AbstractGroup[sprite._SpriteSupportsGroup]) -> None:
        sprite.Sprite.__init__(self, *groups)

        # Variables
        self.sourceimage = image
        self.renderer = renderer
        self.position = position
        self.scale = scale
        self.rotation = rotation

    # Attributes
    @property
    def position(self) -> pmath.Vector2:
        return self._position

    @position.setter
    def position(self, p: pmath.Vector2 | Tuple[float, float]) -> None:
        self._position = pmath.Vector2(p)

    @property
    def scale(self) -> pmath.Vector2:
        return self._scale

    @scale.setter
    def scale(self, s: pmath.Vector2 | Tuple[float, float])  -> None:
        self._scale = pmath.Vector2(s)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, r: float) -> None:
        self._rotation = r % 360

    # @property
    # def rect(self) -> Rect:

    #     return self.get_rect()
    
    # @rect.setter
    # def rect(self, r):
    #     pass

    # Functions
    # @cache
    # def get_rect(self) -> Rect:
    #     pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

class Collection(sprite.Group):
    def __init__(self, *sprites: Any | sprite.AbstractGroup | sprite.Iterable) -> None:
        super().__init__(*sprites)

class Renderer:
    pass


# Testing
if __name__ == "__main__":
    pass