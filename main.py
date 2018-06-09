from pygame.locals import *
from random import randint
import pygame
from apple import Apple
from segment import Segment
from player import Player
from game import Game

class App:
    window_width = 400
    window_height = 400
    player = None
    apple = None
    size = 9
    margain = 1

    def __init__(self):
        self._running = True
        self._screen = None
        self.all_sprites_list = pygame.sprite.Group()
        self.game = Game()
        self.player = Player(self.all_sprites_list, self.window_width/2,
                                self.window_height/2, self.size, self.margain)
        self.apple = Apple(self.window_width/2, self.window_height/2,
                self.size)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Snake')
        self._running = True
        self.all_sprites_list.add(self.apple)
        self.clock = pygame.time.Clock()

    def on_exit(self):
        self._running = False

    def on_loop(self):
        # does snake collide with itself?
        for i in range(2, len(self.player.snake_segments)):
            if (self.game.is_collision(self.player.snake_segments[0],
                                      self.player.snake_segments[i],
                                      self.player.size)):
                self.on_exit()

        # does snake collide with wall?
        if (self.game.is_wall_collision(self.player.snake_segments[0],
                                      self.size, self.window_width,
                                      self.window_height)):
            self.on_exit()

        # does snake eat apple?
        if (self.game.is_collision(self.apple,
                                  self.player.snake_segments[0],
                                  self.size)):

            self.player.add_segment(self.all_sprites_list)
            self.all_sprites_list.remove(self.apple)
            self.apple = Apple(randint(0, self.window_width/10-1) * 
					(self.size + self.margain),
                               randint(0, self.window_height/10-1) * 
					(self.size + self.margain),
                               self.size)
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
                    self.on_exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RIGHT):
                        self.player.move_right()
                    if (event.key == pygame.K_LEFT):
                        self.player.move_left()
                    if (event.key == pygame.K_UP):
                        self.player.move_up()
                    if (event.key == pygame.K_DOWN):
                        self.player.move_down()
                    if (event.key == pygame.K_ESCAPE):
                        self.on_exit()
            self.on_loop()
            self.on_render()
            self.clock.tick(20)
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
