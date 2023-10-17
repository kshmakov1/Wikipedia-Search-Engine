import ijson
from asyncore import write
import glob
from heapq import merge
from functools import reduce
from helper_module import writeJSONToFile
import json


def readJSON(filePath):
    f = open(filePath)
    return json.load(f)


def mergeDictionaries(readFolder, outputFolder):
    readPath = readFolder + "/dictionary*.json"

    allDictFilesPath = glob.glob(readPath)
    allDictFilesPath = sorted(allDictFilesPath)
    print(allDictFilesPath)
    dictData = []

    for d in allDictFilesPath:
        dictData.append(readJSON(d))

    # dict_seq = [post0, post1]

# Merge 2 dicts together!!
    mergedDict = reduce(lambda d1, d2: {k: d1.get(k, 0)+d2.get(k, 0)
                                        for k in set(d1) | set(d2)}, dictData)

    sortedDict = dict(sorted(mergedDict.items()))

    writeJSONToFile(outputFolder, 'combinedDict.json', sortedDict)


# mergeDictionaries('../output/blocks', '../output/combine')

def merge2Postings(post0, post1):
    for k in post0:
        # print(k)
        if k in post1:
            post0[k].update(post1[k])

    for k in post1:
        if k not in post0:
            post0[k] = post1[k]


def mergePostings(readFolder, outputFolder):
    readPath = readFolder + "/postings*.json"

    allPostingsFilesPath = glob.glob(readPath)
    allPostingsFilesPath = sorted(allPostingsFilesPath)
    print(allPostingsFilesPath)

    if len(allPostingsFilesPath) > 0:
        workingPosting = readJSON(allPostingsFilesPath.pop(0))

    while len(allPostingsFilesPath) > 0:
        currPosting = readJSON(allPostingsFilesPath.pop(0))
        merge2Postings(workingPosting, currPosting)

    sortedPostings = dict(sorted(workingPosting.items()))
    # for key in sortedPostings.keys():
    #     sortedPostings[key] = sorted(sortedPostings[key].items())

    for k in sortedPostings:
        sortedPostings[k] = {key: value for key, value in sorted(
            sortedPostings[k].items(), key=lambda item: int(item[0]))}

    writeJSONToFile(outputFolder, 'combinedPostings.json', sortedPostings)


# mergePostings('../output/blocks copy', '../output/combine')

pairs = [0, 1, 2, 3, 4, 5, 6]

while len(pairs) > 0:
    print(pairs.pop(0))

for prefix, the_type, value in ijson.parse(open("../output/blocks/postings0.json")):
    print(value)
