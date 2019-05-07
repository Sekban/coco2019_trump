import re 
import csv
import tweepy
from textblob import TextBlob

OUTFILE = "trump_cleaned_tweets.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['createdAt', 'text', 'favourites', 'sentiment']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

cleanedTweets = []
with open('trump_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    '''
    Cleaning retweets
    '''
    for row in readCSV:
        'filtering out retweets'
        if row[4] == 'true': 
            continue
        

        cleanedRow = {}

        cleanedRow['createdAt'] = row[2]
        'Cleaning Tweet'
        cleanedRow['text'] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row[1]).split())
        cleanedRow['favourites'] = row[3]
        'Sentiment Analysis on cleaned tweet'
        analysis = TextBlob(cleanedRow['text'])
        if analysis.sentiment.polarity > 0:
            cleanedRow['sentiment'] = 'positive'
        elif analysis.sentiment.polarity == 0:
            cleanedRow['sentiment'] = 'neutral'
        else:
            cleanedRow['sentiment'] = 'negative'

        cleanedTweets.append(cleanedRow)
    dict_writer.writerows(cleanedTweets)