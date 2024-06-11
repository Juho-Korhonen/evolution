import uuid
import random
from neural_network import create_random_brain_structure


class Creature:
    def __init__(self, energy, mutation_probability, brain=None, color=None) -> None:
        self.energy = energy
        self.identifier = uuid.uuid4()
        self.location = []
        self.mutation_probability = mutation_probability
        
        if color is None: # if color is not passed, generate it
            self.color = [random.randint(0, 255) for _ in range(3)]
        else: # if color is passed, set it
            self.color = color
        
        if brain is None: # if brain is not passed, generate completely random brain structure
            self.brain = create_random_brain_structure()
        else:
            self.brain = brain # if brain is passed, set it
        


    def mutate(self):
        if random.random() < self.mutation_probability:
            maxval=1
            minval=-1
            spot_to_change = random.randrange(0,2)
            if(self.color[spot_to_change] < 1):
                minval = 0
            elif(self.color[spot_to_change] > 254):
                maxval = 0
            self.color[spot_to_change] += random.randint(minval, maxval)
                
                
        self.brain.mutate_brain_structure(self.mutation_probability)
        
    def generateOffspring(self, energy):
        offspring = Creature(
            energy = energy, 
            brain = self.brain, 
            color = self.color,
            mutation_probability = self.mutation_probability,
        ) # create a new creature which has same brain, color and mutation probability
        offspring.mutate() # make it possible for the new creature to mutate
        return offspring