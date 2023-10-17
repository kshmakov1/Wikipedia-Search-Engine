import gzip
import json
from unittest.util import sorted_list_difference
from bs4 import BeautifulSoup
from helper_module import stringCleaner
from string import punctuation
from helper_module import openStopWordsFile
from helper_module import stemWord, writeJSONToFile, stringCleaner2, dictClearer
import psutil
import gc
import os

process = psutil.Process(os.getpid())

# Get user input if they want to enable/disable stop word removal and stemming
stopWordRemoval = False
wordStemming = False

while True:
    userInputStopWord = input(
        'Would you like to enable stop word removal? (yes/no):\t')
    if userInputStopWord.lower() in ['yes', 'y']:
        stopWordRemoval = True
        break
    elif userInputStopWord.lower() in ['no', 'n']:
        break
    else:
        userInputStopWord = input(
            'Would you like to enable stop word removal? (yes/no):\t')

while True:
    userInputStemming = input(
        'Would you like to enable stemming? (yes/no):\t')
    if userInputStemming.lower() in ['yes', 'y']:
        wordStemming = True
        break
    elif userInputStemming.lower() in ['no', 'n']:
        break
    else:
        userInputStemming = input(
            'Would you like to enable stemming? (yes/no):\t')

stopWordsDict = openStopWordsFile('stopwords.txt')

with gzip.open('../data/trec_corpus_5000.jsonl.gz', 'r') as file:
    tokenDict = {}
    postingsDict = {}
    max_ram_percentage = 45.0  # Max ram % allowed
    fileCounter = 0
    recordsCounter = 0  # TODO: Remove this later!!!

    for line in file:  # Read the files line by line

        ram_percentage = psutil.virtual_memory()[2]
        percentage_available = psutil.virtual_memory().available * 100 / \
            psutil.virtual_memory().total
        currPythonProcessRamUsage = process.memory_info().rss / (1024 ** 3)
        print('curr percentage: ', ram_percentage)
        print('available percentage:', percentage_available)
        print('curr python process', currPythonProcessRamUsage)
        if (currPythonProcessRamUsage >= 0.5):

            print('Sorting and saving to file')
            sortedDict = dict(sorted(tokenDict.items()))
            # for key in sortedDict.keys():
            #     sortedDict[key] = sorted(sortedDict[key].items())
            sortedPostings = dict(sorted(postingsDict.items()))
            # for key in sortedPostings.keys():
            #     sortedPostings[key] = sorted(sortedPostings[key].items())

            for k in sortedPostings:
                sortedPostings[k] = {key: value for key, value in sorted(
                    sortedPostings[k].items(), key=lambda item: int(item[0]))}

            dictFileName = "dictionary" + str(fileCounter) + ".json"
            postingFileName = "postings" + str(fileCounter) + ".json"
            writeJSONToFile('../output/blocks', dictFileName, sortedDict)
            writeJSONToFile('../output/blocks',
                            postingFileName, sortedPostings)
            # dictClearer([sortedDict, sortedPostings, tokenDict, postingsDict])
            # sortedDict.clear()
            sortedDict = {}
            sortedPostings = {}
            tokenDict = {}
            postingsDict = {}
            gc.collect()
            # sortedPostings.clear()
            # tokenDict.clear()
            # postingsDict.clear()
            print('Ram info after clear:', psutil.virtual_memory())
            fileCounter += 1

        tempObj = json.loads(line)  # Load the data

        # Use BS4 to parse HTML
        soup = BeautifulSoup(tempObj['contents'], 'html.parser')
        # tempObj['parsed_contents'] = soup.get_text(separator=' ')

        # tokens = stringCleaner(soup.get_text(separator=' '))

        tokens = stringCleaner2(soup.get_text(separator=' '))

        # testing
        # tokens = re.sub(r"[^A-Za-z0-9\s]+", "", str(soup.get_text(separator=' '))).lower().split()

        # blackList = ".,:;()[]\"\'"
        document_id = tempObj['id']
        currentDocDict = {}
        pos = 0

        for token in tokens:

            # Skip the token if it exists in the stop word list
            if stopWordRemoval:
                if token in stopWordsDict:
                    pos += 1
                    continue

            if wordStemming:
                # stemming
                token = stemWord(token)

            # if token not in tokenDict:
            #     tokenDict[token] = 1
            # else:
            #     tokenDict[token] += 1

            # if token not in tokenDict:
            #     tokenDict[token] = 1
            #     currentDocDict[token] = [document_id]
            # else:
            #     if document_id not in currentDocDict[token]:
            #         tokenDict[token] += 1
            #         currentDocDict[token].append(document_id)

            if token not in currentDocDict:
                currentDocDict[token] = 1

                if token in tokenDict:
                    tokenDict[token] += 1
                else:
                    tokenDict[token] = 1

            else:
                currentDocDict[token] += 1

            if token in postingsDict:
                # check if this is first occurence of this term in this document
                if document_id in postingsDict[token]:
                    # if yes
                    postingsDict[token][document_id]['tf'] += 1
                    postingsDict[token][document_id]['pos'].append(pos)

                else:
                    # if not first occurency
                    postingsDict[token][document_id] = {}
                    postingsDict[token][document_id]['tf'] = 1
                    postingsDict[token][document_id]['pos'] = [pos]

            else:
                postingsDict[token] = {}
                postingsDict[token][document_id] = {}
                postingsDict[token][document_id]['tf'] = 1
                postingsDict[token][document_id]['pos'] = [pos]

            pos += 1

        recordsCounter += 1  # TODO: Remove this later!!!
        print(recordsCounter)

        # print(sortedPostings)

        # with open("../output/dictionary.json", "w") as write_file:
        #     write_file.write(json.dumps(sortedDict))
        #     write_file.close()

        # writeJSONToFile("../output", "dictionary.json", sortedDict)

    # with open("../output/postings.json", "w") as write_file:
    #     write_file.write(json.dumps(sortedPostings))
    #     write_file.close()

    # with open("../output/parsedText.txt", "a") as write_file:
    #     write_file.write(str(tempObj['id']))
    #     write_file.write(str(soup.get_text(separator=' ')))
    #     write_file.close()

        # with open("../output/parsedTextNoPunc.txt", "a") as write_file:
        #     write_file.write(re.sub(r"[^A-Za-z0-9\s]+", " ", str(soup.get_text(separator=' '))))
        #     write_file.close()

        # with open("../output/sample.html", "w") as write_file:
        #     write_file.write(tempObj['contents'])
        #     write_file.close()

        # exit()

        # for i in tempObj['parsed_contents'].split(' '):
        #     print(i)

        # input()

    print('Sorting and saving to file')
    sortedDict = dict(sorted(tokenDict.items()))
    # for key in sortedDict.keys():
    #     sortedDict[key] = sorted(sortedDict[key].items())
    sortedPostings = dict(sorted(postingsDict.items()))
    # for key in sortedPostings.keys():
    #     sortedPostings[key] = sorted(sortedPostings[key].items())

    for k in sortedPostings:
        sortedPostings[k] = {key: value for key, value in sorted(
            sortedPostings[k].items(), key=lambda item: int(item[0]))}

    dictFileName = "dictionary" + str(fileCounter) + ".json"
    postingFileName = "postings" + str(fileCounter) + ".json"
    writeJSONToFile('../output/blocks', dictFileName, sortedDict)
    writeJSONToFile('../output/blocks',
                    postingFileName, sortedPostings)
