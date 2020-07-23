import gym
env = gym.make('FrozenLake-v0')
observation = env.reset()
print (env.observation_space)
print (env.observation_space.sample())
env.render()
for t in range(100):
    #action = env.action_space.sample()
    action = 0
    observation, reward, done, info = env.step(action)
    env.render()
    print (observation)
    if done:
        break
env.close()