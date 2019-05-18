import nltk
import csv
from nltk.corpus import brown

OUTFILE = "trump_adjectives.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['word', 'frequency', 'polarity']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

nltk.download('brown')
brownTaggedWords = brown.tagged_words()

adjectives = []
with open('trump_words.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
        table = nltk.FreqDist(t for w, t in brownTaggedWords if w.lower() == row[0])
        
        mostCommonClasses = table.most_common()
        if not mostCommonClasses:
            continue
        
        adjEntry = {}
        if mostCommonClasses[0][0].startswith('JJ'):
            print(row[0])
            adjEntry['word'] = row[0]
            adjEntry['frequency'] = 0
            adjEntry['polarity'] = mostCommonClasses[0][0]
            
            dict_writer.writerow(adjEntry)