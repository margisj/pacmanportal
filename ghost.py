import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Ghost(Sprite):

    def __init__(self, screen, maze, img, behavior):
        super(Ghost, self).__init__()
        self.screen = screen
        self.sz = 34
        self.spritesheet = SpriteSheet('images/' + img + '.png')
        self.behavior = behavior
        self.images = []
        for i in range(8):
            self.images.append(self.spritesheet.get_image(i*16, 0, 16, 16))
            self.images[i] = pygame.transform.scale(self.images[i], (self.sz, self.sz))
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.center = float(self.rect.centerx)
        # Move to start position
        self.reset()

        self.walls = maze.bricks

        self.speed = 1
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

        self.path = []
        # self.genPath(behavior)
        self.curPath = 1

        self.last = pygame.time.get_ticks()
        self.animIter = 0

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        super().update()
        self.animate()
        if self.moveLeft:
            self.rect.x -= self.speed
            self.checkcoll('left')
        elif self.moveRight:
            self.rect.x += self.speed
            self.checkcoll('right')
        elif self.moveUp:
            self.rect.y -= self.speed
            self.checkcoll('up')
        elif self.moveDown:
            self.rect.y += self.speed
            self.checkcoll('down')

    def stop(self):
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

    def checkcoll(self, direction):
        for wall in self.walls:
            if self.rect.colliderect(wall):
                if direction == 'left':
                    self.rect.left = wall.right
                    self.stop()
                elif direction == 'right':
                    self.rect.right = wall.left
                    self.stop()
                elif direction == 'up':
                    self.rect.top = wall.bottom
                    self.stop()
                elif direction == 'down':
                    self.rect.bottom = wall.top
                    self.stop()
                return False
        return True

    def reset(self):
        self.rect.x = 280 + self.behavior*40
        self.rect.y = 350

    def genpath(self):
        if self.behavior == 0:
            self.path = [(351, 130),
                         (702, 130),
                         (689, 208),
                         (546, 208),
                         (546, 520),
                         (689, 520),
                         (689, 598),
                         (624, 598),
                         (624, 650),
                         (637, 676),
                         (546, 676),
                         (546, 546),
                         (559, 130), ]

    def animate(self):
            if pygame.time.get_ticks() > self.last + 200:
                if self.animIter == 7:
                    self.animIter = 0
                else:
                    self.animIter += 1
                self.image = self.images[self.animIter]
                self.last = pygame.time.get_ticks()
