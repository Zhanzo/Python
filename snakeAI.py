from pygame.locals import *
from random import randint
import pygame
import time

class Apple:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x *= self.step
        self.y *= self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Computer:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    update_count_max = 2
    update_count = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        #initial positions, no collision
        self.x[1] = 1*44
        self.y[2] = 2*44

    def update(self):
        self.update_count += 1
        if (self.update_count > self.update_count_max):
            # update previous positions
            for i in range(self.length-1, 0, -1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if (self.direction == 0):
                self.x[0] += self.step
            if (self.direction == 1):
                self.x[0] -= self.step
            if (self.direction == 2):
                self.y[0] -= self.step
            if (self.direction == 3):
                self.y[0] += self.step

            self.update_count = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def target(self, dx, dy):
        if (self.x[0] > dx):
            self.moveLeft()
        if (self.x[0] < dx):
            self.moveRight()
        if (self.x[0] == dx):
            if (self.y[0] < dy):
                self.moveDown()
            if (self.y[0] > dy):
                self.moveUp()

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

class Game:
    def isCollision(self, x1, y1, x2, y2, b_size):
        if (x1 >= x2 and x1 <= x2 + b_size):
            if (y1 >= y2 and y1 <= y2 + b_size):
                return True
        return False
            
class App:
    window_width = 800
    window_height = 600
    apple = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.apple = Apple(5, 5)
        self.computer = Computer(3)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("snake.jpg").convert()
        self._apple_surf = pygame.image.load("apple.jpg").convert()

    def on_event(self, event):
        if (event.type == QUIT):
            self._running = False

    def on_loop(self):
        self.computer.target(self.apple.x, self.apple.y)
        self.computer.update()

        # does snake eat apple?
        for i in range(0,self.computer.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.computer.x[i], self.computer.y[i], 44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.computer.length += 1
                
        # does snake collide with itself?
        for i in range(2, self.computer.length):
            if (self.game.isCollision(self.computer.x[0], self.computer.y[0], self.computer.x[i], self.computer.y[i], 40)):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.computer.x[0]) + "," + str(self.computer.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.computer.x[i]) + "," + str(self.computer.y[i]) + ")")
                exit(0)

        # does snake collide with wall?
        if (self.computer.x[0] >= 800 or self.computer.x[0] < 0 or self.computer.y[0] >= 600 or self.computer.y[0] < 0):
            print("You lose! Collision with wall!")
            print("x[0] (" + str(self.computer.x[0]) + "," + str(self.computer.y[0]) + ")")
            exit(0)
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._image_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if (self.on_init() == False):
            self._running = False
            
        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            
            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(1.0/30.0)
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

    
