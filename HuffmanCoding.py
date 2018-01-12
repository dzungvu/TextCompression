import heapq
from collections import defaultdict
import pickle
import os

compressedFolder = 'HufmanCompressed\\'
decompressedFolder = 'HuffmanDecompressed\\'
dictionaryFolder = 'HuffmanDictionary\\'

'''
Calculate frequent for each charater in data input
'''
def frequent(data):
    frequency = defaultdict(int)
    for symbol in data:
        frequency[symbol] += 1

    return frequency

'''
Encode characters to binary numbers
'''
def huffmanEncodeCharacter(data):

    frequency = frequent(data)
    heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

'''
From characters and binary strings of each characters, create dictionary
'''
def createDictionary(huff):
    dic = {}
    for p in huff:
        dic[p[0]] = p[1]

    return dic

'''
Encode string in file using huffman
'''
def encode(pathFile):
    compressed = ''
    fileRead = open(pathFile, 'r')
    
    input_string = fileRead.read()

    huff = huffmanEncodeCharacter(input_string)
    dic = createDictionary(huff)

    for i in range(0, len(input_string)):
        compressed = compressed + dic[input_string[i]]

    pathSplit = str(fileRead.name).split('\\')
    fileName = pathSplit[len(pathSplit) - 1].split('.')

    if not os.path.exists(compressedFolder):
        os.makedirs(compressedFolder)
    
    if not os.path.exists(dictionaryFolder):
        os.makedirs(dictionaryFolder)

    pathCompress = compressedFolder + fileName[0] + '.bin'
    pathDictionary = dictionaryFolder + fileName[0] + '.pkl'

    with open(pathCompress, "w") as fp:
        fp.write(compressed)

    with open(pathDictionary, "wb") as fp:
        pickle.dump(dic, fp)

    sizeBefore = len(input_string) * 7
    sizeAfter = len(compressed)

    print ('Ratio of file ' + fileName[0] + ' using huffman = ' + str(float(sizeBefore/sizeAfter)))
'''
Using dictionary, decode file using huffman
'''
def decode (dictionaryPath, pathFile):

    with open(dictionaryPath, 'rb') as f:
        dictionary = pickle.load(f)
    fileRead = open(pathFile, 'r')
    text = fileRead.read()

    res = ""
    while text:
        for k in dictionary.keys():
            if text.startswith(dictionary[k]):
                res += k
                text = text[len(dictionary[k]):]

    pathSplit = pathFile.split('\\')
    fileName = pathSplit[len(pathSplit) - 1].split('.')

    if not os.path.exists(decompressedFolder):
        os.makedirs(decompressedFolder)

    pathDecompress = decompressedFolder + fileName[0] + '.txt'
    fileDecompressed = open(pathDecompress, 'w')
    fileDecompressed.write(res)
    fileDecompressed.close()
    return res

def encodeMultiFile(pathFolder):
	for file in os.listdir(pathFolder):
		if file.endswith(".txt"):
			encode(os.path.join(pathFolder, file))


def decodeMultiFile(dictionaryFolder, pathFolder):
    for file in os.listdir(pathFolder):
        if file.endswith(".bin"):
            filePiece = file.split('.')
            filename = filePiece[0] + '.pkl'
            decode(os.path.join(dictionaryFolder, filename), os.path.join(pathFolder, file))

pathFolder = 'text_data'
encodeMultiFile(pathFolder)

# pathFolder = 'HufmanCompressed'
# pathDictionary = 'HuffmanDictionary'
# decodeMultiFile(pathDictionary, pathFolder)









