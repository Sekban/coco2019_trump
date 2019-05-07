import re 
import csv
import tweepy
from datetime import datetime
from textblob import TextBlob

OUTFILE = "trump_cleaned_tweets.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['timestamp', 'day', 'week', 'tweet', 'sentiment']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

cleanedTweets = []
with open('trump_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    '''
    Cleaning retweets
    '''
    startDate = datetime.strptime('04-28-2013 00:00:00', "%m-%d-%Y %H:%M:%S")
    for row in readCSV:
        'filtering out retweets'
        if row[4] == 'true': 
            continue
        

        cleanedRow = {}

        cleanedRow['timestamp'] = row[2]
        tweetDate = datetime.strptime(row[2], "%m-%d-%Y %H:%M:%S")
        delta = tweetDate - startDate
        cleanedRow['day'] = delta.days
        cleanedRow['week'] = int(delta.days / 7)
        'Cleaning Tweet'
        cleanedRow['tweet'] = ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row[1]).split())
        
        'Sentiment Analysis on cleaned tweet'
        analysis = TextBlob(cleanedRow['tweet'])
        cleanedRow['sentiment'] = analysis.sentiment.polarity

        cleanedTweets.append(cleanedRow)
    dict_writer.writerows(cleanedTweets)