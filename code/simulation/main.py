from simulation import Simulation

# def generate_world():
#     world_rect: pygame.Rect = SCREEN.get_rect().scale_by(.8, .8)
#     tile_size: int = world_rect.width // 120

#     world: World = None
#     drawing = False

#     brush_size = 20
#     brush_outline = 2
#     brush_rect: pygame.Rect = pygame.Rect(0 , 0, brush_size, brush_size)

#     while True:
#         MOUSE_POSITION: tuple[int, int] = pygame.mouse.get_pos()
#         brush_rect.center = (MOUSE_POSITION[0], MOUSE_POSITION[1])

#         if world:
#             world.draw(SCREEN)

#             if world_rect.contains(brush_rect):
#                 # Draw cursor highlight
#                 pygame.draw.rect(
#                     SCREEN,
#                     pygame.Color("white"),
#                     brush_rect,
#                     width=brush_outline
#                 )
#             if drawing:
#                 intersecting_tiles = world.get_tiles(brush_rect)
#                 if intersecting_tiles:
#                     for tile in intersecting_tiles:
#                         change_in_height = 0.01
#                         if tile.height >= change_in_height:
#                             tile.height -= change_in_height
#                     world.refresh_tiles()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 drawing = True
#             if event.type == pygame.MOUSEBUTTONUP:
#                 drawing = False
#             if event.type == pygame.VIDEORESIZE:
#                 generate_world()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame_menu.pygame_menu.Menu._open(world_generation_menu)
#             if world:
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_a:
#                         world.spawn_animals(chance_to_spawn=.01)
#                     elif event.key == pygame.K_p:
#                         world.spawn_plants(chance_to_spawn= .1)

#         pygame.display.update()

if __name__ == "__main__":
    Simulation().mainlopp()