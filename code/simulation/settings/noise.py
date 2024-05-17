import random

freq_x1 = 1


def set_freq_x1(value):
    global freq_x1
    freq_x1 = value


freq_y1 = 1


def set_freq_y1(value):
    global freq_y1
    freq_y1 = value


freq_x2 = 2


def set_freq_x2(value):
    global freq_x2
    freq_x2 = value


freq_y2 = 2


def set_freq_y2(value):
    global freq_y2
    freq_y2 = value


freq_x3 = 4


def set_freq_x3(value):
    global freq_x3
    freq_x3 = value


freq_y3 = 4


def set_freq_y3(value):
    global freq_y3
    freq_y3 = value


scale_1 = 1


def set_scale_1(value):
    global scale_1
    scale_1 = value


scale_2 = 0.5


def set_scale_2(value):
    global scale_2
    scale_2 = value


scale_3 = 0.25


def set_scale_3(value):
    global scale_3
    scale_3 = value


offset_x1 = 0


def set_offset_x1(value):
    global offset_x1
    offset_x1 = value


offset_y1 = 0


def set_offset_y1(value):
    global offset_y1
    offset_y1 = value


offset_x2 = 4.7


def set_offset_x2(value):
    global offset_x2
    offset_x2 = value


offset_y2 = 2.3


def set_offset_y2(value):
    global offset_y2
    offset_y2 = value


offset_x3 = 19.1


def set_offset_x3(value):
    global offset_x3
    offset_x3 = value


offset_y3 = 16.6


def set_offset_y3(value):
    global offset_y3
    offset_y3 = value


height_power = 2  # TODO make this a slider in the settings


def set_height_power(value):
    global height_power
    height_power = value


height_fudge_factor = 1.2  # Should be a number near 1


def set_fudge_factor(value):
    global height_fudge_factor
    height_fudge_factor = value


height_freq_x: float = random.uniform(-0.01, 0.01)


def set_height_freq_x(value):
    global height_freq_x
    height_freq_x = value


height_freq_y: float = random.uniform(-0.01, 0.01)


def set_height_freq_y(value):
    global height_freq_y
    height_freq_y = value


moisture_freq_x: float = random.uniform(-0.01, 0.01)


def set_moisture_freq_x(value):
    global moisture_freq_x
    moisture_freq_x = value


moisture_freq_y: float = random.uniform(-0.01, 0.01)


def set_moisture_freq_y(value):
    global moisture_freq_y
    moisture_freq_y = value


moisture: float = 0.5


def set_moisture(value):
    global moisture
    moisture = value


height: float = 0.5


def set_height(value):
    global height
    height = value
