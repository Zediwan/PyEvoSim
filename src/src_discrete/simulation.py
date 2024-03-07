import config
import pygame as pg
import sys
from world import World
class Simulation:
    STARTING_GAME_SPEED = 120
    
    SMALL_BIG_GAME_SPEED_THRESHOLD = 10
    BIG_CHANGE_GAME_SPEED = 10
    SMALL_CHANGE_GAME_SPEED = 1
    MIN_GAME_SPEED = 1
    
    def __init__(self, height: int, width: int, tile_size : int):
        pg.display.init()
        pg.font.init()
        pg.display.set_caption("Evolution Simulation")
        self.screen = pg.display.set_mode((width, height), pg.HWSURFACE | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.world = World(height, width, tile_size)
        
        self.game_speed = self.STARTING_GAME_SPEED
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
            event = pg.event.poll()
            
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    is_paused  = not is_paused
                elif event.key == pg.K_1 and pg.key.get_mods() & pg.KMOD_ALT: 
                    config.draw_water_level = not config.draw_water_level
                    self.world.draw(self.screen) 
                    pg.display.flip() 
                elif event.key == pg.K_2 and pg.key.get_mods() & pg.KMOD_ALT: 
                    config.draw_growth_level = not config.draw_growth_level
                    self.world.draw(self.screen) 
                    pg.display.flip() 
                elif event.key == pg.K_UP and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = True
                    self.decrease_game_speed = False
                elif event.key == pg.K_DOWN and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = False
                    self.decrease_game_speed = True
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = False
                elif event.key == pg.K_DOWN and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.decrease_game_speed = False
            
            self.handle_game_speed()
                
            if not is_paused:
                self.screen.fill((pg.Color("white")))  # Fill the screen with a white background
                self.world.update()
                self.world.draw(self.screen) 
                pg.display.flip() 
                print(self.clock.tick(self.game_speed))
            
    def handle_game_speed(self):
        if self.game_speed <= self.SMALL_BIG_GAME_SPEED_THRESHOLD:
            change_in_game_speed = self.SMALL_CHANGE_GAME_SPEED
        elif self.game_speed > self.SMALL_BIG_GAME_SPEED_THRESHOLD:
            change_in_game_speed = self.BIG_CHANGE_GAME_SPEED
                
        if self.increase_game_speed:
            self.game_speed += change_in_game_speed
            #print(self.game_speed)
        if self.decrease_game_speed:
            self.game_speed = max(self.game_speed - change_in_game_speed, self.MIN_GAME_SPEED)
            #print(self.game_speed)   