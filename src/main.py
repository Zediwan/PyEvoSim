from settings.config import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from simulation import Simulation

if __name__ == "__main__":
    simulation = Simulation(SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE)
    simulation.simulate()
