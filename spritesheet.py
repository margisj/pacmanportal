import pygame

class SpriteSheet(object):

    def __init__(self, file):
        self.spritesheet = pygame.image.load(file).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image.set_colorkey((0,0,0))

        return image