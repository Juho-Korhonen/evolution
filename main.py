from grid import Grid
from visualize import create_video
import random
from creature import Creature
from neural_network import brain



plate = Grid(150, 10)
plate.initialize()
plate.placeValueInRandomLocation(500, 1) 

simulation_duration = 1000
default_creature_energy = 10
number_of_creatures = 10



creatures = []



for index in range(0,number_of_creatures):
    new_creature = Creature(energy=default_creature_energy)
    randLocation = plate.getRandomEmptyLocation()
    plate.setGrid(randLocation[0], randLocation[1], new_creature.energy)
    new_creature.location = randLocation
    creatures.append(new_creature)

    # creature list contains locations of all creatures, we just display energy of creature, that is all.



for second in range(1, simulation_duration):
    plate.saveGridHistory() 

    print("second " + str(second))
    
    plantLocations = plate.getValueLocations(1)
    for plantLocation in plantLocations:
        spaceforplant = plate.checkIfValueCloseToLocation(plantLocation[0], plantLocation[1], 0)
        if spaceforplant: # if empty space for plant to grow
            plant_should_grow = random.randint(1, 10) == 10
            if plant_should_grow:
                growth_location = plate.getLocationWithValueCloseToLocation(plantLocation[0], plantLocation[1], 0) # gets random location for plant to grow
                if growth_location:
                    plate.setGrid(growth_location[0], growth_location[1], 1) # sets new plant in growth location

    for creature in creatures:
        creature.energy -= 1
        
        
        if(creature.energy > 11):
            new_creature_location = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 0) # get random food if its close
            if(new_creature_location):
                creature.energy -= 6
                
                new_creature = Creature(energy=default_creature_energy)
                
                new_creature.location = new_creature_location
                plate.setGrid(new_creature_location[0], new_creature_location[1], new_creature.energy)
                
                creatures.append(new_creature)
            
        if(creature.energy > 10):
            weakCreatureNearby = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 3) # get random weak creature if its close
            if not weakCreatureNearby:
                weakCreatureNearby = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 4) # get random weak creature if its close
                
            if weakCreatureNearby:
                creature.energy += 3
                plate.setGrid(creature.location[0], creature.location[1], 0)
                plate.setGrid(weakCreatureNearby[0], weakCreatureNearby[1], creature.energy)
                creature.location = weakCreatureNearby
            else:
                freeSpaceNearby = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 0) # get random food if its close
                if(freeSpaceNearby):
                    plate.setGrid(creature.location[0], creature.location[1], 0)
                    plate.setGrid(freeSpaceNearby[0], freeSpaceNearby[1], creature.energy)
                    creature.location = freeSpaceNearby
        
        elif(creature.energy > 3):
            foodNearby = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 1) # get random food if its close
            if foodNearby:
                creature.energy += 2.1
                plate.setGrid(creature.location[0], creature.location[1], 0)
                plate.setGrid(foodNearby[0], foodNearby[1], creature.energy)
                creature.location = foodNearby
            else:
                freeSpaceNearby = plate.getLocationWithValueCloseToLocation(creature.location[0], creature.location[1], 0) # get random food if its close
                if(freeSpaceNearby):
                    plate.setGrid(creature.location[0], creature.location[1], 0)
                    plate.setGrid(freeSpaceNearby[0], freeSpaceNearby[1], creature.energy)
                    creature.location = freeSpaceNearby
        else:
            plate.setGrid(creature.location[0], creature.location[1], 0)
        

            











print("Simulation finished, generating video")


print(plate.grid_history[len(plate.grid_history)-1])
create_video(
    plate.grid_history,
    labels={
        "zero": "Empty",
        "one": "Food",
        "two": "Organism",
    },
    colors={
        "zero": "white",
        "one": "green",
        "two": "#ff0000",   # Red
        "two_to_cyan": "#00ffff"  # Cyan
    },
    fps=4
)
print("Video generated")
