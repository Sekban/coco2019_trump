import csv
import ast
import numpy as np

'The adjacency matrix is created, and initialised to 0s'
adjacencyList = np.zeros([24,24], dtype=np.int_)
enemyNames = []

'''
Aim of this file is to create a symmetric matrix representing which enemies have been mentioned with which other enemies in the same week.
The values beteen two enemies are updated based on the occurrence of this phenomenon.
'''
with open('trump_enemies.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    'enemyNames are stored in memory'
    for enemy in readCSV:
        enemyNames.append(enemy[0])
    'For each enemy, we are traversing through trump_actors_weekly.csv file'
    for enemyName in enemyNames:
        with open('trump_actors_weekly.csv', encoding='utf8') as actorsCSV:
            weeklyActorsCSV = csv.reader(actorsCSV, delimiter = ',')
            next(weeklyActorsCSV)
            for weeklyActors in weeklyActorsCSV:
                'String representation of the actors and their frequncies are evaluated back to a dictionary data structure'
                weeklyActorsList = ast.literal_eval(weeklyActors[1])
                weeklyActorNames = []
                'weeklyActorNames are stored in memory'
                for actor in weeklyActorsList:
                    weeklyActorNames.append(actor["name"])
                "We then check if the enemyName in trump_enemies.csv is in the specified week's weeklyActorNames"
                if enemyName in weeklyActorNames:
                    for storedEnemyName in enemyNames:
                        'If one of the enemies inside enemyNames fetched from trump_enemies.csv is the same as storedEnemyName we skip this iteration of the loop.'
                        if storedEnemyName == enemyName:
                            continue
                        "We then check if one of the enemies inside enemyNames is in the specified week's actor names. If so we update the matrix"
                        if storedEnemyName in weeklyActorNames:
                            adjacencyList[enemyNames.index(enemyName)][enemyNames.index(storedEnemyName)] += 1
    'Finally the matrix is printed'
    print(adjacencyList)