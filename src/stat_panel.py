from pygame import Rect, Color, Surface, SRCALPHA
from pygame.sprite import Sprite
from pygame.font import Font
from pygame.display import get_surface
from helper import format_number

class StatPanel(Sprite):
    offset: tuple[int, int] = (20, 20)
    background_color: Color = Color("black")
    text_color: Color = Color('white')
    alpha: int = 200
    font: Font = Font(None, 20)
    border_size: int = 10
    offset_between_cols: int = 20
    
    def __init__(self, headers: list[str], stats: list[float]):
        Sprite.__init__(self)
        self.headers = headers
        self.stats = stats
        self.rect: Rect
        
        self.name_column_width = 0
        self.value_column_with = 0
        self.total_text_height = 0
        for header in headers:
            self.name_column_width = max(self.name_column_width, self.font.size(header)[0])
            self.total_text_height += self.font.size(header)[1]
        for value in stats:
            v = format_number(value)
            self.value_column_with = max(self.value_column_with, self.font.size(v)[0])
    
        panel_width = self.name_column_width + self.value_column_with + (self.offset_between_cols) + self.border_size * 2
        panel_height = self.total_text_height + self.border_size * 2
                
        self.surface = Surface((panel_width, panel_height), SRCALPHA)
        self.surface.set_alpha(self.alpha)
        
    def draw(self):
        self.surface.fill(self.background_color)
                
        y = self.border_size
        for idx, header in enumerate(self.headers):
            name_surface = self.font.render(header, True, self.text_color)
            self.surface.blit(name_surface, (self.border_size, y))
            
            value_surface = self.font.render(format_number(self.stats[idx]), True, self.text_color)
            self.surface.blit(value_surface, (self.name_column_width + self.offset_between_cols, y))
            
            y += name_surface.get_height()

        main_surface = get_surface()
        main_surface.blit(self.surface, self.rect)
        
    def update(self, base: Rect, stats: list[float]):
        world_width, world_height = get_surface().get_size()
        self.stats = stats
        
        # Calculate the new position for the stat panel
        sp_height = self.surface.get_height()
        sp_width = self.surface.get_width()
        
        new_x_position = base.right + self.offset[0]
        new_y_position = base.bottom + self.offset[1]
        
        if new_x_position + sp_width > world_width:
            new_x_position = base.left - sp_width - self.offset[0]
        if new_y_position + sp_height > world_height:
            new_y_position = base.top - sp_height - self.offset[1]
        
        # Create a new rect for the stat panel at the adjusted position
        self.rect = Rect(new_x_position, new_y_position, sp_width, sp_height)
        