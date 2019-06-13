import csv

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_actors_rated.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['actor', 'frequency', 'negative','positive', 'rated']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

with open('trump_mentions.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for wordDict in readCSV:
        'We are skipping actors that have been mentioned less than 10 times, and the odd case where only "@" is used as a mention without specifying the address'
        if int(wordDict[1]) < 10 or wordDict[0] == "@":
            continue
        word = wordDict[0]
        'Desired data structure is created, and its fields are initialised'
        actor = {}
        actor["actor"] = word
        actor["frequency"] = wordDict[1]
        actor["negative"] = 0
        actor["positive"] = 0
        actor["rated"] = 0
        with open('trump_cleaned_tweets.csv', encoding='utf8') as tweetscsvfile:
            tweetCSV = csv.reader(tweetscsvfile, delimiter=',')
            next(tweetCSV)
            'cleaned tweets are looped through'
            for tweet in tweetCSV:
                if word in tweet[4]:
                    "We then fetch the polarity that we've previsouly calculated with trumpInitialiser.py "
                    polarity = float(tweet[5])
                    if polarity < 0:
                        """
                        If the tweet's sentiment is negative, we decrement the value present in the field. This is done to get a cumulative picture of Trump's feelings towards a specific actor.
                        If a specific actor has been mentioned in a negative context thrice, then he/she will get a negative rating of -3
                        If a specific actor has been mentioned in a positive context twice, then he/she will get a positive rating of +2
                        """
                        
                        actor["negative"] = int(actor["negative"]) - 1
                    elif polarity > 0:
                        actor["positive"] = int(actor["positive"]) + 1
            

        'We then calculate the net rating that our analysis assigns to an actor'
        actor["rated"] = int(actor["negative"]) + int(actor["positive"])
        print(actor)
        'Finally the findings are written onto trump_actors_rated.csv'
        dict_writer.writerow(actor)
