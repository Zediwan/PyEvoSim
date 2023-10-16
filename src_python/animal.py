class Animal(Organism):
    MAX_HEALTH = 100
    MAX_ENERGY = 100
    MAX_SIZE = 10
    MAX_SPEED = 10
    
    def __init__(self):
        # Call the constructor of the parent class (Organism)
        super().__init()
        # Add any additional attributes or methods specific to the Animal class