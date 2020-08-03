
from columnar import columnar

class link:
    def __init__(self, start, finish, weight):
        self.start = start
        self.finish = finish
        self.weight = weight

class node:
    
    def __init__(self, value, is_end_node):
        """

        Args:
            value (int): Position if input, action is end_node
            is_end_node (bool):
        """
        self.value = value
        self.links = []
        self.is_end_node = is_end_node


    def add_link(self, node, weight):
        self.links.append(link(self, node, weight))

    def get_highest_link(self):
        self.links.sort(key=lambda x: x.weight, reverse = True)
        return self.links[0]

    def get_move(self):
        if (self.is_end_node == True):
            return self.value
        else:
            next_node = self.get_highest_link().finish
            return next_node.get_move()

    def is_dead(self):
        one_link_alive = False
        for link in self.links:
            if (link.weight != 0):
                one_link_alive = True
        return not one_link_alive

class network:
    def __init__(self, input_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes

    def train_model(self, env, num_iter):

        input_nodes = self.input_nodes

        modification_factor = 2

        # Each iteration plays a full new game
        for i in range(num_iter):
            self.draw()
            observation = env.reset()
            # Each iteration pays a single move
            for j in range(100):
                # Play
                node = input_nodes[observation]
                link = node.get_highest_link()
                output_node = link.finish
                action = output_node.value
                observation, reward, done, info = env.step(action)
                # Feedback
                if (done and j == 99):
                    break
                if (done and int(reward) == 0):
                    link.weight -= modification_factor
                    break
                if (done and int(reward) == 1):
                    print ("SUCCESS!")
                    return i
                last_node = input_nodes[observation]
                if (last_node.is_dead()):
                    link.weight -= modification_factor
                    break

    def draw(self):
        # Create the data
        data = []
        for node in self.input_nodes:
            row = [f'Node {node.value}:']
            for link in node.links:
                row.append(f"{link.weight}")
            data.append(row)
        
        #Print table
        table = columnar(data, headers=None, no_borders=True)
        print (table)
         
            # print ("Node: " + str(node.value))
            # for i, link in zip(range(0, len(node.links)), node.links):
            #     print (f"   Link {i}: {link.weight}")


def main():
    # Input
    input_nodes = []
    for i in range(0, 16):
        input_nodes.append(node(i, False))   
    # Moves
    output_nodes = []
    for i in range(0, 4):
        output_nodes.append(node(i, True))
    
    # Link nodes 
    default_weight = 10
    for start in input_nodes:
        for finish in output_nodes:
            start.add_link(finish, default_weight)
    
    # Start environment
    import gym
    env = gym.make('FrozenLake-v0')

    model = network(input_nodes, output_nodes)
    model.draw()

    # Train
    num_episodes = model.train_model(env, 1000)

    print ("Solved in " + str(num_episodes) + " episodes.")





if __name__ == "__main__":
    main()