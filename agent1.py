
import gym
from columnar import columnar
import logging

class Link:
    def __init__(self, start, finish, weight):
        self.start = start
        self.finish = finish
        self.weight = weight

    def update(self, update_value):
        """Add (positive or negative) update value to the weight 

        Args:
            update_value (int): value to use for update
        """
        self.weight += update_value
        # Make sure that weight is min 0
        if (self.weight<0):
            self.weight = 0

class Node:
    
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
        self.links.append(Link(self, node, weight))

    def get_highest_link(self):
        """Get this node's link with the highest weight

        Returns:
            link: [description]
        """
        return max(self.links, key=lambda x: x.weight)

    def get_move(self):
        if (self.is_end_node == True):
            return self.value
        else:
            next_node = self.get_highest_link().finish
            return next_node.get_move()

    def is_dead(self):
        one_link_alive = False
        for link in self.links:
            if (link.weight > 0):
                one_link_alive = True
        return not one_link_alive

class Network:
    def __init__(self, input_nodes, output_nodes, modification_factor, log_file_name):
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.modification_factor = modification_factor
        logging.basicConfig(filename=log_file_name,filemode='w', level=logging.DEBUG)

    def train_model(self, env, num_iter):
        """Train the neural network to solve the "FrozenLake" puzzle

        Args:
            env (TimeLimit): OpenAI environment
            num_iter (int): Maximum number of game that can be played

        Returns:
            int: number of game played before the agent is able to succeed
        """
        # Each iteration plays a full new game
        prev_snapshot = self.get_snapshot()
        for i in range(num_iter):
            # Log if change was made to network
            snapshot = self.get_snapshot()
            if (prev_snapshot == snapshot):
                logging.debug("CHANGES: NO")
            else:
                logging.debug("CHANGES: YES")
            logging.debug(self.to_string())
            prev_snapshot = snapshot

            observation = env.reset()
            # Each iteration pays a single move
            for j in range(100):
                # Get move
                node = self.input_nodes[observation]
                link = node.get_highest_link()
                output_node = link.finish
                action = output_node.value
                # Play
                observation, reward, done, info = env.step(action)
                # Feedback
                
                if (done and j == 99):
                    logging.debug("SHOULD CHANGE: NOTHING")
                    logging.debug("END: DID NOT FINISH")
                    break
                if (done and int(reward) == 0):
                    logging.debug(f"SHOULD CHANGE: Node {link.start.value}, link {action}")
                    logging.debug("END: HOLE")
                    link.update(-self.modification_factor)
                    break
                if (done and int(reward) == 1):
                    logging.debug("SHOULD CHANGE: NOTHING")
                    logging.debug("END: SUCCESS!")
                    # return i
                # Decrease weight if went to dead node
                last_node = self.input_nodes[observation]
                if (last_node.is_dead()):
                    logging.debug(f"SHOULD CHANGE: Node {link.start.value}, link {action}")
                    logging.debug("END: DEAD NODE")
                    link.weight -= self.modification_factor
                    break
        # return num_successes


    def to_string(self):
        # Create the data
        data = []
        for node in self.input_nodes:
            row = [f'Node {node.value}:']
            for link in node.links:
                row.append(f"{link.weight}")
            data.append(row)
        
        #Print table
        table = columnar(data, headers=None, no_borders=True)
        return (table)

    def get_snapshot(self):
        """Get a snapshot of the network by creating a string out of it

            Return: network as a string
        """
        snapshot = ''
        for node in self.input_nodes:
            snapshot += f'_Node{node.value}:'
            for link in node.links:
                snapshot += str(link.weight)
        return snapshot



def main():
    # Create input nodes
    input_nodes = []
    for i in range(0, 16):
        input_nodes.append(Node(i, False))   
    # Create output nodes
    output_nodes = []
    for i in range(0, 4):
        output_nodes.append(Node(i, True))
    
    # Link input and output together
    default_weight = 10
    for start in input_nodes:
        for finish in output_nodes:
            start.add_link(finish, default_weight)
    
    # Create wrapper network object
    model = Network(input_nodes, output_nodes, 2, "test.log")

    snap1 = model.get_snapshot()
    snap2 = model.get_snapshot()
    

    # Start environment
    env = gym.make('FrozenLake-v0')

    # Train
    num_episodes = model.train_model(env, 150)

    print ("Solved in " + str(num_episodes) + " episodes.")

    print (model.to_string())



if __name__ == "__main__":
    main()