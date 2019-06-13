import csv
import copy
import ast

'''
Preparation of the output files trump_allies_weekly.csv and trump_enemies_weekly.csv
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
allies_OUTFILE = "trump_allies_weekly.csv" 
enemies_OUTFILE = "trump_enemies_weekly.csv"
allies_output_file = open(allies_OUTFILE, 'w', newline='')
enemies_output_file = open(enemies_OUTFILE, 'w', newline='')
keys = ["week", "actors", "cumulative"]
allies_dict_writer = csv.DictWriter(allies_output_file, keys)
enemies_dict_writer = csv.DictWriter(enemies_output_file, keys)
allies_dict_writer.writeheader()
enemies_dict_writer.writeheader()

enemyNames = []
allyNames = []

'Trump enemy names are fetched and stored in a list'
with open('trump_enemies.csv', encoding='utf8') as enemyCsvfile:
    enemyReadCSV = csv.reader(enemyCsvfile, delimiter=',')
    next(enemyReadCSV)
    for enemy in enemyReadCSV:
        enemyNames.append(enemy[0])
'Trump ally names are fetched and stored in a list'
with open('trump_allies.csv', encoding='utf8') as allyCsvfile:
    allyReadCSV = csv.reader(allyCsvfile, delimiter=',')
    next(allyReadCSV)
    for ally in allyReadCSV:
        allyNames.append(ally[0])

'Helper Functions'
'Intersection(lst1, lst2) returns the entries where the "name" field of the weeklyActors object is in stored enemyNames or allyNames'
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value["name"] in lst2] 
    return lst3
'Cumulative(lst1) returns the cumulative frequency values of allies/enemies mentioned in a week'
def cumulative(lst1):
    for x in range(0, len(lst1)):
        act = lst1[x]["actors"]
        freq = 0
        lst1[x]["cumulative"] = freq
        for y in range(0, len(act)):
            freq = int(act[y]["frequency"]) + freq
        lst1[x]["cumulative"] = freq
'End of helper functions'

alliesWeekly = []
enemiesWeekly = []

'Aim of this file is to separate the allies and enemies inside trump_actors_weekly.csv'
with open('trump_actors_weekly.csv', encoding='utf8') as actorsCSV:
            weeklyActorsCSV = csv.reader(actorsCSV, delimiter = ',')
            next(weeklyActorsCSV)
            for weeklyActors in weeklyActorsCSV:
                weeklyActorsList = ast.literal_eval(weeklyActors[1])
                oldWeeklyActors = copy.deepcopy(weeklyActors)
                'Allies'
                alliesWeeklyActorsList = intersection(weeklyActorsList, allyNames)
                oldWeeklyActors[1] = alliesWeeklyActorsList
                allyWeeklyObject = {
                    "week": oldWeeklyActors[0],
                    "actors": oldWeeklyActors[1],
                    "cumulative": oldWeeklyActors[2]
                }
                alliesWeekly.append(allyWeeklyObject)
                'End of Allies'

                'Enemies'
                enemiesWeeklyActorsList = intersection(weeklyActorsList, enemyNames)
                oldWeeklyActors[1] = enemiesWeeklyActorsList
                enemyWeeklyObject = {
                    "week": oldWeeklyActors[0],
                    "actors": oldWeeklyActors[1],
                    "cumulative": oldWeeklyActors[2]
                }
                enemiesWeekly.append(enemyWeeklyObject)
                'end of Enemies'
                

cumulative(alliesWeekly)
cumulative(enemiesWeekly)

'Finally alliesWeekly and enemiesWeekly are written to trump_allies_weekly.csv and trump_enemies_weekly.csv files respectively'
allies_dict_writer.writerows(alliesWeekly)
enemies_dict_writer.writerows(enemiesWeekly)