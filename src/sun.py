from pygame import Surface, SRCALPHA, Color, sprite
import math

class Sun(sprite.Sprite):
    def __init__(self, cycle_length=240, max_light_intensity=1.0, max_temperature=35):
        sprite.Sprite.__init__(self)
        
        self.cycle_length = cycle_length
        self.max_light_intensity = max_light_intensity
        self.max_temperature = max_temperature
        self.current_tick = 0  # Tracks the current time within the day-night cycle

    def update(self):
        """
        Updates the sun system state, progressing the day-night cycle.
        """
        self.current_tick = (self.current_tick + 1) % self.cycle_length
                
    def draw(self, screen: Surface):
        temp_surface = Surface(screen.get_size(), SRCALPHA)
        temp_surface.set_alpha(100)
        
        night_color = Color(12, 20, 69)
        day_color = Color(252, 229, 112)
        sun_color = night_color.lerp(day_color, self.get_light_intensity())
        
        temp_surface.fill(sun_color)
        screen.blit(temp_surface, (0, 0))

    def get_light_intensity(self):
        """
        Calculates the current light intensity based on the time of day, with longer periods of darkness.

        Returns:
            float: The current light intensity.
        """
        # Calculate the angle of the sun in the sky based on the current tick
        angle = (self.current_tick / self.cycle_length) * 2 * math.pi
        # Adjust the cosine function to simulate longer periods of darkness
        # You can adjust the multiplier (e.g., 1.5, 2) to control the length of darkness
        intensity = (math.cos(angle * 1.5) + 1) / 2  # Normalize to range [0, 1]
        return intensity * self.max_light_intensity

    def get_temperature(self):
        """
        Calculates the current temperature based on the time of day.

        Returns:
            float: The current temperature.
        """
        # Temperature variation follows the same pattern as light intensity
        intensity = self.get_light_intensity()
        return intensity * self.max_temperature