import settings.screen
from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation(
        settings.screen.SCREEN_HEIGHT,
        settings.screen.SCREEN_WIDTH,
        settings.screen.TILE_SIZE,
    )
    simulation.simulate()
