from segment import Segment

class Apple(Segment):
    def __init__(self, x, y, size):
        Segment.__init__(self, x, y, size)
        self.image.fill((0, 255, 0))
