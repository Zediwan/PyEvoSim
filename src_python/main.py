from simulation.simulation import Simulation

if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    NUM_ANIMALS = 10
    simulation = Simulation(WIDTH, HEIGHT, NUM_ANIMALS)
    simulation.run()