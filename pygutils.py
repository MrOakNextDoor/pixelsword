
# Libraries
import pygame as _pygame
from time import time as _time

# Code
class Clock:
    def __init__(self, framerate: int = 300, base_framerate: int = 60):
        
        self._clock: _pygame.time.Clock = _pygame.time.Clock()
        self.framerate = framerate
        self.dt: float = 0.0
        self._lt: float = 0.0

        # Hidden Variables
        self._framerate: int = 0
        self._base_framerate: int = base_framerate

    # Clock Attributes
    @property
    def framerate(self) -> int:
        return self._framerate
    
    @framerate.setter
    def framerate(self, f: int) -> None:
        self._framerate = f

    # Juicy Code
    def tick(self) -> None:
        """Updates the Clock.
        """
        
        self.dt = (self._clock.tick(self.framerate) - self._lt) * self._base_framerate
        self._lt = _time()

# Testing
if __name__ == '__main__':
    pass