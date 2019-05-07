import re 
import csv
import tweepy
from datetime import datetime
from textblob import TextBlob
from collections import Counter

OUTFILE = "trump_cleaned_tweets.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['id', 'timestamp', 'day', 'week', 'tweet', 'sentiment']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

cleanedTweets = []
with open('trump_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    '''
    Cleaning retweets
    '''
    startDate = datetime.strptime('04-28-2013 00:00:00', "%m-%d-%Y %H:%M:%S")
    counter = 0
    for row in readCSV:
        'filtering out retweets'
        if row[3] == 'true': 
            continue

        cleanedRow = {}
        cleanedRow['id'] = row[4]
        cleanedRow['timestamp'] = row[2]
        tweetDate = datetime.strptime(row[2], "%m-%d-%Y %H:%M:%S")
        delta = tweetDate - startDate
        cleanedRow['day'] = delta.days
        cleanedRow['week'] = int(delta.days / 7)
        'Cleaning Tweet'
        cleanedRow['tweet'] = ' '.join(re.sub("([^@0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row[1]).split())
        
        'Sentiment Analysis on cleaned tweet'
        analysis = TextBlob(cleanedRow['tweet'])
        cleanedRow['sentiment'] = analysis.sentiment.polarity

        cleanedTweets.append(cleanedRow)
    dict_writer.writerows(cleanedTweets)

OUTFILEWORDS = "trump_words.csv" 
OUTFILEMENTIONS = "trump_mentions.csv"
output_file = open(OUTFILEWORDS, 'w', newline='')
keys = ['word', 'frequency']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

allWords = []
wordsByFreq = []
wordsByFreqCsv = []

mentions = []
mentionsByFreq = []
mentionsByFreqCsv = []

with open('trump_cleaned_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
        csvWords = row[4].split(" ")
        for i in csvWords:
            if (i.startswith("@")):
                mentions.append(i)
            else:
                allWords.append(i.lower())

    wordsByFreq = Counter(allWords)
    for key, value in wordsByFreq.items():
        wordByFreq = {}
        wordByFreq['word'] = key
        wordByFreq['frequency'] = value
        wordsByFreqCsv.append(wordByFreq)
    
    dict_writer.writerows(wordsByFreqCsv)

    mentionsByFreq = Counter(mentions)
    for key, value in mentionsByFreq.items():
        mentionWordByFreq = {}
        mentionWordByFreq['word'] = key
        mentionWordByFreq['frequency'] = value
        mentionsByFreqCsv.append(mentionWordByFreq)

    output_file = open(OUTFILEMENTIONS, 'w', newline='')
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    
    dict_writer.writerows(mentionsByFreqCsv)
