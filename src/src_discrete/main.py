from simulation import Simulation

if __name__ == "__main__":
    WIDTH, HEIGHT = 1000, 1000
    TILE_SIZE = 20
    
    simulation = Simulation(WIDTH, HEIGHT, TILE_SIZE)
    simulation.build_world()
    #simulation.run()