import uuid
import random

class Creature:
    def __init__(self, energy, mutation_probability) -> None:
        self.energy = energy
        self.identifier = uuid.uuid4()
        self.location = []
        self.brain = None
        self.color=[random.randint(0, 255) for _ in range(3)]
        self.mutation_probability = mutation_probability

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
                
                
        self.brain.mutate(self.mutation_probability)