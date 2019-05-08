import re
import csv
from datetime import datetime
import numpy as np
import pandas as pd

PositiveSentimentPerDay = np.zeros(2192, dtype=float)
NegativeSentimentPerDay = np.zeros(2192, dtype=float)

with open('trump_cleaned_tweets.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    counter = 0
    for row in readCSV:
        dayIndex = int(row[2]) - 9 # since the days column in trump_cleaned_tweets.csv started from 9
        sentiment = float(row[5])
        if sentiment > 0:
            PositiveSentimentPerDay[dayIndex] += sentiment
        if sentiment < 0:
            NegativeSentimentPerDay[dayIndex] += sentiment

PositiveSentimentPerDay = PositiveSentimentPerDay.tolist()
NegativeSentimentPerDay = NegativeSentimentPerDay.tolist()
outFileForPositiveTweets = "trump_positive_tweets_daily.csv"
outFileForNegativeTweets= "trump_negative_tweets_daily.csv"

output_file_for_positive_tweets = open(outFileForPositiveTweets, 'w', newline='')
output_file_for_negative_tweets = open(outFileForNegativeTweets, 'w', newline='')

df = pd.DataFrame(PositiveSentimentPerDay, columns=["aggregated_sentiment_per_day"])
df.to_csv(output_file_for_positive_tweets, index=True)

df = pd.DataFrame(NegativeSentimentPerDay, columns=["aggregated_sentiment_per_day"])
df.to_csv(output_file_for_negative_tweets, index=True)