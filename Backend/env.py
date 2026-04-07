import random

class OpenEnv:
    def __init__(self, grid_size=6, max_steps=100):
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.obstacles = [(1,1),(2,3),(3,2)]
        self.reset()

    def reset(self):
        self.agent = [0,0]
        self.pickup = [2,2]
        self.drop = [4,4]
        self.has_package = False
        self.steps = 0
        self.done = False
        return self.get_state()

    def get_state(self):
        return [
            self.agent[0], self.agent[1],
            self.pickup[0], self.pickup[1],
            self.drop[0], self.drop[1],
            int(self.has_package)
        ]

    def step(self, action):
        reward = -1

        if action == 0: self.agent[1] = max(0,self.agent[1]-1)
        elif action == 1: self.agent[1] = min(self.grid_size-1,self.agent[1]+1)
        elif action == 2: self.agent[0] = max(0,self.agent[0]-1)
        elif action == 3: self.agent[0] = min(self.grid_size-1,self.agent[0]+1)

        elif action == 4:
            if self.agent == self.pickup and not self.has_package:
                self.has_package = True
                reward = 20
            else:
                reward = -10

        elif action == 5:
            if self.agent == self.drop and self.has_package:
                reward = 100
                self.done = True
            else:
                reward = -10

        if tuple(self.agent) in self.obstacles:
            reward = -20

        self.steps += 1
        if self.steps >= self.max_steps:
            self.done = True

        return self.get_state(), reward, self.done, {}
