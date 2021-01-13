#! python3

import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
WIDTH_START, HEIGHT_START = 80, 80
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Python Snake')
GAME_WIDTH = 72
GAME_HEIGHT = 72
BACKGROUND = pygame.image.load(os.path.join('Extra', 'background.jpg'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (800, 800))
SNAKE_IMG = pygame.image.load(os.path.join('Extra', 'snake.png'))
SNAKE_IMG = pygame.transform.scale(SNAKE_IMG, (120, 120))
SNAKE_IMG2 = pygame.transform.flip(SNAKE_IMG, True, False)
CLOCK = pygame.time.Clock()
FPS = 15
N = 10
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
DARK_GREEN = (19, 87, 18)
BROWN = (63, 29, 6)
YELLOW = (220, 223, 54)
FONT = pygame.font.SysFont('comicsans', 60)
NICE_FONT = pygame.font.SysFont('CURLZ___', 80, 1)
BEST_SCORE = int(open(os.path.join('Extra', 'best_score.txt'),'r').read())


class Game:
    def __init__(self):
        self.score = 0
        self.snake = [pygame.Rect(GAME_WIDTH // 2 * N, GAME_HEIGHT // 2 * N, N, N)]
        self.fruit = self.generate_fruit()
        self.direction = 'right'
        self.view = 'horizontal'

    def draw_window(self):
        SCREEN.fill(DARK_GREEN)
        text = FONT.render(f'Score: {self.score}', 1, YELLOW)
        text2 = FONT.render(f'Best score: {BEST_SCORE}', 1, YELLOW)
        SCREEN.blit(text2, (480, 20))
        SCREEN.blit(text, (20, 20))
        pygame.draw.line(SCREEN, YELLOW, (0, 78), (800, 78), width=2)
        for sn in self.snake:
            pygame.draw.rect(SCREEN, YELLOW,sn)
        pygame.draw.rect(SCREEN, RED, self.fruit)
        pygame.display.flip()

    def scored(self):
        if self.snake[0].topleft == self.fruit.topleft:
            return True
        return False

    def generate_fruit(self):
        body = [self.snake[i].topleft for i in range(len(self.snake))]
        valid = False
        while not valid:
            x = random.sample([i for i in range(180, WIDTH-180, 10)], 1)[0]
            y = random.sample([i for i in range(180, HEIGHT-180, 10)], 1)[0]
            if not (x, y) in body:
                valid = True
        return pygame.Rect(x, y, N, N)

    def game_over(self):
        body = [self.snake[i].topleft for i in range(1, len(self.snake))]
        if self.snake[0].topleft in body:
            return True
        return False

    def draw_end(self):
        SCREEN.blit(BACKGROUND, (0, 0))
        text = NICE_FONT.render('GAME OVER', 1, RED)
        if self.score > BEST_SCORE:
            text2 = NICE_FONT.render(f'NEW RECORD: {self.score} !', 1, BLACK)
            SCREEN.blit(text2, (70, 300))
        else:
            text2 = NICE_FONT.render(f'BEST SCORE: {BEST_SCORE}', 1, BLACK)
            text3 = NICE_FONT.render(f'YOUR SCORE: {self.score}', 1, BLACK)
            SCREEN.blit(text2, (80, 300))
            SCREEN.blit(text3, (80, 400))
        SCREEN.blit(text, (120, 100))
        pygame.display.flip()

    def end_loop(self):
        running = True
        while running:
            self.draw_end()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
    def increase_size(self):
        # e is a helper variable to add/subtract from either x or y.
        if self.view == 'horizontal':
            if self.direction == 'right':
                # Tail must be added to the left (x - N)
                e = -N
            else:
                # Tail must be added to the right (x + N)
                e = N
            top_x, top_y = self.snake[-1].topleft  # previous tail.
            self.snake.append(pygame.Rect(top_x+e, top_y, N, N))
        else:
            if self.direction == 'down':
                # Tail must be added up (x - N)
                e = -N
            else:
                # Tail must be added down (x + N)
                e = N
            top_x, top_y = self.snake[-1].topleft  # previous tail.
            self.snake.append(pygame.Rect(top_x, top_y+e, N, N))

    def move(self, modif_x, modif_y):
        for sn in self.snake:
            if self.snake.index(sn) == 0:  # head of the snake.
                sn.x, sn.y = sn.x + modif_x, sn.y + modif_y
                to_follow = sn.topleft[0]- modif_x, sn.topleft[1] - modif_y
            else:  # body.
                tmp = sn.topleft  # previous position
                sn.topleft = to_follow  # actual position
                to_follow = tmp
            if sn.y > HEIGHT:  # bottom
                sn.y = 80  # starting at 80 due to stats display.
            if sn.x > WIDTH:  # right
                sn.x = 0
            if sn.y < 80:  # top
                sn.y = HEIGHT # starts at the bottom (max height)
            if sn.x < 0:  # left
                sn.x = WIDTH

    def draw_menu(self):
        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(SNAKE_IMG, (160, 360))
        SCREEN.blit(SNAKE_IMG2, (550, 360))
        text = NICE_FONT.render('PYTHON SNAKE', 1, (100, 100, 100))
        text2 = NICE_FONT.render('PYTHON SNAKE', 1, BLACK)
        text3 = NICE_FONT.render('PLAY', 1, BLACK)
        SCREEN.blit(text, (65, 195))
        SCREEN.blit(text2, (70, 200))
        SCREEN.blit(text3, (300, 360))
        pygame.draw.rect(SCREEN, BLACK, (290, 365, 245, 100), width=3)
        pygame.display.flip()

    def main_menu(self):
        running = True
        rect_area = [(j, i) for i in range(365, 365+100) for j in range(290, 290+245)]
        while running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos in rect_area:
                        running = False


    def main(self):
        self.main_menu()
        modif_x, modif_y = -N, 0
        running = True
        force_quit = False
        while running:
            CLOCK.tick(FPS)
            if self.game_over():
                running = False
                continue
            if self.scored():
                self.score += 1
                self.increase_size()
                self.fruit = self.generate_fruit()
            self.move(modif_x, modif_y)
            self.draw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    force_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and not self.direction == 'down':
                        modif_y, modif_x = -N, 0
                        self.direction = 'up'
                        self.view = 'vertical'
                    if event.key == pygame.K_s and not self.direction == 'up':
                        modif_y, modif_x = N, 0
                        self.direction = 'down'
                        self.view = 'vertical'
                    if event.key == pygame.K_d and not self.direction == 'left':
                        modif_x, modif_y = N, 0
                        self.direction = 'right'
                        self.view = 'horizontal'
                    if event.key == pygame.K_a and not self.direction == 'right':
                        modif_x, modif_y = -N, 0
                        self.direction = 'left'
                        self.view = 'horizontal'
        if self.score > BEST_SCORE:
            with open('best_score.txt', 'w') as fwriter:
                fwriter.write(str(self.score))
        if force_quit:
            pygame.quit()
            exit()
        self.end_loop()

if __name__ == '__main__':
    run = Game()
    run.main()
