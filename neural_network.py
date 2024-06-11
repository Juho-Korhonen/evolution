import random
import uuid
import numpy as np

def relu(x):
    return max(0, x)
    
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
    
def generateRandomWeightsForNodes(number_of_weights, number_of_nodes):
    return np.random.uniform(-0.5, 0.5, (number_of_nodes, number_of_weights)).tolist()

def generateRandomBias(number_of_nodes):
    return np.random.uniform(-0.5, 0.5, number_of_nodes).tolist()

class Brain:
    def __init__(self, number_of_output_layers, number_of_hidden_layers, biases, weights):
        
        self.biases = biases
        
        self.weights = weights
        
        self.hidden_layers = number_of_hidden_layers
        self.output_layers = number_of_output_layers

    def output_layer_weights(self):
        return self.weights[len(self.weights)-1]

    def getFirstHiddenLayerValues(self, inputs):
        calculated_hidden_layers = []
        
        for hidden_layer_index in range(0, self.hidden_layers):  # for each hidden layer
            weights_of_hidden_layer = self.weights[0][hidden_layer_index]  # get weights of first hidden layer
            hidden_layer_value = 0  # set value to zero
            
            for input_index, input_value in enumerate(inputs):  # for each input
                weighted_value = input_value * weights_of_hidden_layer[input_index]
                hidden_layer_value += weighted_value  # add weighted value to hidden layer value
                
            hidden_layer_value += self.biases[0][hidden_layer_index]  # add bias after summing weights
            calculated_hidden_layers.append(relu(hidden_layer_value))  # apply relu to hidden layer value and add to list
            
        return calculated_hidden_layers

    def getOutputValues(self, prev_layer_values):
        calculated_output_layers = []
        
        for output_index in range(0, self.output_layers):  # for each output layer
            weights_of_output_layer = self.output_layer_weights()[output_index]  # get output layer weights of output node
            output_node_value = 0  # set value to zero
            
            for prev_layer_index, prev_layer_value in enumerate(prev_layer_values):  # for each input
                weighted_value = prev_layer_value * weights_of_output_layer[prev_layer_index]
                output_node_value += weighted_value  # add weighted value to output layer value
                
            output_node_value += self.biases[len(self.biases)-1][output_index]  # add bias after summing weights
            calculated_output_layers.append(output_node_value)  # add output layer value to list
            
        return calculated_output_layers

    def generateOutput(self, inputs):
        hidden_node_values = self.getFirstHiddenLayerValues(inputs)
        output_nodes = self.getOutputValues(hidden_node_values)
        return softmax(output_nodes)

    def mutate_brain_structure(self, mutation_probability):
        for node_index, node_weights in enumerate(self.weights[0]):
            for index, node_weight in enumerate(node_weights):
                if random.random() < mutation_probability:
                    self.weights[0][node_index][index] += (random.uniform(-0.5, 0.5))

number_of_input_layers = 25
number_of_hidden_layers = 8
number_of_output_layers = 4

def create_random_brain_structure(biases=None, weights=None):
    random.seed(uuid.uuid4().int)  # Seed the random number generator with a unique value
    
    if(weights is None):
        weights = [
            generateRandomWeightsForNodes(number_of_input_layers, number_of_hidden_layers),
            generateRandomWeightsForNodes(number_of_hidden_layers, number_of_output_layers)
        ]
    if biases is None:
        biases = [
            generateRandomBias(number_of_hidden_layers),
            generateRandomBias(number_of_output_layers)
        ]
    
    return Brain(
        biases=biases,
        weights=weights,
        number_of_hidden_layers=number_of_hidden_layers,
        number_of_output_layers=number_of_output_layers,
    )
