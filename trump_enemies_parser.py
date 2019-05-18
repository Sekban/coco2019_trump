import csv

OUTFILE = "trump_enemies.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['actor', 'frequency', 'negative','positive', 'rated']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

enemies = []

with open('trump_actors_rated.csv', encoding='utf8') as csvfile:
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
