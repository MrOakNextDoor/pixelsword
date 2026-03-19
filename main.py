
# Libraries
import pygame
import pygutils

# Code
class App:
    def __init__(self, debug: bool=True, display_title: str='Pygame Window', icon: pygame.Surface | None = None) -> None:
        
        pygame.init()

        self.icon = icon
        self.display: pygame.Surface = pygame.display.set_mode(
            (500, 400), 
            pygame.RESIZABLE)
        self.clock: pygutils.Clock = pygutils.Clock()
        self.running: bool = False

        # Hidden Variables
        self.display_title = display_title

    # App Attributes
    @property
    def display_title(self) -> str:
        return self._display_title
    
    @display_title.setter
    def display_title(self, d: str) -> None:
        self._display_title = d
        pygame.display.set_caption(self.display_title)

    @property
    def icon(self) -> pygame.Surface | None:
        return self._icon
    
    @icon.setter
    def icon(self, i: pygame.Surface | None) -> None:
        if i is not None:
            self._icon = i
            pygame.display.set_icon(i)

    # Actual juicy code
    def loop(self) -> None:
        
        self.start()
        while self.running:
            self.update()
            self.check_events()
            self.render()
        self.quit()

    def start(self) -> None:
        self.running = True

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.clock.tick()

    def render(self) -> None:
        self.display.fill((255, 255, 255))

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit() 

# Run
if __name__ == '__main__':
    a = App()
    a.loop()