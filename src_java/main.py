from simulation import Simulation
from config import *

if __name__ == "__main__":
    simulation = Simulation(HEIGHT, WIDTH, TILE_SIZE)
    simulation.simulate()