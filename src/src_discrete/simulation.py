import config
import pygame
import sys
from world import World
class Simulation:
    game_speed = 60
    
    def __init__(self, height: int, width: int, tile_size : int):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("Evolution Simulation")
        self.screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.world = World(height, width, tile_size)
        self.increase_game_speed = False
        self.decrease_game_speed = False

    def simulate(self):
        """
        The main loop of the simulation. Updates the state of the animals and plants, handles their interactions,
        and manages the spawning of new animals and plants.
        """
        running = True
        is_paused = False
        
        while running:
            event = pygame.event.poll()
            
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused  = not is_paused
                elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_ALT: 
                    config.draw_water_level = not config.draw_water_level
                    self.world.draw(self.screen) 
                elif event.key == pygame.K_2 and pygame.key.get_mods() & pygame.KMOD_ALT: 
                    config.draw_growth_level = not config.draw_growth_level
                    self.world.draw(self.screen) 
                elif event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.increase_game_speed = True
                    self.decrease_game_speed = False
                elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.increase_game_speed = False
                    self.decrease_game_speed = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.increase_game_speed = False
                elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.decrease_game_speed = False
            
            self.handle_game_speed()
                
            if not is_paused:
                self.screen.fill((pygame.Color("white")))  # Fill the screen with a white background
                self.world.update()
                self.world.draw(self.screen) 
                
            pygame.display.flip() 
            self.clock.tick(self.game_speed)  
            
    def handle_game_speed(self):
        if self.game_speed <= 10:
            change_in_game_speed = 1
        elif self.game_speed > 10:
            change_in_game_speed = 10
                
        if self.increase_game_speed:
            self.game_speed += change_in_game_speed
            #print(self.game_speed)
        if self.decrease_game_speed:
            self.game_speed = max(self.game_speed-change_in_game_speed, 1)
            #print(self.game_speed)   