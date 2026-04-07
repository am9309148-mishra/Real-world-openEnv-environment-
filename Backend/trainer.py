import torch, random
from collections import deque
from dqn import DQN

model = DQN()
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
memory = deque(maxlen=5000)

gamma = 0.95
epsilon = 1.0

def select_action(state):
    if random.random()<epsilon:
        return random.randint(0,5)
    return torch.argmax(model(torch.tensor(state,dtype=torch.float32))).item()

def train_step(batch):
    states,actions,rewards,next_states,dones = zip(*batch)

    states = torch.tensor(states,dtype=torch.float32)
    next_states = torch.tensor(next_states,dtype=torch.float32)

    q = model(states)
    next_q = model(next_states)

    target = q.clone()

    for i in range(len(batch)):
        target[i][actions[i]] = rewards[i] + gamma*torch.max(next_q[i])*(1-dones[i])

    loss = torch.nn.MSELoss()(q,target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()
