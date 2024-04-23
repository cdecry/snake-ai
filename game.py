import pygame
from enum import Enum
from collections import namedtuple
import random
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (231,71,29)
LIGHT_RED = (238,117,92)
BLUE1 = (65,111,228)
BLUE2 = (77,124,246)
GREEN1 = (170,215,80)
GREEN2 = (162,209,72)
GREEN3 = (84,140,116)
WHITE = (255,255,255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40
E_DIST = 8

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.reset()
        
    def reset(self):
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.apple = None
        self.add_apple()
        self.frame_iteration = 0

    def add_apple(self):
        x = random.randint(0, (self.w - BLOCK_SIZE ) // BLOCK_SIZE) * BLOCK_SIZE 
        y = random.randint(0, (self.h - BLOCK_SIZE ) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple = Point(x, y)

        if self.apple in self.snake:
            self.add_apple()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        if self.head == self.apple:
            self.score += 1
            reward = 10
            self.add_apple()
        else:
            self.snake.pop()
        
        self.update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt == None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def update_ui(self):
        background = pygame.Surface(self.display.get_size())
        ts, w, h, c1, c2 = BLOCK_SIZE, *background.get_size(), GREEN1, GREEN2
        tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
        [pygame.draw.rect(background, color, rect) for rect, color in tiles]
        
        self.display.blit(background, (0, 0))

        for i in range(len(self.snake)):
            pt = self.snake[i]
            x_pt = pt.x + BLOCK_SIZE // 2
            y_pt = pt.y + BLOCK_SIZE // 2
            center = (x_pt, y_pt)
            if i == 0:
                pygame.draw.circle(self.display, BLUE1, center, BLOCK_SIZE // 2 + 2)
                pygame.draw.circle(self.display, BLUE2, center, BLOCK_SIZE // 2 - 2)

                eyes_center = [(x_pt - E_DIST, y_pt), (x_pt + E_DIST, y_pt)]
                pupils_center = [(x_pt - E_DIST, y_pt + 2), (x_pt + E_DIST, y_pt + 2)]
                
                if self.direction == Direction.UP:
                    pupils_center = [(x_pt - E_DIST, y_pt - 2), (x_pt + E_DIST, y_pt - 2)]
                elif self.direction == Direction.LEFT:
                    eyes_center = [(x_pt, y_pt - E_DIST), (x_pt, y_pt + E_DIST)]
                    pupils_center = [(x_pt - 2, y_pt - E_DIST), (x_pt - 2, y_pt + E_DIST)]
                elif self.direction == Direction.RIGHT:
                    eyes_center = [(x_pt, y_pt - E_DIST), (x_pt, y_pt + E_DIST)]
                    pupils_center = [(x_pt + 2, y_pt - E_DIST), (x_pt + 2, y_pt + E_DIST)]
                
                pygame.draw.circle(self.display, BLUE1, eyes_center[0], 7)
                pygame.draw.circle(self.display, BLUE1, eyes_center[1], 7)
                pygame.draw.circle(self.display, WHITE, eyes_center[0], 4)
                pygame.draw.circle(self.display, WHITE, eyes_center[1], 4)
                pygame.draw.circle(self.display, BLACK, pupils_center[0], 2)
                pygame.draw.circle(self.display, BLACK, pupils_center[1], 2)
            else:
                pygame.draw.circle(self.display, BLUE1, center, BLOCK_SIZE // 2)
                pygame.draw.circle(self.display, BLUE2, center, BLOCK_SIZE // 2 - 4)
            
        center = (self.apple.x + BLOCK_SIZE // 2, self.apple.y + BLOCK_SIZE // 2)
        h_center = (self.apple.x + BLOCK_SIZE // 2 - 4, self.apple.y + BLOCK_SIZE // 2 - 5)
        l_center = (self.apple.x + BLOCK_SIZE // 2, self.apple.y + BLOCK_SIZE // 2 - 12)
        # pygame.draw.rect(self.display, RED, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(self.display, RED, center, BLOCK_SIZE // 2 + 2)
        pygame.draw.circle(self.display, LIGHT_RED, h_center, 4)
        pygame.draw.circle(self.display, GREEN3, l_center, 4)
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def move(self, action):
        cw_dir = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = cw_dir.index(self.direction)

        if action == [1,0,0]:
            new_dir = cw_dir[idx]
        elif action == [0,1,0]:
            new_dir = cw_dir[(idx + 1) % 4]
        else:
            new_dir = cw_dir[(idx - 1) % 4]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)