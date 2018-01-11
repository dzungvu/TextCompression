import RunLengthText
from HuffmanCoding import HuffmanCoding

# RunLengthText.encodeMultiFile('data', True)

path = 'data\\TheFurnishedRoom.txt'
h = HuffmanCoding(path)
h.compress()