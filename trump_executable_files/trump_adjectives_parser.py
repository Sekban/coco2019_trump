import nltk
import csv
from nltk.corpus import brown

'''
Preparation of the output file
Csv's headers are declared, and Python's csv library is asked to create a dictionary writer object
Subsequently, the declared headers are written into the file
'''
OUTFILE = "trump_adjectives.csv" 
output_file = open(OUTFILE, 'w', newline='')
keys = ['word', 'frequency', 'polarity']
dict_writer = csv.DictWriter(output_file, keys)
dict_writer.writeheader()

'''
Natural Language Toolkit is used to download Brown Corpus, first created in 1961 at Brown University. 
We are then fetching Brown's tagged words without specifying a category, such as news. 
'''
nltk.download('brown')
brownTaggedWords = brown.tagged_words()

adjectives = []
with open('trump_executable_outputs/trump_words.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)
    for row in readCSV:
        '''
        We are then giving each word to nltk's frequency distribution method and trying to find the most common usage of the words. We are only interested in whether the used word is an adjective or not.
        The line below returns us a table where the usage of the word is assigned several tags such as JJ(adjective)
        '''
        table = nltk.FreqDist(t for w, t in brownTaggedWords if w.lower() == row[0])
        'We are only interested in the highest rated meaning'
        mostCommonClasses = table.most_common()
        if not mostCommonClasses:
            continue
        
        adjEntry = {}
        'if the most common tag is JJ-corresponding to an adjective we create our data structure accordingly.'
        if mostCommonClasses[0][0].startswith('JJ'):
            print(row[0])
            adjEntry['word'] = row[0]
            adjEntry['frequency'] = 0
            adjEntry['polarity'] = mostCommonClasses[0][0]
            
            dict_writer.writerow(adjEntry)