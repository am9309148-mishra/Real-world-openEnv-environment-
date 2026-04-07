from fastapi import FastAPI, WebSocket
import asyncio, random
from env import OpenEnv
from trainer import select_action, train_step, memory

app = FastAPI()

def explain(a):
    return ["UP","DOWN","LEFT","RIGHT","PICK","DROP"][a]

@app.websocket("/train")
async def train(ws: WebSocket):
    await ws.accept()
    env = OpenEnv()

    for ep in range(100):
        state = env.reset()
        total = 0

        for step in range(50):
            action = select_action(state)
            ns, r, done, _ = env.step(action)

            memory.append((state,action,r,ns,done))

            loss = 0
            if len(memory)>32:
                loss = train_step(random.sample(memory,32))

            state = ns
            total += r

            await ws.send_json({
                "episode":ep,
                "reward":total,
                "loss":loss,
                "state":state,
                "action":action,
                "explanation":explain(action)
            })

            await asyncio.sleep(0.05)
            if done: break
