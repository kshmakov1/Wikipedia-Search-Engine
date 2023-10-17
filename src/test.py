

from asyncore import read
from textwrap import indent

from matplotlib.font_manager import json_dump
from helper_module import stringCleaner
from helper_module import stringCleaner2
from helper_module import stemWord, writeJSONToFile
from nltk import word_tokenize
import json
# Importing the library
import psutil
import os

from functools import reduce
# s = '''
#     Hello, there! This is a test file!

#     first-person
#     third-person
#     hello-world
#     Jame's laptop
#     1998-2000
#     1995–1998
#     hello - world
#     !@#$%^&*()-=_+<>,./?;:'"↑h↑e↑l↑l↑o↑↑↑↑↑↑↑
#     ABC'DEF
#     a€bñcá
#     a_b^0
# '''
# i = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', ';',
#      '<', '=', '>', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', '\t']
# # print(stringCleaner(s))
# # print(word_tokenize(s))
# # print(s.split())
# # print(stemWord('Activision\'s'))

# print(stringCleaner2(s))

# # Getting % usage of virtual_memory ( 3rd field)
# print('RAM memory % used:', psutil.virtual_memory()[2])
# # Getting usage of virtual_memory in GB ( 4th field)
# print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)


# sampleDictStr = '''{
# "1.3": {
#     "3": { "token_frequency": 2, "position": [1081, 4038] },
#     "1": { "token_frequency": 1, "position": [831] },
#     "600": { "token_frequency": 1, "position": [831] },
#     "0": { "token_frequency": 1, "position": [831] },
#     "4": { "token_frequency": 1, "position": [831] }
#   }
# }'''

# sampleDict = json.loads(sampleDictStr)

# keys = sampleDict.keys()

# for key in sampleDict.keys():
#     sampleDict[key] = sorted(sampleDict[key].items())

# print(sampleDict)
# # print(sampleDict)
# # sortedDict = dict(sorted(sampleDict.items()))

# # print(sortedDict)
process = psutil.Process()
print(process)

# input()


def readJSON(filePath):
    f = open(filePath)
    return json.load(f)


# post0 = readJSON('../output/test/postings0.json')
post0 = readJSON('../output/test/postings3.json')
post1 = readJSON('../output/test/postings4.json')
combined = readJSON('../output/test/combinedPostings.json')
# post1 = readJSON('../output/blocks/postings1.json')
# =====================start
# dict_seq = [post0, post1]

# Merge 2 dicts together!!
# newDict = reduce(lambda d1, d2: {k: d1.get(k, 0)+d2.get(k, 0)
#                                  for k in set(d1) | set(d2)}, dict_seq)
# =====================end
# writeJSONToFile('../output', 'combined.json', newDict)
# print(process.memory_info().rss / (1024 ** 3))
# for keys in post1['achim'].keys():
#     print(keys)
#     post1['achim'][int(keys)] = 1

# =====================start
# print(type(post1['achim']))
# d = post1['achim']
# print(dict(sorted(post1['achim'].items(), key=lambda item: int(item))))
# print(post1['achim'])


# Sort postings by ID!!!
# for k in post1:
#     post1[k] = {key: value for key, value in sorted(
#         post1[k].items(), key=lambda item: int(item[0]))}
# =====================end


# for k in post0:
#     # print(k)
#     if k in post1:
#         post0[k].update(post1[k])

# for k in post1:
#     if k not in post0:
#         post0[k] = post1[k]

# writeJSONToFile('../output/test', 'combinedPostings.json', post0)
# post1['achim'] = d_sorted
# print(post1)

f = open("../output/test/query.txt", "w")


userInput = input('Enter term:')
while userInput != 'ZZEND':
    if userInput in post0 and userInput in post1:
        #print(json.dumps(post0[userInput], indent=4))
        f.write(str(post0[userInput].keys()))
        f.write("="*10)
        # f.write(json.dumps(post1[userInput], indent=4))
        f.write(str(post1[userInput].keys()))
        f.write("="*10)
        # f.write(json.dumps(combined[userInput], indent=4))
        f.write(str(combined[userInput].keys()))
    userInput = input('Enter term:')
f.close()
#print(json.dumps(post0, indent=4))
