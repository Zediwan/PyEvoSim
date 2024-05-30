from abc import ABC, abstractmethod

import pygame
import pygame_menu


class ISimulation(ABC):
    def __init__(self) -> None:
        super().__init__()

        self.drawing = False
        self.running = False

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        self.running = True

    def pause(self) -> None:
        self.running = False

    @abstractmethod
    def quit(self) -> None:
        pass


class IPygameSimulation(ISimulation):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fps_limit=0,
        background_color=pygame.Color("black"),
    ) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface(self.rect.size)
        self.clock = pygame.time.Clock()

        self.fps_limit = fps_limit
        self.background_color = background_color

        self.world: pygame.sprite.GroupSingle

        self.drawing = False
        self.running = False

    def update(self) -> None:
        super().update()
        self.world.update()

    def draw(self, screen: pygame.Surface) -> None:
        super().draw()
        self.surface.fill(self.background_color)
        self.world.draw(self.surface)
        screen.blit(self.surface, self.rect)

    def run(self) -> None:
        self.running = True
        while self.running:
            self.update()

            if self.drawing:
                self.draw(pygame.display.get_surface())

            self.clock.tick(self.fps_limit)

    def quit(self) -> None:
        super().quit()
        pygame.quit()
        exit()


class IPygameMenuSimulation(IPygameSimulation):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fps_limit=0,
        background_color=pygame.Color("black"),
        starting_menu: pygame_menu.Menu = None,
        pause_menu: pygame_menu.Menu = None,
    ) -> None:
        super().__init__(x, y, width, height, fps_limit, background_color)

        if starting_menu is None:
            starting_menu = pygame_menu.Menu(
                "Welcome", self.rect.width, self.rect.height
            )
            starting_menu.add.button("Start", self.run)
            starting_menu.add.button("Quit", self.quit)
        self.starting_menu: pygame_menu.Menu = starting_menu

        if pause_menu is None:
            pause_menu = pygame_menu.Menu("Pause", self.rect.width, self.rect.height)
            pause_menu.add.button("Return", self.run)
            pause_menu.add.button("Quit", self.starting_menu)
        self.pause_menu: pygame_menu.Menu = pause_menu

        self.starting_menu.mainloop(self.surface)

    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.mainloop(self.surface)

            self.update()

            if self.drawing:
                self.draw(pygame.display.get_surface())

            self.clock.tick(self.fps_limit)
