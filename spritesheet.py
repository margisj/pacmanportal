# Sprite Sheet Class
# USAGE: Constructor takes spritesheet image file
#        To get a single image use get_image(x-coord, y-coord, width of image, height of image)
import pygame


class SpriteSheet(object):

    def __init__(self, file):
        self.spritesheet = pygame.image.load(file).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        return image
