from env import OpenEnv
import random

env = OpenEnv()
s = env.reset()

for _ in range(10):
    a = random.randint(0,5)
    s,r,d,_ = env.step(a)
    print(s,r,d)
