import gym
env = gym.make('FrozenLake-v0')
initial_observation = env.reset()
env.render()
# Each iteration is a different move
for t in range(100):
    # Get input from user
    action = input("----------\n" + "Enter an action (0, 1, 2, 3): ")
    action = int(action, 10)
    observation, reward, done, info = env.step(action)
    env.render()
    print ("observation: " + str(observation))
    print ("reward: " + str(reward))
    print ("done: " + str(done))
    print ("info: " + str(info))

    #action = env.action_space.sample()
    if done:
        break
env.close()