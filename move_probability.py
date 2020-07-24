
# Move:
# Expected_observation: 
# For 100 times
#     Initialise the environment
#     setup the move 1 (down)
#     play the move
#     If observation = 4, then Add to successful_move_counter
#     If observation != 4, then add to unsucessful_move_counter
# Print results


import gym
env = gym.make('FrozenLake-v0')
# Setup
action = 0
expected_observation = 1
total_runs = 1000
# Counters
successful_move = 0
unsuccessful_move = 0


for _ in range(total_runs):
    env.reset()
    observation, reward, done, info = env.step(action)
    if (observation == expected_observation): 
        successful_move += 1
    else:
        unsuccessful_move += 1

#Print results
print ("Probability of success: " + str(successful_move/total_runs))
print ("Probability of failures: " + str(unsuccessful_move/total_runs))

