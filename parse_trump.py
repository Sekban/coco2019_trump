import re 
import tweepy
import csv
from tweepy import tweepy 
from textblob import TextBlob

class TrumpTweetParser(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements.
        '''
        cleanedRow = {}
        cleanedRow.text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet[1]).split())
        cleanedRow.createdAt = tweet[2]
        cleanedRow.favorites = tweet[3]
        return cleanedRow

        
        #return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self):
        cleanedTweets = []
        parsedTweets = []
        with open('trump_tweets.csv', encoding='utf8') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            '''
            Cleaning retweets
            '''
            for row in readCSV:
                # filtering out retweets
                if row[4] == 'true': 
                    continue
                cleanedTweets.append(self.clean_tweet(row))
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        try: 
            # parsing tweets one by one 
            for tweet in cleanedTweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {}

                # saving text of tweet 
                parsed_tweet['text'] = cleanedTweets.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                parsedTweets.append(parsed_tweet)
              
            # return parsed tweets 
            return parsedTweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

def main(): 
    # creating object of TwitterClient Class 
    trumpTweetParser = TrumpTweetParser()
    # calling function to get tweets 
    tweets = trumpTweetParser.get_tweets() 

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} % \ ".format(100*len(tweets - ntweets - ptweets)/len(tweets))) 

    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 

if __name__ == "__main__": 
    # calling main function 
    main() 
