from simulation import Simulation

if __name__ == "__main__":
    WIDTH, HEIGHT = 1200, 1000
    TILE_SIZE = 20
    
    simulation = Simulation(HEIGHT, WIDTH, TILE_SIZE)
    simulation.run()