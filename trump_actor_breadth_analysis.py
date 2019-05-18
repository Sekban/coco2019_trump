import csv
import copy
import numpy as np

OUTFILE = "trump_actors_weekly.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ["week", "actors", "cumulative"]
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

actorsWeekly = []

for x in range(1,315):
    actorsWeekly.append({
        "week": x,
        "actors": [],
        "cumulative": 0
    })



with open('trump_actors_rated.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    counter = 0
    for actorRated in readCSV:
        actorName = actorRated[0]

        actor = {}
        actor["name"] = actorName
        actor["frequency"] = 1
        print(actorName)
        print(counter)
        counter+=1

        with open('trump_cleaned_tweets.csv', encoding='utf8') as tweetscsvfile:
            tweetCSV = csv.reader(tweetscsvfile, delimiter=',')
            next(tweetCSV)
            for tweet in tweetCSV:
                if actorName in tweet[4]:
                    weekIndex = int(tweet[3]) - 1
                    relevantActors = actorsWeekly[weekIndex]["actors"]

                    if not relevantActors:
                        actorsWeekly[weekIndex]["actors"].append(copy.deepcopy(actor))
                    else:
                        found = 0
                        for x in range(0, len(relevantActors)):
                            relevantActor = relevantActors[x]
                            if actorName == relevantActor["name"]:
                                relevantActors[x]["frequency"] = int(relevantActors[x]["frequency"]) + 1
                                found = 1
                        
                        if found == 0:
                            actorsWeekly[weekIndex]["actors"].append(copy.deepcopy(actor))

for x in range(0, len(actorsWeekly)):
    act = actorsWeekly[x]["actors"]
    freq = 0
    for y in range(0, len(act)):
        freq = int(act[y]["frequency"]) + freq
    actorsWeekly[x]["cumulative"] = freq

dict_writer.writerows(actorsWeekly)