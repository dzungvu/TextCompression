import pickle
import os
import glob

#This folder is created automaticly to contain compressed data
compressedFolder = 'RunlengthCompressed\\'

#This folder is created automaticly to contain decompressed data
decompressedFolder = 'RunlengthDecompressed\\'

realityRatios = []
theoryRatios = []

'''
@param pathData path of file want to compress
'''
def encode(pathData):

	fileRead = open(pathData, 'r')
	input_string = fileRead.read()

	count = 1
	prev = ''
	lst = []

	for character in input_string:
		if character != prev:
			if prev:
				entry = (prev,count)
				lst.append(entry)
			count = 1
			prev = character
		else:
			count += 1
	else:
		entry = (character,count)
		lst.append(entry)

	pathSplit = str(fileRead.name).split('\\')
	fileName = pathSplit[len(pathSplit) - 1].split('.')

	if not os.path.exists(compressedFolder):
		os.makedirs(compressedFolder)

	pathCompress = compressedFolder + fileName[0] + '.pkl'
	with open(pathCompress, "wb") as fp:
		pickle.dump(lst, fp)

	fileRead.close()

	sizeBefore = os.path.getsize(pathData)
	sizeAfter = os.path.getsize(pathCompress)
	ratio = float(sizeBefore/sizeAfter)

	realityRatios.append(ratio) 
	print ('Ratio of file ' + fileName[0] + ' using Runlength coding = ' + str(ratio))

	theory = ''
	for item in lst:
		theory += (item[0] + str(item[1]))

	ratio = float(len(input_string) / (len(theory)))
	theoryRatios.append(ratio)
 
'''
@param pathCompress path of compressed file need to decompress
'''
def decode(pathCompress):

	lst = []
	with open(pathCompress, "rb") as fp:
		lst = pickle.load(fp)

	q = ""
	for character, count in lst:
		q += character * count

	pathSplit = pathCompress.split('\\')
	fileName = pathSplit[len(pathSplit) - 1].split('.')

	if not os.path.exists(decompressedFolder):
		os.makedirs(decompressedFolder)

	pathDecompress = decompressedFolder + fileName[0] + '.txt'
	fileDecompressed = open(pathDecompress, 'w')
	fileDecompressed.write(q)
	fileDecompressed.close()




'''
@param pathFolder folder contain .txt files need to endcode
'''
def encodeMultiFile(pathFolder):
	for file in os.listdir(pathFolder):
		if file.endswith(".txt"):
			encode(os.path.join(pathFolder, file))


'''
@param pathFolder folder contain .pkl file need to decode
'''
def decodeMultiFile(pathFolder):
	for file in os.listdir(pathFolder):
		if file.endswith(".pkl"):
			decode(os.path.join(pathFolder, file))

#call method endcode
pathFolder = 'text_data'
encodeMultiFile(pathFolder)
averageRealityRatio = 0
averageTheoryRatio = 0
for ratio in realityRatios:
	averageRealityRatio += ratio

for ratio in theoryRatios:
	averageTheoryRatio += ratio

averageRealityRatio = float(averageRealityRatio / len(realityRatios))
averageTheoryRatio = float (averageTheoryRatio / len(theoryRatios))
with open('RunlengthRecord.txt', 'w') as f:
	f.write('Runlength theory average ratio: ' + str(averageTheoryRatio) + '\n')
	f.write('Runlength reality average ratio: ' + str(averageRealityRatio))

f.close()


##Call method decode
# pathFolder = 'RunlengthCompressed'
# decodeMultiFile(pathFolder)
