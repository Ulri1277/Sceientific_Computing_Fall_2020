# Importing packages

import numpy as np
import pygame
import random

# making color codes for the different object and there stages

# Tree
ColorOfNewTree = (171, 235, 198)    # Light Green
ColorOFYoungTree = (39, 174, 96)    # Green
ColorOfGrowingTree = (25, 111, 61)  # Dark Green
ColorOfDyingTree = (165, 99, 99)    # Red-ish Brown

# Water
ColorOfWaterSource = (0, 249, 249)      # Cyan
ColorOfWaterSourceAged = (40, 116, 166) # Dark Blue

# Color code for the grid and Empty spaces.
ColorEmpty = (213, 196, 161)    # Kaki
ColorGrid = (30, 30, 60)        # Blue-ish Black

# States the variables connected to the screens speed and efficiency.
FramesPerSec = 60
Speed = 45

# Initialization of variables connected to the trees growth or reproduction.
ID = 0
TreeReproductionAge = 5  # When the Tree is 5 runs old, it can reproduce.
TreeOverGrowing = 3  # Indicated the amount of trees that can be alive near each other.
TreeHydration= 10  # The Tree will die if it has no more water, this happens after 10 rounds.
WaterSourceAging = 2  # When the Water Source have been sustained for two rounds, a new Water Source is made.
WaterDriesOut = 3  # If a Water Source is touching 3 other Water Sources, it dries out.


# Defining the objects and their attributes:
def NewTree():
    global ID
    Tree = {'Type': 'Tree',
            'ID': ID,
            'Age': 0,
            'Hydration': TreeHydration,
            'Color': ColorOfNewTree}
    ID += 1
    return Tree


def NewSourceOfWater():
    global ID
    WaterSource = {'Type': 'WaterSource',
                   'ID': ID,
                   'Age': 0,
                   'Color': ColorOfWaterSource}
    ID += 1
    return WaterSource


def Empty():
    return {'Type': 'Empty'}


# Defining and initializing the grid from dimensions and the objects.
def init(DimensionX, DimensionY, NewTrees, WaterSource):
    # Create a list that represents the grid.
    ContentsList = []

    # Loops there looks for objects and put them into lists; a list for each object.
    for i in range(NewTrees):
        ContentsList.append(NewTree())

    for i in range(WaterSource):
        ContentsList.append(NewSourceOfWater())

    # A loop for the empty spaces in the grid:
    for i in range((DimensionX * DimensionY - Tree - WaterSource)):
        ContentsList.append(Empty())
    random.shuffle(ContentsList)

    # Reshape the grid in random order, inform a list to a array in 1- dimension, this is done by Typecasting
    ContentsListToArray = np.array(ContentsList)
    Cells = np.reshape(ContentsListToArray, (DimensionY, DimensionX))

    return Cells


# Make a function that checks for Neighbours for a given object.
def GetNeighbours(Current, Row, Column):
    # Define the row/ columns minimum:
    Row_min, Column_min = 0, 0

    # Defines the row and columns max as the shape from line 80:
    Row_max, Column_max = Current.shape
    Row_max, Column_max = Row_max - 1, Column_max - 1  # it's off by one

    # Makes/ initializes a list for the Neighbours found.
    Neighbours = []

    # If statement for the neighbour cells and
    # how the object are put into the grid out from there placement in relation to the current object.
    if Row - 1 >= Row_min:
        if Column - 1 >= Column_min:
            Neighbours.append((Row - 1, Column - 1))

        Neighbours.append((Row - 1, Column))  # Column is inside Current

        if Column + 1 <= Column_max:
            Neighbours.append((Row - 1, Column + 1))

    # Row:
    if Column - 1 >= Column_min:
        Neighbours.append((Row, Column - 1))

    # Skip center (Row,Column) since we are listing its neighbour positions
    if Column + 1 <= Column_max:
        Neighbours.append((Row, Column + 1))

    # Row+1:
    if Row + 1 <= Row_max:

        if Column - 1 >= Column_min: Neighbours.append((Row + 1, Column - 1))
        Neighbours.append((Row + 1, Column))  # Column is inside Current

        if Column + 1 <= Column_max: Neighbours.append((Row + 1, Column + 1))

    return Neighbours


# Divide the neighbour cells into list out from there object type (typecasting)
def CellNeighbours(Current, Neighbours):
    # Divide the Neighbours: Tree, Empty and Water into lists
    TreeNeighbours = []
    EmptyNeighbours = []
    WaterNeighbours = []

    # Loop there checks the type of object and sets it into the end of the list match to its type:
    for neighbour in Neighbours:
        if Current[neighbour]['Type'] == "Tree":
            TreeNeighbours.append(neighbour)

        elif Current[neighbour]['Type'] == "WaterSource":
            WaterNeighbours.append(neighbour)

        else:
            EmptyNeighbours.append(neighbour)

    return TreeNeighbours, WaterNeighbours, EmptyNeighbours


# Defines function for how the tree reproduces and moves around in the grid
def RulesForTrees(Current, Row, Column, WaterNeighbours, NeighboursTree, NeighboursEmpty):
    # If-else statement there checks for the trees Age and color them out from
    # the given rules for reproduction or growth:
    if Current[Row, Column]['Age'] >= TreeReproductionAge:
        Current[Row, Column]['Color'] = ColorOfGrowingTree
    else:
        Current[Row, Column]['Color'] = ColorOFYoungTree

    if Current[Row, Column]['Hydration'] <= 3:
        Current[Row, Column]['Color'] = ColorOfDyingTree

    # If there is a WaterSource, the Tree will hydrate:
    if len(WaterNeighbours) > 0:
        Current[Row, Column]['Hydration'] = TreeHydration

        # Removes a water source as the tree absorbed the water
        Row_WaterSource, Column_WaterSource = random.choice(WaterNeighbours)

        WaterNeighbours.remove((Row_WaterSource, Column_WaterSource))

        NeighboursEmpty.append((Row_WaterSource, Column_WaterSource))
        Current[Row_WaterSource, Column_WaterSource] = Empty()

        # The Hydration are updated by adding 10
        Current[Row, Column]['Hydration'] += 10

        # Reproduction if-else statement there checks if the tree is under the reproduction Age
        # and length of the neighbour-Empty list is over zero. if this is true there is made a new tree
        if Current[Row, Column]['Age'] >= TreeReproductionAge and len(NeighboursEmpty) > 0:
            # Tree breeds to an Empty cell
            Row_new, Column_new = random.choice(NeighboursEmpty)
            Current[Row_new, Column_new] = NewTree()

            # Make a new tree in a random space in the grid and removes this space form the Empty neighbour list
            NeighboursTree.append((Row_new, Column_new))
            NeighboursEmpty.remove((Row_new, Column_new))
    else:
        # Decrease Hydration:
        Current[Row, Column]['Hydration'] -= 1

        # If the Tree is dried out, it dies:
        if Current[Row, Column]['Hydration'] == 0:
            Current[Row, Column] = Empty()

    # The Tree dies (overcrowding) if there are 6 or more neighbouring Tree
    if len(NeighboursTree) >= TreeOverGrowing:
        Current[Row, Column] = Empty()

    return Current


# Defines rules for water sources and how are the made and removed in relation to the other objects in our grid
def RulesForWater(Current, Row, Column, WaterNeighbours, NeighboursEmpty):
    if Current[Row, Column]['Age'] >= WaterSourceAging:
        Current[Row, Column]['Color'] = ColorOfWaterSourceAged
    else:
        Current[Row, Column]['Color'] = ColorOfWaterSource

    # If the length of the neighbour-Empty list is over zero. If this is true, a new Water Source is made:
    if Current[Row, Column]['Age'] >= WaterSourceAging and len(NeighboursEmpty) > 0:

        # Tree breeds to an Empty cell
        Row_new, Column_new = random.choice(NeighboursEmpty)
        Current[Row_new, Column_new] = NewSourceOfWater()

        # Make a new tree in a random space in the grid and removes this space form the Empty neighbour list:
        WaterNeighbours.append((Row_new, Column_new))
        NeighboursEmpty.remove((Row_new, Column_new))

    # The Water Source dries out if there are too many Water Sources:
    if len(WaterNeighbours) >= WaterDriesOut:
        Current[Row, Column] = Empty()

    # If it does not dried out:
    elif len(NeighboursEmpty) > 0:
        Row_new, Column_new = random.choice(NeighboursEmpty)
        Current[Row_new, Column_new] = Current[Row, Column]
        Current[Row, Column] = Empty()

    return Current


# defines a function there updates the cells in the grid and reshape the grid, are given tree inputs
# as we uses it later on to draw our representation of the grid:
def update_status(Surface, Current, Size):
    # For each cell
    for Row, Column in np.ndindex(Current.shape):
        # If there are a Tree in the cell it update the trees Age
        if Current[Row, Column]['Type'] == "Tree" or Current[Row, Column]['Type'] == "WaterSource":
            Current[Row, Column]['Age'] += 1

            # Calculate the Neighbours( Empty/ occupied) and there placement(row, column position)
            # in the grid in relation to current object, and calls on the function
            # CellNeighbours to place them in the grid representation
            Neighbours = GetNeighbours(Current, Row, Column)
            NeighboursTree, NeighbourWater, NeighbourEmpty = CellNeighbours(Current, Neighbours)

            # If it is a Tree, we update its state out from the rule function in line:
            if Current[Row, Column]['Type'] == "Tree":
                Current = RulesForTrees(Current, Row, Column, NeighbourWater, NeighboursTree, NeighbourEmpty)

            # If it is a Water Source:
            elif Current[Row, Column]['Type'] == "WaterSource":
                Current = RulesForWater(Current, Row, Column, NeighbourWater, NeighbourEmpty)

    return Current


# Function which draws the grid representation as a array and on our screen:
def DrawGrid(Surface, Current, Size):
    # For loop there checks is the cell is Empty or not and color after this:
    for Row, Column in np.ndindex(Current.shape):
        Color = ColorEmpty

        if Current[Row, Column]['Type'] != 'Empty':
            Color = Current[Row, Column]['Color']

        # Draw our representation:
        pygame.draw.rect(Surface, Color, (Column * Size, Row * Size, Size - 1, Size - 1))


# Make our main there initializes the frame and the screen representation:
def main(DimensionX, DimensionY, CellSize, Tree, WaterSource):
    pygame.init()
    Surface = pygame.display.set_mode((DimensionX * CellSize, DimensionY * CellSize))
    pygame.display.set_caption("Tree World")

    Cells = init(DimensionX, DimensionY, Tree, WaterSource)

    # We create a clock, to make sure, that the given framerate earlier is consistent, so that it does change back
    # and furth in the program.
    Clock = pygame.time.Clock()
    SpeedCounter = 0

    # While loop there checks for events connected to the user, as the program runs
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:  # Press "q" to quit game
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

        Surface.fill(ColorGrid)

        # From our clock, we update the Cells, and update our visual representation (the shown grid).
        # The function makes sure, that we dont have any "rest (kommatal når vi dividere)" time.
        if SpeedCounter % Speed == 0:
            Cells = update_status(Surface, Cells, CellSize)

        DrawGrid(Surface, Cells, CellSize)
        pygame.display.update()

        Clock.tick(FramesPerSec)
        SpeedCounter = SpeedCounter + 1


# Recursively calls the main with some initialization values for the screen representation
if __name__ == "__main__":
    Tree = 6
    WaterSource = 12
    main(40, 10, 16, Tree, WaterSource)
