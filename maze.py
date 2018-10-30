import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13

    def __init__(self, screen, mazefile, brickfile, portalfile, shieldfile, pointfile):
        self.screen = screen
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.bricks = []
        self.shields = []
        self.points = []
        self.hportals = []
        self.vportals = []
        self.pills = []

        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.shield = ImageRect(screen, shieldfile, sz, sz)
        self.point = ImageRect(screen, pointfile, int(sz*0.75), int(sz*0.75))
        self.pill = ImageRect(screen, pointfile, int(sz*1.25), int(sz*1.25))
        self.hportal = ImageRect(screen, portalfile, sz, sz)
        self.vportal = self.hportal
        self.vportal.image = pygame.transform.rotate(self.vportal.image, 90)
        self.deltax = self.deltay = Maze.BRICK_SIZE

        self.build()

    def build(self):
        r = self.brick.rect
        rshield = self.shield.rect
        rpoint = self.point.rect
        rhportal = self.hportal.rect
        rvportal = self.vportal.rect
        rpill = self.pill.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                elif col == 'o':
                    self.shields.append(pygame.Rect(ncol * dx, nrow * dy, rshield.width, rshield.height))
                elif col == 'h':
                    self.hportals.append(pygame.Rect(ncol * dx, nrow * dy, rhportal.width, rhportal.height))
                elif col == 'v':
                    self.vportals.append(pygame.Rect(ncol * dx, nrow * dy, rvportal.width, rvportal.height))
                elif col == 'P':
                    self.points.append(pygame.Rect(ncol * dx, nrow * dy, rpoint.width, rpoint.height))
                elif col == 'D':
                    self.pills.append(pygame.Rect(ncol * dx, nrow * dy, rpill.width, rpill.height))
                elif col.isdigit():
                    print(col + row[ncol+1] + ' (', ncol*dx, ',', nrow*dy, '), \n')

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.shields:
            self.screen.blit(self.shield.image, rect)
        for rect in self.hportals:
            self.screen.blit(self.hportal.image, rect)
        for rect in self.vportals:
            self.screen.blit(self.vportal.image, rect)
        for rect in self.points:
            self.screen.blit(self.point.image, rect)
        for rect in self.pills:
            self.screen.blit(self.pill.image, rect)
