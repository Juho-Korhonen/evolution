from grid import Grid
from visualize import create_video
import random
from creature import Creature
from neural_network import brain

plate = Grid(50, 75)
plate.initialize()
plate.placeValueInRandomLocation(1000, 1)  # Placing initial food

simulation_duration = 500
default_creature_energy = 6
number_of_creatures = 150
mutation_probability = 0.05  # 5%


creatures = []

def appendCreature(parent=None):
    new_creature = Creature(energy=default_creature_energy, mutation_probability=mutation_probability)
    if(parent == None):
        new_creature.brain = brain()  # Create brain of creature
    else:
        new_creature.color = parent.color
        new_creature.brain = brain(
            biases = parent.brain.biases.copy(),
            output_layer_weights=[w.copy() for w in parent.brain.output_layer_weights],
            first_layer_weights=[w.copy() for w in parent.brain.first_layer_weights],
        )
    randLocation = plate.getRandomEmptyLocation()
    plate.setGrid(randLocation[0], randLocation[1], new_creature.color)
    new_creature.location = randLocation
    creatures.append(new_creature)
    
    return new_creature

for index in range(number_of_creatures):
    appendCreature()

for second in range(1, simulation_duration):
    plate.saveGridHistory()

    print(f"second {second}")

    # Plant growth logic
    plantLocations = plate.getValueLocations(1)
    for plantLocation in plantLocations:
        spaceforplant = plate.checkIfValueCloseToLocation(plantLocation[0], plantLocation[1], 0)
        if spaceforplant:
            plant_should_grow = random.randint(1, 10) == 10
            if plant_should_grow:
                growth_location = plate.getLocationWithValueCloseToLocation(plantLocation[0], plantLocation[1], 0)
                if growth_location:
                    plate.setGrid(growth_location[0], growth_location[1], 1)

    creatures_to_remove = []

    for creature in creatures:
        creature.energy -= 1

        if creature.energy < 3:
            plate.setGrid(creature.location[0], creature.location[1], 0)
            creatures_to_remove.append(creature)
            continue

        input_matrix = [creature.energy]
        for x_coord in range(creature.location[0] - 2, creature.location[0] + 3):
            for y_coord in range(creature.location[1] - 2, creature.location[1] + 3):
                if (creature.location[0] == x_coord and creature.location[1] == y_coord):
                    continue  # Skip own position
                if x_coord < 0 or x_coord >= plate.x_axel_length or y_coord < 0 or y_coord >= plate.y_axel_length:
                    input_matrix.append(-1)  # Outside of screen
                else:
                    spotvalue = plate.getGrid(x_coord, y_coord)
                    if spotvalue != 1 and spotvalue != 0 and spotvalue != -1: # if its a creature
                        spotvalue = 0  # Everything except food is 0
                    input_matrix.append(spotvalue)
                    

        output_values = creature.brain.generateOutput(input_matrix)

        x_change = 0
        y_change = 0

        if output_values[0] > output_values[1]:
            if creature.location[0] < plate.x_axel_length - 1:
                x_change += 1
        elif output_values[0] < output_values[1]:
            if creature.location[0] > 0:
                x_change -= 1

        if output_values[2] > output_values[3]:
            if creature.location[1] < plate.y_axel_length - 1:
                y_change += 1
        elif output_values[2] < output_values[3]:
            if creature.location[1] > 0:
                y_change -= 1

        new_location = [creature.location[0] + x_change, creature.location[1] + y_change]
        if 0 <= new_location[0] < plate.x_axel_length and 0 <= new_location[1] < plate.y_axel_length:
            value_of_new_location = plate.getGrid(new_location[0], new_location[1])

            if value_of_new_location in [0, 1]:
                if value_of_new_location == 1:
                    creature.energy += 2.1

                plate.setGrid(creature.location[0], creature.location[1], 0)
                creature.location = new_location
                plate.setGrid(creature.location[0], creature.location[1], creature.color)

        if creature.energy > 11:
            new_creature_location = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 0)
            if new_creature_location:
                creature.energy -= 6
                new_creature = appendCreature(parent=creature)
                new_creature.mutate()

    for creature in creatures_to_remove:
        creatures.remove(creature)

print("Simulation finished, generating video")

create_video(
    plate.grid_history,
    labels={
        "zero": "Empty",
        "one": "Food",
    },
    colors = {
        "zero": (255,255,255),  # white
        "one": (0,177,64),  # green
    },
    fps=1,
    grid_size= plate.x_axel_length*plate.y_axel_length
)
print("Video generated")
