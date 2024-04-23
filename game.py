import pygame
from enum import Enum
from collections import namedtuple
import random

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
BLUE1 = (65,111,228)
BLUE2 = (77,124,246)
GREEN1 = (170,215,80)
GREEN2 = (162,209,72)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.add_food()

    def add_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE ) // BLOCK_SIZE) * BLOCK_SIZE 
        y = random.randint(0, (self.h - BLOCK_SIZE ) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self.add_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        self.move(self.direction)
        self.snake.insert(0, self.head)
        
        game_over = False
        if self.is_collision():
            game_over = True
            return game_over, self.score
            
        if self.head == self.food:
            self.score += 1
            self.add_food()
        else:
            self.snake.pop()
        
        self.update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score
    
    def is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def update_ui(self):
        background = pygame.Surface(self.display.get_size())
        ts, w, h, c1, c2 = BLOCK_SIZE, *background.get_size(), GREEN1, GREEN2
        tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
        [pygame.draw.rect(background, color, rect) for rect, color in tiles]
        
        self.display.blit(background, (0, 0))

        for pt in self.snake:
            center = (pt.x + BLOCK_SIZE // 2, pt.y + BLOCK_SIZE // 2)
            pygame.draw.circle(self.display, BLUE1, center, BLOCK_SIZE // 2)
            pygame.draw.circle(self.display, BLUE2, center, (BLOCK_SIZE // 2) - 2)
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
    pygame.quit()