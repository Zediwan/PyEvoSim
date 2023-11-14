import random

class DNA:
    def __init__(self, max_health, max_energy, size, max_health_limit, max_energy_limit, max_size_limit):
        self.max_health = min(max_health, max_health_limit)
        self.max_energy = min(max_energy, max_energy_limit)
        self.size = min(size, max_size_limit)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random RGB color