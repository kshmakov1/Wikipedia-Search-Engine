import json
import time
from unittest import result
from helper_module import retrieveResults
from helper_module import resultDocSummary

# Read Dictionary
dictFile = open('../output/dictionary.json')
dictionaryData = json.load(dictFile)

# Read Postings
postingsFile = open('../output/postings.json')
postingsData = json.load(postingsFile)

# Logs time after each run
timeLog = []

userInput = input('Enter search term:\t')
while (userInput != 'ZZEND'):
    startTime = time.time()
    resultIdentifiers = []

    # TODO: Preprocess user's query before continuing

    if userInput in dictionaryData:
        # Retrieve data from Dictionary
        docFreq = dictionaryData[userInput]

        print(
            f'\nFound {docFreq} document(s) that contains the term \"{userInput}\"\n')

        # Retrieve data from postings
        postingEntries = postingsData[userInput]
        for docID in postingEntries:
            tokenFreq = postingEntries[docID]['tf']
            positions = postingEntries[docID]['pos']

            # Store the location of the doc in the colleciton
            resultIdentifiers.append([docID, positions, tokenFreq])

        res = retrieveResults(
            '../data/trec_corpus_5000.jsonl.gz', resultIdentifiers)

        for (id, title, freq, context, resultPos) in res:
            resultDocSummary(id, title, freq, context, resultPos)
        # Retrieve the result from docs

        endTime = time.time()
        elapsedTime = endTime-startTime
        timeLog.append(elapsedTime)
        print(f'\nIt took {elapsedTime} seconds to retrieve the results')

    else:
        print(
            f'\nFound 0 document that contains the term \"{userInput}\"\n')

    userInput = input('Enter search term:\t')


print(
    f'\nIt takes {sum(timeLog)/len(timeLog)} seconds on average to retrieve the results of a query')
# TODO: Input check
# TODO: Input normalization
# TODO: token freq is wrong. Supposed to be freq within doc
