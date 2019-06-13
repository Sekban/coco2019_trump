import re 
import csv
from datetime import datetime
from textblob import TextBlob
from collections import Counter

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_cleaned_tweets.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['id', 'timestamp', 'day', 'week', 'tweet', 'sentiment']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

'''
trump_tweets.csv is the raw data we've fetched from http://trumptwitterarchive.com/archive
'''
cleanedTweets = []
with open('trump_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    'The following line skips the row that includes the headers'
    next(readCSV)
    
    'startDate corresponding to our cutoff point in Trumps tweets. This variable allows us to calculate the number of days, weeks that have passed since the creation of the tweet'
    startDate = datetime.strptime('04-28-2013 00:00:00', "%m-%d-%Y %H:%M:%S")
    
    for row in readCSV:
        'filtering out retweets as they are not in scope of our project'
        if row[3] == 'true': 
            continue
        'Mapping the required fields from raw data to our own data format'
        cleanedRow = {}
        cleanedRow['id'] = row[4]
        cleanedRow['timestamp'] = row[2]
        'Parsing of Twitter Datetime format'
        tweetDate = datetime.strptime(row[2], "%m-%d-%Y %H:%M:%S")
        delta = tweetDate - startDate
        cleanedRow['day'] = delta.days
        cleanedRow['week'] = int(delta.days / 7)
        '''
        We've cleaned out the tweet texts by removing symbols such as commas, full stops, quotation marks. 
        This allowed the sentiment analysis to be easier to calculate, only focusing on nouns, verbs, adjectives, and adverbs.
        '''
        cleanedRow['tweet'] = ' '.join(re.sub("([^@0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row[1]).split())
        
        'Sentiment Analysis on cleaned tweet, which returns values in the range of -1,1'
        analysis = TextBlob(cleanedRow['tweet'])
        cleanedRow['sentiment'] = analysis.sentiment.polarity

        cleanedTweets.append(cleanedRow)
    'cleanedTweets are then written onto trump_cleaned_tweets.csv'
    dict_writer.writerows(cleanedTweets)

'''
Preparation of the output files trump_words and trump_mentions, both having the same headers
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
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
        'Fetching words from the cleaned tweets separated by whitespace'
        csvWords = row[4].split(" ")
        for i in csvWords:
            if (i.startswith("@")):
                'Twitter mention usage entails including the "@" symbol in front of the referred account. This allows us to identify mentions'
                mentions.append(i)
            else:
                'Words that are not mentions are appended to allWords dst. Bear in mind this list has duplicates, which will allow us to find their usage frequency'
                allWords.append(i.lower())
    'Imported Counter library is used to find out the frequency of unique items in a list'
    'Words'
    wordsByFreq = Counter(allWords)
    for key, value in wordsByFreq.items():
        wordByFreq = {}
        wordByFreq['word'] = key
        wordByFreq['frequency'] = value
        wordsByFreqCsv.append(wordByFreq)
    'Words and their frequencies are written onto trump_words.csv'
    dict_writer.writerows(wordsByFreqCsv)
    'Mentions'
    mentionsByFreq = Counter(mentions)
    for key, value in mentionsByFreq.items():
        mentionWordByFreq = {}
        mentionWordByFreq['word'] = key
        mentionWordByFreq['frequency'] = value
        mentionsByFreqCsv.append(mentionWordByFreq)

    output_file = open(OUTFILEMENTIONS, 'w', newline='')
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    'Mentions and their frequencies are written onto trump_mentions.csv'
    dict_writer.writerows(mentionsByFreqCsv)
