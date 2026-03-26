
# Libraries
from functools import lru_cache
from typing import Any, Tuple
import pygame

# Constants
DEFAULT_IMAGE = pygame.Surface((64, 64))
DEFAULT_IMAGE.set_colorkey((0, 0, 0, 0))
DEFAULT_IMAGE.fill((255, 0, 255, 0))

# Code
class GameObject(pygame.sprite.Sprite):
    def __init__(self, 
        image: pygame.Surface | None = None,
        renderer: Renderer | None = None,
        position: pygame.math.Vector2 | Tuple[float, float] = (0, 0), 
        scale: pygame.math.Vector2 | Tuple[float, float] = (64, 64), 
        rotation: float = 0.0,
        *groups: pygame.sprite.AbstractGroup[pygame.sprite._SpriteSupportsGroup]) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)

        # Variables
        self.renderer = renderer
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.source = image # Moved the source here because the attribute calls update_image().
        self.image = image
        self.rect = None

    # Attributes
    @property
    def renderer(self) -> Renderer:
        return self._renderer
    
    @renderer.setter
    def renderer(self, r: Renderer | None) -> None:
        self._renderer = Renderer() if r is None else r

    @property
    def source(self) -> pygame.Surface:
        return self._source
    
    @source.setter
    def source(self, s: pygame.Surface | None):
        if s is None:
            self._source = DEFAULT_IMAGE    # Ensures that the GameObject always has something to render.
        else:
            self._source = s
        self.update_image()

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
        return self.__rect # type: ignore
    
    @rect.setter
    def rect(self, value: pygame.Rect | pygame.FRect | None) -> None:
        if value is None:
            # If value is None, default to this GameObject's own position & scale.
            # GameObjects must always have rects.
            # Transforms the image first before getting the rect. 
            # This allows us to get a rect accurate to the GameObject's position and scale.
            self.update_image()
            self.__rect = self.image.get_rect(center=self.position) # type: ignore
            return

        # Attempts to set the position and scale of the GameObject through the rect.
        # This would immediately raise an error if some bullshit is passed instead of rects.
        self.position = value.center # type: ignore
        self.scale = (value.w, value.h) # type: ignore
        self.__rect = pygame.Rect(value)

    # Functions
    def update_image(self) -> None:
        """Updates the GameObject's image to its current scale and rotation.
        """
        self.image = self.renderer.transform(self.source, tuple(self.scale), self.rotation)

    def update(self) -> None:
        self.rect = None    # By default, the rect is derived from the GameObject's info.

    def draw(self) -> None:
        pass

class Collection(pygame.sprite.Group):
    def __init__(self, *gameobjects: Any | GameObject | Collection) -> None:
        super().__init__(*gameobjects)

    def update(self) -> None:
        """Updates the GameObjects in this Collection by calling their update() functions.
        """
        for sprite in self:
            sprite.update()

    def render(self) -> None:
        pass

class Renderer:
    def __init__(self) -> None:
        pass

    def __call__(self) -> None:
        pass

    @lru_cache(maxsize=1024)
    def transform(self, source: pygame.Surface, scale: Tuple[float, float], rotation: float) -> pygame.Surface:
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

# Testing
if __name__ == "__main__":
    # t = GameObject()
    pass