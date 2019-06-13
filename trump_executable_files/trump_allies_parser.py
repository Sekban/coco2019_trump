import csv

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_allies.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['actor', 'frequency', 'negative','positive', 'rated']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

allies = []

'''
This parser simply fetches the rows from trump_actors_rated.csv and depending on the net rating we've calculated within trump_actors_parser.py, appends a desired data structure to a list of allies.
'''
with open('trump_actors_rated.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for actor in readCSV:
        ally = {}
        if int(actor[4]) >= 0:
            ally["actor"] = actor[0]
            ally["frequency"] = actor[1]
            ally["negative"] = actor[2]
            ally["positive"] = actor[3]
            ally["rated"] = actor[4]
            allies.append(ally)
        
dict_writer.writerows(allies)
