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
    def __init__(self, first_layer_weights, first_bias, output_layer_weights, output_bias, color, mutation_probability, number_of_output_layers, number_of_hidden_layers, identifier):
        self.identifier = identifier
        
        self.first_bias = first_bias
        self.output_bias = output_bias
        self.hidden_layers = number_of_hidden_layers
        self.output_layers = number_of_output_layers
        
        self.first_layer_weights = first_layer_weights
        self.output_layer_weights = output_layer_weights
        
        self.color = color
        self.mutation_probability = mutation_probability

    def getFirstHiddenLayerValues(self, inputs):
        calculated_hidden_layers = []
        
        for hidden_layer_index in range(0, self.hidden_layers):  # for each hidden layer
            weights_of_hidden_layer = self.first_layer_weights[hidden_layer_index]  # get first_layer_weights of hidden layer
            hidden_layer_value = 0  # set value to zero
            
            for input_index, input_value in enumerate(inputs):  # for each input
                weighted_value = input_value * weights_of_hidden_layer[input_index]
                hidden_layer_value += weighted_value  # add weighted value to hidden layer value
                
            hidden_layer_value += self.first_bias[hidden_layer_index]  # add bias after summing weights
            calculated_hidden_layers.append(relu(hidden_layer_value))  # apply relu to hidden layer value and add to list
            
        return calculated_hidden_layers

    def getOutputValues(self, prev_layer_values):
        calculated_output_layers = []
        
        for output_index in range(0, self.output_layers):  # for each output layer
            weights_of_output_layer = self.output_layer_weights[output_index]  # get output_layer_weights of hidden layer
            output_node_value = 0  # set value to zero
            
            for prev_layer_index, prev_layer_value in enumerate(prev_layer_values):  # for each input
                weighted_value = prev_layer_value * weights_of_output_layer[prev_layer_index]
                output_node_value += weighted_value  # add weighted value to output layer value
                
            output_node_value += self.output_bias[output_index]  # add bias after summing weights
            calculated_output_layers.append(output_node_value)  # add output layer value to list
            
        return calculated_output_layers

    def generateOutput(self, inputs):
        hidden_node_values = self.getFirstHiddenLayerValues(inputs)
        output_nodes = self.getOutputValues(hidden_node_values)
        return softmax(output_nodes)

    def mutate(self):
        if random.random() < self.mutation_probability:
            self.color = [max(0, min(255, c + random.randint(-3, 3))) for c in self.color]
        
        for node_index, node_weights in enumerate(self.first_layer_weights):
            for index, node_weight in enumerate(node_weights):
                if random.random() < self.mutation_probability:
                    self.first_layer_weights[node_index][index] += (random.uniform(-0.5, 0.5))

mutation_probability = 0.05  # 5%
number_of_input_layers = 24
number_of_hidden_layers = 5
number_of_output_layers = 4

def brain(identifier, first_layer_weights=None, output_layer_weights=None, first_bias=None, output_bias=None):
    random.seed(uuid.uuid4().int)  # Seed the random number generator with a unique value
    
    if first_layer_weights is None:
        first_layer_weights = generateRandomWeightsForNodes(number_of_input_layers, number_of_hidden_layers)
    if output_layer_weights is None:
        output_layer_weights = generateRandomWeightsForNodes(number_of_hidden_layers, number_of_output_layers)
    if first_bias is None:
        first_bias = generateRandomBias(number_of_hidden_layers)
    if output_bias is None:
        output_bias = generateRandomBias(number_of_output_layers)
    
    return Brain(
        first_layer_weights=first_layer_weights,
        first_bias=first_bias,
        output_layer_weights=output_layer_weights,
        output_bias=output_bias,
        color=[random.randint(0, 255) for _ in range(3)],
        mutation_probability=mutation_probability,
        number_of_hidden_layers=number_of_hidden_layers,
        number_of_output_layers=number_of_output_layers,
        identifier=identifier
    )