import re

from matplotlib.ticker import LinearLocator
from porter import PorterStemmer
import gzip
import json
from bs4 import BeautifulSoup
from string import punctuation

p = PorterStemmer()


def stringCleaner(line: str):

    # Ver 1
    # blacklistChar = ":;!`~@#$%^&*()[]\{\},?/.\'\""

    # #Remove possessive (apostrophe + s)
    # if "\'s" in line:
    #     line = line.replace("'s","")
    # for char in line:
    #     if char in blacklistChar:
    #         line = line.replace(char, '')
    #     elif char in '–':
    #         line = line.replace('–', ' ') #Remove dashes

    # return line.lower().split()

    # Ver 2
    # Remove possessive (apostrophe + s)

    #line = line.replace("'s", "")

    return re.sub(r"[^A-Za-z0-9\s']+", "", line).lower().split()


def stringCleaner2(line):
    # Remove non-ASCII chars
    line = ''.join([c if ord(c) < 128 else ' ' for c in line])

    # Remove possessives
    line = line.replace("'s", "")

    # Remove special characters
    special_chars = "!@#$%^&*()[]\{\}<>?`~\\|;:\"/"
    for c in special_chars:
        line = line.replace(c, '')

    # Convert all case to lower case and start tokenization
    lineArr = line.lower().split()

    # Strip leading and trailing punctuations from each token
    lineArr = [token.strip(punctuation) for token in lineArr]

    while "" in lineArr:
        lineArr.remove("")

    return lineArr


def openStopWordsFile(filepath: str):
    stopwordsFile = open('stopwords.txt', 'r')
    stopwords = dict.fromkeys(stopwordsFile.read().splitlines())
    stopwordsFile.close()

    return stopwords


def stemWord(word: str):
    return p.stem(word, 0, len(word)-1)


def retrieveResults(filepath, resultIdentifiers):
    result = []
    numResultRetrieved = 0
    with gzip.open(filepath, 'r') as file:
        for line in file:  # Line by line
            currDoc = json.loads(line)  # Load the data

            # Use BS4 to parse HTML
            soup = BeautifulSoup(currDoc['contents'], 'html.parser')
            # tempObj['parsed_contents'] = soup.get_text(separator=' ')

            tokens = stringCleaner2(soup.get_text(separator=' '))

            # currDoc['id']
            # Each entry in resultsIdentifier is [docID, pos of the searched term]
            for [resultDocID, resultPositions, resultTokenFreq] in resultIdentifiers:
                # print('from result:', type(resultDocID))
                if resultDocID == str(currDoc['id']):  # If the IDs matches
                    #print('ID', currDoc['id'])
                    #print('Title:', currDoc['title'])

                    # Get the context
                    firstOccurencePos = resultPositions[0]
                    lowest_start = max(0, firstOccurencePos-5)
                    context = " ".join(tokens[lowest_start:lowest_start + 10])
                    # print('Context:',
                    #      context)
                    # resultIdentifiers.pop(0)

                    result.append(
                        (currDoc['id'], currDoc['title'], resultTokenFreq, context, resultPositions))
                    numResultRetrieved += 1

            if numResultRetrieved == len(resultIdentifiers):
                break
    return result


# Method for displaying the summary of the doc provided the data
def resultDocSummary(id, title, termFreq, context, positions):
    print('Document ID:\t', id)
    print('Document Title:\t', title)
    print('Term frequency:\t', termFreq)
    print('Context:\t', context)
    print('Positions:\t', positions)
    print('\n')


def writeJSONToFile(folderPath, fileName, data):
    with open(folderPath + "/" + fileName, "w") as write_file:
        write_file.write(json.dumps(data))
        write_file.close()

# Method that accepts a list of dictionaries and clear each one


def dictClearer(listOfDicts):
    for dict in listOfDicts:
        dict.clear()
