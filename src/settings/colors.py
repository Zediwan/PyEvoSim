from pygame import Color
from random import randint

# Simulation
SIMULATION_BACKGROUND_COLOR: Color = Color("white")
MENU_BACKGROUND_COLOR: Color = Color("grey")
STAT_BAR_BACKGROUND_COLOR: Color = Color("grey")
STAT_BAR_BORDER_COLOR: Color = Color("black")
STAT_BAR_FONT_COLOR: Color = Color("black")

# Stat Panel
STAT_PANEL_BACKGROUND_COLOR: Color = Color("black")
STAT_PANEL_FONT_COLOR: Color = Color('white')

# Tile Colors
WATER_COLOR: Color = Color(26, 136, 157)
SAND_COLOR: Color = Color(228,232,202)
SCORCHED_COLOR: Color = Color(153, 153, 153)
BARE_COLOR: Color = Color(187, 187, 187)
TUNDRA_COLOR: Color = Color(221,221,187)
SNOW_COLOR: Color = Color(248,248,248)
TEMPERATE_DESERT_COLOR: Color = Color(228,232,202)
SHRUBLAND_COLOR: Color = Color(195,204,187) 
TAIGA_COLOR: Color = Color(203,212,187)
GRASSLAND_COLOR: Color = Color(196,212,170)
TEMPERATE_DECIDUOUS_FOREST_COLOR: Color = Color(180,200,169)
TEMPERATE_RAIN_FOREST_COLOR: Color = Color(163,196,168)
SUBTROPICAL_DESERT_COLOR: Color = Color(233,220,198)
TROPICAL_SEASONAL_FOREST_COLOR: Color = Color(169,204,163)
TROPICAL_RAIN_FOREST_COLOR: Color = Color(156,187,169)

# Organism Colors
BASE_ORGANISM_COLOR: Color = Color("black")

# Animals Colors
BASE_ANIMAL_COLOR = lambda: Color(randint(0,255), randint(0,255), randint(0,255))

# Plant Colors
BASE_PLANT_COLOR: Color = Color(76, 141, 29)