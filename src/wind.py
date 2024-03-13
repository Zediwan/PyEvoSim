import random
from config import *
import math
from pygame import Surface
from config import Direction

class Wind:
    MIN_WIND_SPEED = 0
    MAX_WIND_SPEED = 10
    
    def __init__(self, direction: Direction = Direction.NORTH, speed = 1):
        self.direction = direction
        self.speed = speed

    def update(self, tile):
        possible_directions: list[Direction] = Direction.get_neighboring_directions(self.direction)
        possible_directions.append(self.direction)
        self.direction = random.choice(possible_directions)
        
        self.speed = random.randint(self.MIN_WIND_SPEED, self.MAX_WIND_SPEED)  # Assuming 1 is calm and 5 is strong wind
        
    def draw(self, screen: Surface, tile):
        self.draw_wind_speed(screen, tile)
        self.draw_wind_direction(screen, tile)
        
    def draw_wind_speed(self, screen: Surface, tile):
        from config import draw_wind_speed
        if draw_wind_speed:
            text = font.render(str(math.floor(self.speed)), True, (0, 0, 0))
            text.set_alpha(ground_font_alpha)
            self._render_text_centered(screen, text, tile)
    
    def _render_text_centered(self, screen: Surface, text: Surface, tile):
        """
        Renders the given text surface centered on the tile.

        Args:
            screen (Surface): The surface on which the text will be rendered.
            text (Surface): The text surface to be rendered.
        """
        center_x = tile.rect.x + tile.rect.width // 2
        center_y = tile.rect.y + tile.rect.height // 2
        text_x = center_x - text.get_width() // 2
        text_y = center_y - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
         
    def draw_wind_direction(self, screen: Surface, tile):
        from config import draw_wind_direction
        if not draw_wind_direction:
            return

        # Define the length of the arrow
        arrow_length = 20

        # Calculate the center of the tile
        center_x = tile.rect.x + tile.rect.width // 2
        center_y = tile.rect.y + tile.rect.height // 2

        # Calculate the end point of the arrow based on the wind direction
        if self.direction == Direction.NORTH:
            end_x, end_y = center_x, center_y - arrow_length
        elif self.direction == Direction.SOUTH:
            end_x, end_y = center_x, center_y + arrow_length
        elif self.direction == Direction.EAST:
            end_x, end_y = center_x + arrow_length, center_y
        elif self.direction == Direction.WEST:
            end_x, end_y = center_x - arrow_length, center_y
        else:
            # If the direction is not recognized, do not draw anything
            return

        # Draw the line for the arrow
        pygame.draw.line(screen, pygame.Color("black"), (center_x, center_y), (end_x, end_y), 2)

        # Now, draw the arrowhead. You can adjust the size and the angle of the arrowhead here.
        arrowhead_length = 5
        pygame.draw.line(screen, pygame.Color("black"), (end_x, end_y), (end_x - arrowhead_length, end_y - arrowhead_length), 2)
        pygame.draw.line(screen, pygame.Color("black"), (end_x, end_y), (end_x + arrowhead_length, end_y - arrowhead_length), 2)

        # If the wind direction is vertical (NORTH or SOUTH), the arrowhead should be adjusted accordingly.
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            pygame.draw.line(screen, pygame.Color("black"), (end_x, end_y), (end_x - arrowhead_length, end_y + arrowhead_length), 2)
            pygame.draw.line(screen, pygame.Color("black"), (end_x, end_y), (end_x + arrowhead_length, end_y + arrowhead_length), 2)