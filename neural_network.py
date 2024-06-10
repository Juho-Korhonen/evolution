# 3 inputs
# 3 hidden layer
import random
import uuid
import numpy as np

def relu(x):
    # turns values lower than 0 to 0
    if x < 0:
        return 0
    else: return x
    
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
    
def generateRandomWeightsForNodes(number_of_weights, number_of_nodes):
    weights_for_nodes = []
    for node in range(0, number_of_nodes):
        weights_for_node = []
        for weight in range(0, number_of_weights):
            weights_for_node.append(random.randint(-10,10))
        weights_for_nodes.append(weights_for_node)
    return weights_for_nodes


def generateRandomBias():
    return random.randrange(-100,100)  
    

class Brain:
    def __init__(self, first_layer_weights, first_bias, output_layer_weights, output_bias, color, mutation_probability, number_of_output_layers, number_of_hidden_layers):
        self.identifier = uuid.uuid4()
        
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
        
        for hidden_layer_index in range(0, self.hidden_layers): # for each hidden layer
            weights_of_hidden_layer = self.first_layer_weights[hidden_layer_index] # get first_layer_weights of hidden layer
            
            hidden_layer_value = 0 # set value to zero
            
            for input_index, input_value in enumerate(inputs): # for each input
                weighted_and_biased_value = input_value * weights_of_hidden_layer[input_index] + self.first_bias # calculate input * weight + bias
                hidden_layer_value += relu(weighted_and_biased_value) # add weighted and biased value to hidden layer value through relu
                
            calculated_hidden_layers.append(hidden_layer_value) # add hidden layer value to list of hidden layer values
        return calculated_hidden_layers
    
    
    
    def getOutputValues(self, prev_layer_values):
        calculated_output_layers = []
        
        for output_index in range(0, self.output_layers): # for each hidden layer
            weights_of_output_layer = self.output_layer_weights[output_index] # get output_layer_weights of hidden layer
            
            output_node_value = 0 # set value to zero
            
            for prev_layer_index, prev_layer_value in enumerate(prev_layer_values): # for each input
                weighted_and_biased_value = prev_layer_value * weights_of_output_layer[prev_layer_index] + self.output_bias # calculate input * weight + bias
                output_node_value += weighted_and_biased_value # add weighted and biased value to hidden layer value through relu
                
            calculated_output_layers.append(output_node_value) # add hidden layer value to list of hidden layer values
        return softmax(calculated_output_layers)
    
    def generateOutput(self, inputs):
        hidden_node_values = self.getFirstHiddenLayerValues(inputs)
        output_nodes = self.getOutputValues(hidden_node_values)
        return output_nodes
    
    def mutate(self):
        shouldMutateColor = random.randint(1, (100/(self.mutation_probability*100))) == 1
        if(shouldMutateColor):
            for color_index in enumerate(self.colors):
                if(self.color[color_index] < 3):
                    self.color[color_index] += random.randrange(0,3)
                elif(self.color[color_index] > 252):
                    self.color[color_index] += random.randrange(-3,0)
                else:
                    self.color[color_index] += random.randrange(-3,3)
                
        for node_index, node_weights in enumerate(self.first_layer_weights):
            for index, node_weight in enumerate(node_weights):
                shouldMutateWeight = random.randint(1, 100/(self.mutation_probability*100)) == 1
                if(shouldMutateWeight):
                    self.first_layer_weights[node_index][index] += (random.randrange(-3, 3) * self.first_layer_weights[node_index][index])
        
                



mutation_probability = 0.2 # 20%
number_of_input_layers = 25
number_of_hidden_layers = 3
number_of_output_layers = 3

def brain():
    return Brain(
        first_layer_weights = generateRandomWeightsForNodes(number_of_input_layers,number_of_hidden_layers),
        first_bias = generateRandomBias(),
        
        output_layer_weights = generateRandomWeightsForNodes(number_of_hidden_layers,number_of_output_layers),
        output_bias = generateRandomBias(),
        
        color = [random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)],
        mutation_probability = mutation_probability,
        number_of_hidden_layers=number_of_hidden_layers,
        number_of_output_layers=number_of_output_layers
    )


jim = brain()

inputs = [
    0,0,0,0,0,
    1,1,0,0,0,
    0,0  ,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    
    8
]

output = jim.generateOutput(inputs)

frase = ""
if(output[0] < 0.5):
    frase = "left"
elif(output[0] > 0.5):
    frase = "right"
else:
    frase = "stay"
    
frase2 = ""
if(output[1] < 0.5):
    frase2 = "down"
elif(output[1] > 0.5):
    frase2 = "up"
else:
    frase2 = "stay"
    
frase3=""
if output[2] >= 0.5:
    frase3 = "yes"
else:
    frase3 = "no"


print("x movement " + frase)
print("y movement " + frase2)
print("try to reproduce " + frase3)

