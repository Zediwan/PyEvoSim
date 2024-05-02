import pygame

pygame.font.init()

draw_height_level = False
draw_animal_energy = False
draw_animal_health = False
show_dead_organisms_stats = True

menu_text: float = "Simulation Paused - Menu"
menu_font_size: float = 36
menu_font: pygame.font.Font = pygame.font.Font(None, menu_font_size)
