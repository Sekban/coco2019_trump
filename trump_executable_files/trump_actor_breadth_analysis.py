import csv
import copy
import numpy as np

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_actors_weekly.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ["week", "actors", "cumulative"]
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

actorsWeekly = []

'Initialising the list with empty desired objects.'
for x in range(1,315):
    actorsWeekly.append({
        "week": x,
        "actors": [],
        "cumulative": 0
    })


'''
trump_actors_rated.csv includes the name of the actor, how frequently the actor has been mentioned, how many times he/she's been mentioned in positive/negative contexts, and the net ratings
'''
with open('trump_actors_rated.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    counter = 0
    for actorRated in readCSV:
        "Actor's name is stored in a variable"
        actorName = actorRated[0]

        actor = {}
        actor["name"] = actorName
        actor["frequency"] = 1
        print(actorName)
        print(counter)
        counter+=1
        '''
        We're looping through every actor, and then checking if they're mentioned in each tweet.
        If so, the actor is appended to the actors list
        If the same actor is encountered again, its frequency is incremented by 1
        '''
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
"Finally we're calculating the cumulative frequency of actors in a single week"
for x in range(0, len(actorsWeekly)):
    act = actorsWeekly[x]["actors"]
    freq = 0
    for y in range(0, len(act)):
        freq = int(act[y]["frequency"]) + freq
    actorsWeekly[x]["cumulative"] = freq

dict_writer.writerows(actorsWeekly)