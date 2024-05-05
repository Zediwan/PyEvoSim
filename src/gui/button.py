import pygame

class Button():
    def __init__(self, 
                 pos: tuple[int, int], 
                 text_input: str, 
                 font: pygame.font.Font,
                 base_color: pygame.Color,
                 hovering_color: pygame.Color = None,
                 background_color: pygame.Color = None,
                 background_hover_color: pygame.Color = None,
                 image: pygame.Surface = None
            ) -> None:
        self.image: pygame.Surface = image
        self.x_pos: int = pos[0]
        self.y_pos: int = pos[1]

        self.base_color: pygame.Color = base_color
        self.hovering_color: pygame.Color = hovering_color
        self.background_color: pygame.Color = background_color
        self.background_hover_color: pygame.Color = background_hover_color

        self.text_input: str = text_input
        self.font: pygame.font.Font = font
        self.text: pygame.Surface = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            if self.background_color:
                self.image = pygame.Surface((int(self.text.get_width() * 2), int(self.text.get_height() * 1.2)))
                self.image.fill(self.background_color)
            else:
                self.image = self.text
        self.rect: pygame.Rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect: pygame.Rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self, screen: pygame.Surface):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def check_for_input(self, position: tuple[int, int]) -> bool:
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)
    
    def change_color(self, position: tuple[int, int]):
        if self.check_for_input(position) and self.hovering_color:
            if self.background_hover_color:
                self.image.fill(self.background_hover_color)
            else:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            if self.background_color:
                self.image.fill(self.background_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
