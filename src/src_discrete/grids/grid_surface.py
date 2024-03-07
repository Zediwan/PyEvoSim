from grids.grid_base import Grid
from tiles.tile_base import Tile

class GridSurface(Grid):
    def __init__(self, rows: int, cols: int, tile_size: int):
        super().__init__(rows, cols, tile_size)
        
    def create_tile(self, col, row) -> Tile:
        #rect = pg.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        #return Tile(rect, self.tile_size)
        return super().create_tile(col, row)