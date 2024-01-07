from scripts.simulation.simulation import Simulation

if __name__ == "__main__":
    WIDTH, HEIGHT = 1920, 1080
    NUM_STARTING_ANIMALS = 10
    NUM_STARTING_PLANTS = 100
    
    simulation = Simulation(WIDTH, HEIGHT, NUM_STARTING_ANIMALS, NUM_STARTING_PLANTS)
    simulation.run()