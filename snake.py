from pygame.locals import *
from random import randint
import pygame


class Apple(pygame.sprite.Sprite):
    size = 40

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill((0, 255, 0))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Segment(pygame.sprite.Sprite):
    size = 40

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([self.size-3, self.size-3])
        self.image.fill((255, 0, 0))
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player():
    snake_segments = []
    size = 37
    margain = 3
    x_change = size + margain
    y_change = 0

    def __init__(self, all_sprites_list):
        for i in range(0, 3):
            x = 250 - (self.size + self.margain) * i
            y = 30
            segment = Segment(x, y)
            self.snake_segments.append(segment)
            all_sprites_list.add(segment)

    def update(self, all_sprites_list):
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = self.snake_segments.pop()
        all_sprites_list.remove(old_segment)

        # Figure out where new segment will be
        x = self.snake_segments[0].rect.x + self.x_change
        y = self.snake_segments[0].rect.y + self.y_change
        segment = Segment(x, y)

        # Insert new segment into the list
        self.snake_segments.insert(0, segment)
        all_sprites_list.add(segment)

    def addSegment(self, all_sprites_list):
        # Figure out where new segment will be
        x = self.snake_segments[0].rect.x + self.x_change
        y = self.snake_segments[0].rect.y + self.y_change
        segment = Segment(x, y)

        # Insert new segment into the list
        self.snake_segments.insert(0, segment)
        all_sprites_list.add(segment)

    def moveRight(self):
        self.x_change = (self.size + self.margain)
        self.y_change = 0

    def moveLeft(self):
        self.x_change = (self.size + self.margain) * -1
        self.y_change = 0

    def moveUp(self):
        self.x_change = 0
        self.y_change = (self.size + self.margain) * -1

    def moveDown(self):
        self.x_change = 0
        self.y_change = (self.size + self.margain)


class Game:
    def isCollision(self, collider, snake_segment, size):
        if (snake_segment.rect.y + size >= collider.rect.y and
                snake_segment.rect.y + size <= collider.rect.y + size):
            if (snake_segment.rect.x >= collider.rect.x and
                    snake_segment.rect.x <= collider.rect.x + size):
                return True
        return False

    def isWallCollision(self, snake_segment, size):
        if (snake_segment.rect.x > 800 or snake_segment.rect.x < 0):
            return True
        elif (snake_segment.rect.y > 800 or snake_segment.rect.y < 0):
            return True
        return False


class App:
    window_width = 800
    window_height = 800
    player = None
    apple = None
    size = 40

    def __init__(self):
        self._running = True
        self._screen = None
        self.all_sprites_list = pygame.sprite.Group()
        self.game = Game()
        self.player = Player(self.all_sprites_list)
        self.apple = Apple(400, 400)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Snake')
        self._running = True
        self.all_sprites_list.add(self.apple)
        self.clock = pygame.time.Clock()

    def on_event(self):
        self._running = False

    def on_loop(self):
        # does snake collide with itself?
        for i in range(2, len(self.player.snake_segments)):
            if (self.game.isCollision(self.player.snake_segments[0],
                                      self.player.snake_segments[i],
                                      self.player.size)):
                self.on_event()

        # does snake collide with wall?
        if (self.game.isWallCollision(self.player.snake_segments[0],
                                      self.size)):
            self.on_event()

        # does snake eat apple?
        if (self.game.isCollision(self.apple,
                                  self.player.snake_segments[0],
                                  self.size)):

            self.player.addSegment(self.all_sprites_list)
            self.all_sprites_list.remove(self.apple)
            self.apple = Apple(randint(1, 10) * self.size,
                               randint(1, 10) * self.size)
            self.all_sprites_list.add(self.apple)

        self.player.update(self.all_sprites_list)

    def on_render(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if (self.on_init() is False):
            self._running = False
        while (self._running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_event()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RIGHT):
                        self.player.moveRight()
                    if (event.key == pygame.K_LEFT):
                        self.player.moveLeft()
                    if (event.key == pygame.K_UP):
                        self.player.moveUp()
                    if (event.key == pygame.K_DOWN):
                        self.player.moveDown()
            self.on_loop()
            self.on_render()
            self.clock.tick(5)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
