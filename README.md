# snake-ai

## Model
### Feedforward Neural Network (FNN)
- input layer => hidden layer => output layer
- Input states (size 11) and output action (straight, left right) (size 3)

### Deep Q Learning
- Q value = Quality of action
- initialize Q value (init model)
#### Training loop:
1. choose action (mode.predict(state) or random)
2. perform action
3. measure reward
4. update Q value & train model

### Loss Function
- Update the Q value using Bellman equation
- MSE of Q values

## Game
### Action
(Relative to current direction)
- Go straight `[1,0,0]`
- Turn left `[0,1,0]`
- Turn right `[0,0,1]`

### Rewards
- Eat an apple `+10`
- Game over `-10`

### States
Information the model needs to know:
- `danger_straight` snake will hit edge if it goes straight
- `danger_left` snake will hit edge if it goes left
- `danger_right` snake will hit edge if it goes right
- `direction_left` snake is moving left
- `direction_right` snake is moving right
- `direction_up` snake is moving up
- `direction_down` snake is moving down
- `food_left` food is to the left of snake
- `food_right` food is to the right of snake
- `food_up` food is above the snake
- `food_down` food is below the snake