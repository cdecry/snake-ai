import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Control the randomness
        self.gamma = 0 # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        
    def get_state(self, game):
        pass

    def remember(self, action, reward, next_state, game_over):
        pass
    
    def train_long_memory(self):
        pass

    def train_short_memory(self, action, reward, next_state, game_over):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    
    while True:
        # Get old state
        state_old = agent.get_state(game)

        # Get move
        final_move = agent.get_action(state_old)
        
        # Perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # save model
            
            print("Game", agent.n_games, "Score", score, "Record:", record)
            # plot

if __name__ == '__main__':
    train()