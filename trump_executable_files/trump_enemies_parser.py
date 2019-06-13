import csv

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_enemies.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['actor', 'frequency', 'negative','positive', 'rated']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

enemies = []

'''
This parser simply fetches the rows from trump_actors_rated.csv and depending on the net rating we've calculated within trump_actors_parser.py, appends a desired data structure to a list of allies.
'''
with open('trump_executable_outputs/trump_actors_rated.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for actor in readCSV:
        enemy = {}
        if int(actor[4]) < 0:
            enemy["actor"] = actor[0]
            enemy["frequency"] = actor[1]
            enemy["negative"] = actor[2]
            enemy["positive"] = actor[3]
            enemy["rated"] = actor[4]
            enemies.append(enemy)
        
dict_writer.writerows(enemies)
