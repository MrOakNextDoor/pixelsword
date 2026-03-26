
# Libraries
import pygame
from math import sqrt

import pygutils
import gameobject

# Code
class App:
    def __init__(self, display_title: str="Pygame Window", debug: bool=False, icon: pygame.Surface | None = None) -> None:
        
        pygame.init()

        self.debug = debug
        self.icon = icon
        self.display_title = display_title
        self.display: pygame.Surface = pygame.display.set_mode(
            (500, 400), 
            pygame.RESIZABLE)
        self.clock: pygutils.Clock = pygutils.Clock(60)
        self.running: bool = False

        self.test_tile = gameobject.GameObject()
        self.test_collection = gameobject.Collection(self.test_tile)

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

        if self.debug:
            # Add shi here for debug
            pass

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.debug:
                # add shi here for debug
                pass

    def update(self) -> None:
        self.clock.tick()

        self.test_collection.update()
        self.test_tile.position = (self.display.get_width()//2, self.display.get_height()//2)

        if self.debug:
            # Add shi here for debug
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.test_tile.rotation += 30 * self.clock.dt
            if keys[pygame.K_RIGHT]:
                self.test_tile.rotation -= 30 * self.clock.dt
                
            pass

    def render(self) -> None:
        self.display.fill((255, 255, 255))

        self.test_collection.draw(self.display)

        if self.debug:
            # Add shi here for debug

            # このコード最高すぎだよ！
            # dont delete this code!
            # it = pygame.transform.rotate(
            #     pygame.transform.scale(self.test_tile, (64, 64)), 
            #     self.test_tile_rot)
            # t = pygame.transform.scale(it, (it.get_width(), it.get_height()//2))
            # r = self.display.get_rect()
            # tr = t.get_rect()
            # self.display.blit(t, (r.w//2 - tr.w//2, r.h//2 - tr.h//2))

            pass 

        pygame.display.flip()

    def quit(self) -> None:
        if self.debug:
            # Add shi here for debug
            pass

        pygame.quit() 

# Run
if __name__ == "__main__":
    a = App(display_title="Pixelsword", debug=True)
    a.loop()