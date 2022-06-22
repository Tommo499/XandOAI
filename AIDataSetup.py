from itertools import permutations
import json
import pprint

spots = '123456789'
jsonList = []

for leng in range(1,10):
    jsonList = []
    for branch in permutations(spots, leng):
        temp = {''.join(branch): {'w': 0, 'p': 0, 'parent': ''.join(branch[:-1])}}
        jsonList.append(json.dumps(temp))
        del temp
    json.dump(jsonList, open(f"C:\\Users\\twach\\PycharmProjects\\XandO\\XandOdata{leng}.json", 'w'))
    del jsonList

#json.dump(jsonList, open("C:\\Users\\twach\\PycharmProjects\\XandO\\XandOboard.json", 'w'))

#pprint.pprint(jsonList)
# Todo # Make another json file to put the constant and the simulation counter
