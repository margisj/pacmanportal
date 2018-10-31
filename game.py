import pygame
from maze import Maze
from eventloop import EventLoop
from pacman import Pacman
from ghost import Ghost


class Game:
    Black = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((715, 850))
        self.font = pygame.font.SysFont(None, 48)
        pygame.display.set_caption("Pacman Portal")

        self.maze = Maze(self.screen, mazefile='images/pacmanportalmaze.txt',
                         brickfile='square', portalfile='portal', shieldfile='shield', pointfile='point')
        self.pacman = Pacman(self.screen, self.maze)
        self.ghost = []
        self.ghost.append(Ghost(self.screen, self.maze, 'redghost', 0))
        self.ghost.append(Ghost(self.screen, self.maze, 'cyanghost', 1))
        self.ghost.append(Ghost(self.screen, self.maze, 'pinkghost', 2))
        self.ghost.append(Ghost(self.screen, self.maze, 'orangeghost', 3))

        self.score = 0
        self.score_image = None
        self.score_rect = None
        self.screen_rect = self.screen.get_rect()

        self.live_image = self.pacman.images[1]
        self.live_rect = None
        self.lives = 2
        self.start_rect = None
        self.scores_rect = None

        self.titlepac = Pacman(self.screen, self.maze)
        self.titleghost = list()
        self.titleghost.append(Ghost(self.screen, self.maze, 'redghost', 0))
        self.titleghost.append(Ghost(self.screen, self.maze, 'cyanghost', 1))
        self.titleghost.append(Ghost(self.screen, self.maze, 'pinkghost', 2))
        self.titleghost.append(Ghost(self.screen, self.maze, 'orangeghost', 3))


    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def play(self):
        eloop = EventLoop(finished=False)

        while not eloop.finished:
            eloop.check_events(self.pacman, self.start_rect)
            self.update_screen()
            self.pacman.update()
            for ghost in self.ghost:
                ghost.update()

    def update_screen(self):
        self.screen.fill(Game.Black)
        if not self.pacman.active:
            self.prepstartscreen()
        else:
            self.maze.blitme()
            self.pacman.blitme()
            self.prepscore()
            self.preplives()
            for ghost in self.ghost:
                ghost.blitme()

        pygame.display.flip()

    def prepscore(self):
        self.score = self.pacman.getscore()
        score_str = '{:>3}'.format(self.score)
        self.score_image = self.font.render('Score: ' + score_str, True, (255, 255, 255), (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.left + 300
        self.score_rect.top = self.screen_rect.bottom - 30
        self.screen.blit(self.score_image, self.score_rect)

    def preplives(self):
        self.lives = self.pacman.getlives()
        lives_text = self.font.render('Lives: ', True, (255, 255, 255), (0, 0, 0))
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.right = self.screen_rect.left + 500
        lives_text_rect.top = self.screen_rect.bottom - 35
        self.screen.blit(lives_text, lives_text_rect)
        for x in range(self.lives):
            self.live_rect = self.live_image.get_rect()
            self.live_rect.right = self.screen_rect.left + 550 + x*50
            self.live_rect.top = self.screen_rect.bottom - 35
            self.screen.blit(self.live_image, self.live_rect)

    def prepstartscreen(self):
        titleimg = pygame.image.load('images/title.png')
        titleimg = pygame.transform.scale(titleimg, (570, 150))
        title_rect = titleimg.get_rect()
        title_rect = (self.screen_rect.centerx - title_rect.width / 2,
                      (self.screen_rect.centery - title_rect.height / 2) - 250)
        self.screen.blit(titleimg, title_rect)

        self.titlepac.rect.x = 200
        self.titlepac.rect.y = 450
        self.titlepac.update()
        self.titlepac.blitme()

        for x in range(4):
            self.titleghost[x].rect.x = 250 + x*60
            self.titleghost[x].rect.y = 450
            self.titleghost[x].update()
            self.titleghost[x].blitme()

        # Play Button
        startimg = pygame.image.load('images/play.png')
        self.start_rect = startimg.get_rect()
        self.start_rect.x = self.screen_rect.centerx - self.start_rect.width / 2
        self.start_rect.y = self.screen_rect.centery - self.start_rect.height/2 + 250
        self.screen.blit(startimg, self.start_rect)

        # High scores
        scoresimg = pygame.image.load('images/scores.png')
        scoresimg = pygame.transform.scale(scoresimg, (380, 100))
        self.scores_rect = scoresimg.get_rect()
        self.scores_rect.x = self.screen_rect.centerx - self.scores_rect.width / 2
        self.scores_rect.y = self.screen_rect.centery - self.scores_rect.height/2 + 350
        self.screen.blit(scoresimg, self.scores_rect)

    def displayscores(self):
        scoresimg = pygame.image.load('images/scores.png')
        # scoresimg = pygame.transform.scale(scoresimg, (380, 100))
        scores_rect = scoresimg.get_rect()
        scores_rect.x = self.screen_rect.centerx - scores_rect.width / 2
        scores_rect.y = self.screen_rect.centery - scores_rect.height / 2
        self.screen.blit(scoresimg, scores_rect)


game = Game()
game.play()
