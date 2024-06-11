import random
import uuid
import numpy as np

def relu(x):
    return max(0, x)
    
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
    
def generate_weights_for_nodes(number_of_weights, number_of_nodes):
    return np.random.uniform(-0.5, 0.5, (number_of_nodes, number_of_weights)).tolist() # generates weights from -0.5 to 0.5, (number of weights for each node)

def generate_bias(number_of_nodes):
    return np.random.uniform(-0.5, 0.5, number_of_nodes).tolist() # generates random bias from -0.5 to 0.5

class Brain:
    def __init__(self, number_of_output_nodes, number_of_hidden_nodes, biases, weights):
        self.biases = biases
        self.weights = weights
        
        self.number_of_hidden_nodes = number_of_hidden_nodes
        self.number_of_output_nodes = number_of_output_nodes

    def get_output_layer_weights(self):
        return self.weights[len(self.weights)-1]
    
    def get_hidden_layer_weights(self):
        return self.weights[0]
    
    def get_hidden_layer_biases(self):
        return self.biases[0]
    
    def get_output_layer_biases(self):
        return self.biases[len(self.biases)-1]

    def get_first_hidden_layer_node_values(self, inputs):
        calculated_hidden_layer_node_values = []
        
        for hidden_node_index in range(0, self.number_of_hidden_nodes):  # for each hidden layer
            weights_of_hidden_layer_node = self.get_hidden_layer_weights()[hidden_node_index]  # get weights of hidden node
            hidden_layer_node_sum = 0  # set initial node value to zero
            
            for input_node_index, input_node_value in enumerate(inputs):  # for each input
                weighted_value = input_node_value * weights_of_hidden_layer_node[input_node_index] # calculate weighted input node value
                hidden_layer_node_sum += weighted_value  # add weighted input node value to sum of hidden node
                
            hidden_layer_node_sum += self.get_hidden_layer_biases()[hidden_node_index]  # add vias to hidden node sum
            calculated_hidden_layer_node_values.append(relu(hidden_layer_node_sum))  # apply relu to hidden hidden node sum and add to array of hidden nodes
            
        return calculated_hidden_layer_node_values # returns as a list, values of all hidden nodes

    def get_output_node_values(self, prev_layer_values):
        calculated_output_nodes = []
        
        for output_node_index in range(0, self.number_of_output_nodes):  # for each output node
            weights_of_output_layer = self.get_output_layer_weights()[output_node_index]  # get output node weights
            
            output_node_sum = 0  # set initial value to zero
            
            for prev_layer_node_index, prev_layer_node_value in enumerate(prev_layer_values):  # for each input
                weighted_value = prev_layer_node_value * weights_of_output_layer[prev_layer_node_index] # calculate weighted value of connection
                output_node_sum += weighted_value  # add weighted value to output node sum
                
            output_node_sum += self.get_output_layer_biases()[output_node_index]  # add bias to output node sum
            calculated_output_nodes.append(relu(output_node_sum))  # add output layer value to list
            
        return calculated_output_nodes # returns calculated output nodes

    def generate_output(self, inputs):
        hidden_node_values = self.get_first_hidden_layer_node_values(inputs) # calculate inputs passed through hidden layer
        output_nodes = self.get_output_node_values(hidden_node_values) # calculate hidden layer values passed through output later weights etc
        return output_nodes # pass output node values through softmax? now not doing

    def mutate_brain_structure(self, mutation_probability):
        hidden_layer_weights = self.get_hidden_layer_weights()
        hidden_layer_weights = self.get_output_layer_weights()
        
        for node_index, node_weights in enumerate(hidden_layer_weights):
            for index, node_weight in enumerate(node_weights):
                if random.random() < mutation_probability:
                    hidden_layer_weights[node_index][index] += (random.uniform(-0.5, 0.5))
                    
        # ADD MUTATION FOR BIASES AND OUTPUT LAYER WEIGHTS
        
number_of_input_layers = 25
number_of_hidden_nodes = 3
number_of_output_nodes = 4

def create_random_brain_structure(biases=None, weights=None):
    random.seed(uuid.uuid4().int)  # Seed the random number generator with a unique value
    
    if(weights is None):
        weights = [
            generate_weights_for_nodes(number_of_input_layers, number_of_hidden_nodes),
            generate_weights_for_nodes(number_of_hidden_nodes, number_of_output_nodes)
        ]
    if biases is None:
        biases = [
            generate_bias(number_of_hidden_nodes),
            generate_bias(number_of_output_nodes)
        ]
    
    return Brain(
        biases=biases,
        weights=weights,
        number_of_hidden_nodes=number_of_hidden_nodes,
        number_of_output_nodes=number_of_output_nodes,
    )
