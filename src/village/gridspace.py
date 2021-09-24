import random

class GridSpace():
    def __init__(self, buffer_x_min, buffer_x_max, buffer_z_min, buffer_z_max, foundation_size_max):
        self.buffer_left_width = random.randint(buffer_x_min, buffer_x_max)
        self.buffer_left_length = foundation_size_max
        self.buffer_right_width = random.randint(buffer_x_min, buffer_x_max)
        self.buffer_right_length = foundation_size_max
        self.buffer_bottom_width = foundation_size_max + self.buffer_left_width + self.buffer_right_width
        self.buffer_bottom_length = random.randint(buffer_z_min, buffer_z_max)
        self.buffer_top_width = foundation_size_max + self.buffer_left_width + self.buffer_right_width
        self.buffer_top_length = random.randint(buffer_z_min, buffer_z_max - self.buffer_bottom_length)
        self.foundation_container_width = foundation_size_max
        self.foundation_container_length = foundation_size_max
        self.width = self.buffer_bottom_width
        self.length = self.buffer_top_length + self.buffer_left_length + self.buffer_bottom_length
        self.foundation = None