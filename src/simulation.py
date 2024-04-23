import sys
import pygame as pg

import config
from world import World

class Simulation:
    STARTING_GAME_SPEED: int = 120
    
    SMALL_BIG_GAME_SPEED_THRESHOLD: int = 10
    BIG_CHANGE_GAME_SPEED: int = 10
    SMALL_CHANGE_GAME_SPEED: int = 1
    MIN_GAME_SPEED: int = 1
    
    def __init__(self, height: int, width: int, tile_size : int):
        pg.display.init()
        pg.font.init()
        pg.display.set_caption("Evolution Simulation")
        self.screen = pg.display.set_mode((width, height), pg.HWSURFACE | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.height = height
        self.width = width
        self.tile_size = tile_size
        self.world = World(height, width, tile_size)
        
        self.game_speed: int = self.STARTING_GAME_SPEED
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
                print("Key Pressed", event.key)
                if event.key == pg.K_SPACE:
                    is_paused  = not is_paused
                elif event.key == 13: #TODO: find out enter key name
                    chance_to_spawn_animals = .001
                    self.world.spawn_animals(chance_to_spawn = chance_to_spawn_animals) 
                elif event.key == pg.K_1 and pg.key.get_mods() & pg.KMOD_ALT: 
                    config.draw_height_level = not config.draw_height_level
                    self.world.draw() 
                    pg.display.flip()
                elif event.key == pg.K_UP and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = True
                    self.decrease_game_speed = False
                elif event.key == pg.K_DOWN and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = False
                    self.decrease_game_speed = True
                elif event.key == pg.K_r and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.world = World(self.height, self.width, self.tile_size)
                    self.world.draw() 
                    pg.display.flip() 
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.increase_game_speed = False
                elif event.key == pg.K_DOWN and pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.decrease_game_speed = False
            
            self.handle_game_speed()
                
            if not is_paused:
                self.screen.fill((pg.Color("white")))  # Fill the screen with a white background
                self.world.update()
                self.world.draw() 
                pg.display.flip() 
                self.clock.tick(self.game_speed)
            
    def handle_game_speed(self):
        if self.game_speed <= self.SMALL_BIG_GAME_SPEED_THRESHOLD:
            change_in_game_speed: int = self.SMALL_CHANGE_GAME_SPEED
        else:
            change_in_game_speed: int = self.BIG_CHANGE_GAME_SPEED
                
        if self.increase_game_speed:
            self.game_speed += change_in_game_speed
            #print(self.game_speed)
        if self.decrease_game_speed and self.game_speed >= change_in_game_speed:
            self.game_speed -= change_in_game_speed
            #print(self.game_speed)   