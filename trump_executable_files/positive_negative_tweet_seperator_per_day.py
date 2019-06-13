import re
import csv
from datetime import datetime
import numpy as np
import pandas as pd

"Our timeframe of 6 years consist of 2192 days. We're initialising two lists of length 2192, and data type int"
PositiveSentimentPerDay = np.zeros(2192, dtype=int)
NegativeSentimentPerDay = np.zeros(2192, dtype=int)

with open('trump_executable_outputs/trump_cleaned_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    counter = 0
    for row in readCSV:
        '''
        dayIndex and sentiment are fetched from trump_cleaned_tweets.csv
        dayIndex has a -9 next to it due to the fact that the startTime in trumpInitialiser.py was initialised to 04-28-2013, instead of 05-07-2013. 
        This mishap doesn't affect the coding anywhere else
        '''
        dayIndex = int(row[2]) - 9 
        sentiment = float(row[5])
        '''
        If the fetched sentiment is > 0, the corresponding day index's positive sentiment value is incremented by 1
        If the fetched sentiment is < 0, the corresponding day index's negative sentiment value is decremented by 1
        '''
        
        if sentiment > 0:
            PositiveSentimentPerDay[dayIndex] += 1
        if sentiment < 0:
            NegativeSentimentPerDay[dayIndex] -= 1

'The corresponding data structures are converted to lists'
PositiveSentimentPerDay = PositiveSentimentPerDay.tolist()
NegativeSentimentPerDay = NegativeSentimentPerDay.tolist()
"Initialisation of output files' names"
outFileForPositiveTweets = "trump_positive_tweets_daily.csv"
outFileForNegativeTweets= "trump_negative_tweets_daily.csv"
'The files are opened with the write permission'
output_file_for_positive_tweets = open(outFileForPositiveTweets, 'w', newline='')
output_file_for_negative_tweets = open(outFileForNegativeTweets, 'w', newline='')

"Python's pandas library is used to convert the list into a tabular data structure with the only column being assigned to 'positive_tweet_count_per_day'"
df = pd.DataFrame(PositiveSentimentPerDay, columns=["positive_tweet_count_per_day"])
"The resulting dst is written to the output file trump_positive_tweets_daily.csv"
df.to_csv(output_file_for_positive_tweets, index=True)
"Python's pandas library is used to convert the list into a tabular data structure with the only column being assigned to 'negative_tweet_count_per_day'"
df = pd.DataFrame(NegativeSentimentPerDay, columns=["negative_tweet_count_per_day"])
"The resulting dst is written to the output file trump_negative_tweets_daily.csv"
df.to_csv(output_file_for_negative_tweets, index=True)