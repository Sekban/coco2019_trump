import csv
import ast
import numpy as np

adjacencyList = np.zeros([24,24], dtype=np.int_)
enemyNames = []

with open('trump_enemies.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for enemy in readCSV:
        enemyNames.append(enemy[0])

    for enemyName in enemyNames:
        with open('trump_actors_weekly.csv', encoding='utf8') as actorsCSV:
            weeklyActorsCSV = csv.reader(actorsCSV, delimiter = ',')
            next(weeklyActorsCSV)
            for weeklyActors in weeklyActorsCSV:
                weeklyActorsList = ast.literal_eval(weeklyActors[1])
                weeklyActorNames = []
                for actor in weeklyActorsList:
                    weeklyActorNames.append(actor["name"])
                if enemyName in weeklyActorNames:
                    for storedEnemyName in enemyNames:
                        if storedEnemyName == enemyName:
                            continue
                        if storedEnemyName in weeklyActorNames:
                            adjacencyList[enemyNames.index(enemyName)][enemyNames.index(storedEnemyName)] += 1

    print(adjacencyList)