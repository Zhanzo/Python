from segment import Segment

class Player():
    def __init__(self, all_sprites_list, width, height, size, margain):
        self.size = size
        self.margain = margain
        self.x_change = size + margain
        self.y_change = 0
        self.snake_segments = []

        # Initialize the player with three segments
        for i in range(0, 3):
            x = width - self.x_change * i
            y = height
            segment = Segment(x, y, self.size)
            self.snake_segments.append(segment)
            all_sprites_list.add(segment)

    def update(self, all_sprites_list):
        # Get rid of last segment of the snake
        old_segment = self.snake_segments.pop()
        all_sprites_list.remove(old_segment)

        # Move the snake
        self.add_segment(all_sprites_list)

    def add_segment(self, all_sprites_list):
        # Figure out where new segment will be
        x = self.snake_segments[0].rect.x + self.x_change
        y = self.snake_segments[0].rect.y + self.y_change
        segment = Segment(x, y, self.size)

        # Insert new segment into the list
        self.snake_segments.insert(0, segment)
        all_sprites_list.add(segment)

    def move_right(self):
        if self.x_change == 0:
            self.x_change = self.size + self.margain
            self.y_change = 0

    def move_left(self):
        if self.x_change == 0:
            self.x_change = (self.size + self.margain) * -1
            self.y_change = 0

    def move_up(self):
        if self.y_change == 0:
            self.x_change = 0
            self.y_change = (self.size + self.margain) * -1

    def move_down(self):
        if self.y_change == 0:
            self.x_change = 0
            self.y_change = self.size + self.margain
