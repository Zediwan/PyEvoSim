import numpy as np

class Transform:
    def __init__(self, position = np.array([0, 0]), velocity = np.array([0, 0]), acceleration = np.array([0, 0]), size = 1):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.size = size

    def copy(self):
        return Transform(
            position = np.copy(self.position),
            velocity = np.copy(self.velocity),
            acceleration = np.copy(self.acceleration),
            size = self.size
        )
    
    def move(self, max_speed):
        assert max_speed >= 0, "max_speed is negative"

        if max_speed == 0:
            return
        else:
            self.velocity += self.acceleration

            self.limit_speed(self, max_speed)

            self.position += self.velocity
            self.acceleration.fill(0)           # Reset Acceleration
    
    def limit_speed(self, max_speed):
        current_speed = np.linalg.norm(self.velocity)
        if current_speed > max_speed:
            self.velocity = np.clip(self.velocity, a_min=0, a_max=max_speed)