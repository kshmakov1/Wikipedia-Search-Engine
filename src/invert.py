from asyncore import write
import gzip
import json
from bs4 import BeautifulSoup
from numpy import record
from helper_module import stringCleaner
from string import punctuation
from helper_module import openStopWordsFile
from helper_module import stemWord
from helper_module import stringCleaner2

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

    recordsCounter = 0  # TODO: Remove this later!!!

    textAcc = ''
    textAcc2 = ''

    for line in file:  # Read the files line by line
        tempObj = json.loads(line)  # Load the data

        # Use BS4 to parse HTML
        soup = BeautifulSoup(tempObj['contents'], 'html.parser')
        #tempObj['parsed_contents'] = soup.get_text(separator=' ')
        textAcc += soup.get_text(separator=' ') + "="*50 + "\n"
        # textAcc2 += stringCleaner2(soup.get_text(separator=' ')
        #                            ) + "="*50 + "\n"
        #tokens = stringCleaner(soup.get_text(separator=' '))
        tokens = stringCleaner2(soup.get_text(separator=' '))
        # testing
        #tokens = re.sub(r"[^A-Za-z0-9\s]+", "", str(soup.get_text(separator=' '))).lower().split()

        #blackList = ".,:;()[]\"\'"
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
                    postingsDict[token][document_id]['token_frequency'] += 1
                    postingsDict[token][document_id]['position'].append(pos)

                else:
                    # if not first occurency
                    postingsDict[token][document_id] = {}
                    postingsDict[token][document_id]['token_frequency'] = 1
                    postingsDict[token][document_id]['position'] = [pos]

            else:
                postingsDict[token] = {}
                postingsDict[token][document_id] = {}
                postingsDict[token][document_id]['token_frequency'] = 1
                postingsDict[token][document_id]['position'] = [pos]

            pos += 1

        recordsCounter += 1  # TODO: Remove this later!!!
        print(recordsCounter)
        if recordsCounter == 20:
            exit()

        with open("../output/parsedTextPreTok.txt", "w") as write_file:
            write_file.write(str(tempObj['id']))
            #write_file.write(str(soup.get_text(separator=' ')))
            write_file.write(textAcc)
            write_file.close()

        with open("../output/parsedTextTok.txt", "w") as write_file:
            write_file.write(str(tempObj['id']))
            #write_file.write(str(soup.get_text(separator=' ')))
            write_file.write(textAcc2)
            write_file.close()

        print('Sorting and saving to file')
        sortedDict = dict(sorted(tokenDict.items()))
        # print(sortedDict)

        sortedPostings = dict(sorted(postingsDict.items()))
        # print(sortedPostings)

        with open("../output/dictionary.json", "w") as write_file:
            write_file.write(json.dumps(sortedDict))
            write_file.close()

        with open("../output/postings.json", "w") as write_file:
            write_file.write(json.dumps(sortedPostings))
            write_file.close()

        # input()

    # with open("../output/parsedTextNoPunc.txt", "a") as write_file:
    #     write_file.write(re.sub(r"[^A-Za-z0-9\s]+", " ", str(soup.get_text(separator=' '))))
    #     write_file.close()

    # with open("../output/sample.html", "w") as write_file:
    #     write_file.write(tempObj['contents'])
    #     write_file.close()

    # exit()

    # for i in tempObj['parsed_contents'].split(' '):
    #     print(i)
