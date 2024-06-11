from grid import Grid
from visualize import create_video
import random
from creature import Creature
from neural_network import brain

plate = Grid(100, 100)
plate.initialize()
plate.placeValueInRandomLocation(7500, 1)  # Placing initial food

simulation_duration = 10
default_creature_energy = 6
number_of_creatures = 2000

creatures = []

for index in range(number_of_creatures):
    new_creature = Creature(energy=default_creature_energy)
    new_creature.brain = brain()  # Create brain of creature
    randLocation = plate.getRandomEmptyLocation()
    plate.setGrid(randLocation[0], randLocation[1], new_creature.brain.color)
    new_creature.location = randLocation
    creatures.append(new_creature)

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

        input_matrix = []
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
                plate.setGrid(creature.location[0], creature.location[1], creature.brain.color)

        if creature.energy > 11:
            new_creature_location = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 0)
            if new_creature_location:
                creature.energy -= 6
                new_creature = Creature(energy=default_creature_energy)
                new_creature.brain = brain(
                    first_bias=creature.brain.first_bias.copy(),
                    output_bias=creature.brain.output_bias.copy(),
                    output_layer_weights=[w.copy() for w in creature.brain.output_layer_weights],
                    first_layer_weights=[w.copy() for w in creature.brain.first_layer_weights],
                )
                new_creature.brain.mutate()

                new_creature.location = new_creature_location
                plate.setGrid(new_creature_location[0], new_creature_location[1], new_creature.brain.color)
                creatures.append(new_creature)

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
