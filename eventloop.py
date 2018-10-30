import pygame
import sys
from pacman import Pacman

class EventLoop:
    def __init__(self, finished):
        self.finished = finished
    def __str__(self):
        return 'eventloop, finished=' + str(self.finished) + ')'

    @staticmethod
    def check_events(pacman, start):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if not pacman.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if start.collidepoint(x, y):
                        pacman.active = True
            else:
                if not pacman.dead:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            pacman.stop()
                            pacman.moveRight = True
                        elif event.key == pygame.K_LEFT:
                            pacman.stop()
                            pacman.moveLeft = True
                        elif event.key == pygame.K_UP:
                            pacman.stop()
                            pacman.moveUp = True
                        elif event.key == pygame.K_DOWN:
                            pacman.stop()
                            pacman.moveDown = True
