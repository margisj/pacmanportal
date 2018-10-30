import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Pacman(Sprite):

    def __init__(self, screen, maze):
        super(Pacman, self).__init__()
        self.screen = screen
        self.sz = 34
        self.spritesheet = SpriteSheet('images/pacman.png')
        self.deathsheet = SpriteSheet('images/death.png')
        self.images = []
        self.death = []
        self.animIter = 1
        self.deathIter = 0
        self.dead = False
        pygame.mixer.init()
        self.chompSound = pygame.mixer.Sound('sounds/pacman_chomp.wav')
        for i in range(3):
            self.images.append(self.spritesheet.get_image(i*32, 0, 32, 32))
            self.images[i] = pygame.transform.scale(self.images[i], (self.sz, self.sz))
        for i in range(14):
            self.death.append(self.deathsheet.get_image(i*16, 0, 16, 16))
            self.death[i] = pygame.transform.scale(self.death[i], (self.sz, self.sz))
        self.rect = self.images[0].get_rect()
        self.center = float(self.rect.centerx)
        self.image = self.images[1]
        self.angle = 0
        self.maze = maze

        self.image = self.images[self.animIter]
        self.walls = self.maze.bricks
        self.points = self.maze.points
        self.pills = self.maze.pills
        self.shields = self.maze.shields

        self.speed = 1
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

        self.last = pygame.time.get_ticks()

        self.score = 0
        self.lives = 2
        self.nextLevel = False
        self.active = False

        # Move to start position
        self.reset()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        super().update()
        self.animate()
        if self.moveLeft:
            self.rect.x -= self.speed
            self.checkcoll()
            self.angle = 180
        elif self.moveRight:
            self.rect.x += self.speed
            self.checkcoll()
            self.angle = 0
        elif self.moveUp:
            self.rect.y -= self.speed
            self.checkcoll()
            self.angle = 90
        elif self.moveDown:
            self.rect.y += self.speed
            self.checkcoll()
            self.angle = 270

    def stop(self):
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

    def checkcoll(self):

        if self.rect.x < 0:
            self.rect.x = self.screen.get_width()
        elif self.rect.x > self.screen.get_width():
            self.rect.x = 0

        for wall in self.walls:
            if self.rect.colliderect(wall):
                if self.moveLeft:
                    self.rect.left = wall.right
                    self.stop()
                elif self.moveRight:
                    self.rect.right = wall.left
                    self.stop()
                elif self.moveUp:
                    self.rect.top = wall.bottom
                    self.stop()
                elif self.moveDown:
                    self.rect.bottom = wall.top
                    self.stop()

        for shield in self.shields:
            if self.rect.colliderect(shield):
                if self.moveLeft:
                    self.rect.left = shield.right
                    self.stop()
                elif self.moveRight:
                    self.rect.right = shield.left
                    self.stop()
                elif self.moveUp:
                    self.rect.top = shield.bottom
                    self.stop()
                elif self.moveDown:
                    self.rect.bottom = shield.top
                    self.stop()

        for index, point in enumerate(self.points):
            if self.rect.colliderect(point):
                del self.points[index]
                self.score += 10
                self.chompSound.play(0, 300)

        for index, pill in enumerate(self.pills):
            if self.rect.colliderect(pill):
                del self.pills[index]
                self.score += 50
                self.chompSound.play(0, 300)

        if len(self.points) == 0 and len(self.pills) == 0:
            self.nextLevel = True
            self.reset()

    def reset(self):
        self.rect.x = 351
        self.rect.y = 585
        self.animIter = 1
        self.deathIter = 0
        self.dead = False
        self.stop()
        self.angle = 0
        if self.nextLevel:
            self.maze.build()
            self.nextLevel = False

    def animate(self):
        if self.dead:
            if pygame.time.get_ticks() > self.last + 100:
                if self.deathIter == 13:
                    self.reset()
                    return
                else:
                    self.deathIter += 1
                self.image = self.death[self.deathIter]
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.last = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() > self.last + 100:
                if self.animIter == 2:
                    self.animIter = 0
                else:
                    self.animIter += 1
                self.image = self.images[self.animIter]
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.last = pygame.time.get_ticks()

    def getscore(self):
        return self.score

    def getlives(self):
        return self.lives

    def die(self):
        self.stop()
        self.dead = True
        if self.lives == 0:
            return
        self.lives -= 1
