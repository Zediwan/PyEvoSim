import settings.screen_settings
from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation(
        settings.screen_settings.SCREEN_HEIGHT,
        settings.screen_settings.SCREEN_WIDTH,
        settings.screen_settings.TILE_SIZE,
    )
    simulation.simulate()
