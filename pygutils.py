
# Libraries
import pygame
from time import time as _time

# Code
class Clock:
    def __init__(self, framerate: int = 300):
        
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate = framerate
        self.dt: float = 0.0
        self._lt: float = 0.0

        # Hidden Variables
        self._framerate: int = 0

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
        
        # Since .tick() already returns time since last call *in milliseconds*
        # we multiply by 1000 to get how much we have to adjust in seconds
        # since everything in the game will hopefully be ran on a rate/sec scale
        self.dt = self._clock.tick(self.framerate) / 1000

# Testing
if __name__ == "__main__":
    pass