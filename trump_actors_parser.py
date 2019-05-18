import csv

OUTFILE = "trump_actors_rated.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['actor', 'frequency', 'negative','positive', 'rated']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

with open('trump_mentions.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for wordDict in readCSV:
        if int(wordDict[1]) < 10:
            continue
        word = wordDict[0]
        actor = {}
        actor["actor"] = word
        actor["frequency"] = wordDict[1]
        actor["negative"] = 0
        actor["positive"] = 0
        actor["rated"] = 0
        with open('trump_cleaned_tweets.csv', encoding='utf8') as tweetscsvfile:
            tweetCSV = csv.reader(tweetscsvfile, delimiter=',')
            next(tweetCSV)
            for tweet in tweetCSV:
                if word in tweet[4]:
                    polarity = float(tweet[5])
                    if polarity < 0:
                        actor["negative"] = int(actor["negative"]) - 1
                    elif polarity > 0:
                        actor["positive"] = int(actor["positive"]) + 1
            

            
        actor["rated"] = int(actor["negative"]) + int(actor["positive"])
        print(actor)
        dict_writer.writerow(actor)
