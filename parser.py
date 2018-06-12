
#------------------------initializations-------------------------

from converters import *
import zipfile, os, shutil

# Read zip file (xrns in this case):
zip = zipfile.ZipFile('Test.xrns')

# Read XML file:
global songFile
songFile = str(zip.read('Song.xml')).split("\\n")

# Data structure initialization:
global songData
songData = {}

# Write 64 lines:
def drawLines(): 
	drawLines = []

	for line in range(64):
		drawLines.append(['-','-','-','-','-','-','-','-'])

	return(drawLines)

def createPatterns():
	patterns = []

	for i in range(1,100):
		value = str(i)

		if len(value) < 2:
			value = '0' + str(i)

		patterns.append(value)

	return(patterns)

#-------------------------------//-------------------------------

def start(thisList=songFile):

	###############################################################
	#-------------------------------------------------------------#
	#-------------------------SAMPLER DATA------------------------#
	#-------------------------------------------------------------#
	###############################################################

	sampler_data = open('sampler_data.txt', 'w+')
	sampler_loops = open('sampler_loops.txt', 'w+')

	totalTags = 0
	auxList = []
	samples = {}

	for tag in thisList:

		if tagHasValue(tag, 'Sample'):
			totalTags += 1

	for i in range(1,totalTags+1):

		counter = 0
		item = []

		for tag in thisList:

			if tagHasValue(tag, 'Sample'):
				counter += 1

			if counter >= i and tagHasValue(tag, 'Sample', True):
				break

			if counter == i:
				if tagHasValue(tag, 'Sample') == False:
					item.append(tag)

		auxList.append(item)

	for z in range(len(auxList)):

		samples['Sample ' + str(z+1)] = auxList[z]

	auxList = []
	counter = 0

	for sample in samples:
		item = []
		counter += 1

		for tag in samples[sample]:

			if tagHasValue(tag, 'LoopMode'):
				loopMode = getValueFromTag(tag, 'LoopMode')

			elif tagHasValue(tag, 'LoopStart'):
				startPoint = getValueFromTag(tag, 'LoopStart', 3)

			elif tagHasValue(tag, 'LoopEnd'):
				endPoint = getValueFromTag(tag, 'LoopEnd', 3)

			elif tagHasValue(tag, 'BaseNote'):
				baseNote = getValueFromTag(tag, 'BaseNote', 3)
				item.append(baseNote)

			elif tagHasValue(tag, 'DisplayLength'):
				sampleSize = getValueFromTag(tag, 'DisplayLength', 3)

		if loopMode == 'Off':
			startTime = 0
			item.append(startTime)

			endTime = samplesToMilliseconds(sampleSize)
			item.append(endTime)

			item.append(0)
			sampler_loops.write(str(counter) + ', 0\n')

		else:
			if startPoint > 0:
				startTime = samplesToMilliseconds(startPoint)
			else:
				startTime = 0
			item.append(startTime)

			endTime = samplesToMilliseconds(endPoint-startPoint, 1)
			item.append(endTime)

			item.append(1)
			sampler_loops.write(str(counter) + ', 1\n')

		for i in item:
			sampler_data.write(str(i) + ',')

		sampler_data.write('\n')
	
	sampler_data.close()
	sampler_loops.close()

	###############################################################
	#-------------------------------------------------------------#
	#-------------------------PATTERN DATA------------------------#
	#-------------------------------------------------------------#
	###############################################################

	totalTags = 0
	auxList = []

	for tag in thisList:

		if tagHasValue(tag, 'Pattern'):
			totalTags += 1

	if totalTags >= 2:
		totalTags //= 2

	#------------------------------//------------------------------
	#---------------------get pattern contents---------------------

	for i in range(1,totalTags+1):

		counter = 0
		item = []

		for tag in thisList:

			if tagHasValue(tag, 'Pattern'):
				counter += 1

			if counter >= i and tagHasValue(tag, 'Pattern', True):
				break

			if counter == i:
				if tagHasValue(tag, 'Pattern') == False:
					item.append(tag)

		auxList.append(item)

	#------------------------------//------------------------------
	#---------------------store data structure---------------------

	for z in range (len(auxList)):

		songData['Pattern ' + str(z)] = auxList[z]

	del auxList
	del thisList

	#------------------------------//------------------------------
	#-----------------------passa os valores-----------------------

	for pattern in songData:
		findTracks('<Pattern>', '</Pattern>', songData[pattern], pattern)

	#------------------------------//------------------------------

def findTracks(openTag, closedTag, thisList, pattern, totalTags=0):

	#----------------obter o número de tags abertos----------------

	openTag = '<PatternTrack type="PatternTrack">'
	closedTag = '</PatternTrack>'

	for tag in thisList:

		if tag.find(openTag) > -1:

			totalTags += 1

	#------------------------------//------------------------------
	#-------------obter a lista segmentada por tracks--------------

	auxList = []

	for i in range(1,totalTags+1):

		counter = 0
		item = []

		for k in thisList:

			if k.find(openTag) > -1:
				counter += 1

			if counter >= i and k.find(closedTag) > -1:
				break

			if counter == i:
				if k.find(openTag) == -1:
					item.append(k)

		auxList.append(item)

	#------------------------------//------------------------------
	#---------------------store data structure---------------------

	songData[pattern].clear()
	songData[pattern] = dict(songData[pattern])

	for z in range (len(auxList)):

		songData[pattern]['Track ' + str(z+1)] = auxList[z]

	del auxList
	del thisList

	#------------------------------//------------------------------
	#-----------------------passa os valores-----------------------

	trackIndex = 0

	for track in songData[pattern]:
		findLines(songData[pattern][track], pattern, track)

	#------------------------------//------------------------------

def findLines(thisList, pattern, track, totalTags=0):

	#------------------------find line tags------------------------

	openTag = '<Line index="'
	closedTag = '</Line>'

	for tag in thisList:

		if tag.find(openTag) > -1:

			totalTags += 1

	#------------------------------//------------------------------
	#-----------------get lines from each channel------------------
	'''
	item ID
	[0] Note
	[1] Volume
	[2] Duration
	[3] Instrument
	[4] Start location
	[5] Fade in
	[6] Fadeout
	[7] Go to pattern
	'''
	auxList = drawLines()
	lineIndex = None

	patternList = createPatterns()
	note = '-'
	inst = '-'
	fxValue = '-'
	fxNumber = '-'

	for i in range(1,totalTags+1):

		counter = 0
		item = ['-','-','-','-','-','-','-','-']

		for k in thisList:

			if k.find(openTag) > -1:
				counter += 1
				lineIndex = int(k.split(openTag)[1].split('">')[0])

			if counter >= i and k.find(closedTag) > -1:
				break

			if counter == i:

				# Note/pitch command:
				if tagHasValue(k, 'Note'):
					note = getValueFromTag(k, 'Note', 1)
					item[0] = note-12

					# Force values
					item[1] = 90.0 	#--> Default volume

				# Instrument/sample command:
				elif tagHasValue(k, 'Instrument'):
					inst = getValueFromTag(k, 'Instrument', 2)
					item[3] = inst
					#item[8] = isLooping(inst)

				# Volume/amplitude/velocity command:
				elif tagHasValue(k, 'Volume'):
					vol = getValueFromTag(k, 'Volume', 2)

					if vol <= 127: # Exclude mute command
						volDB = midiToDB(vol)
						item[1] = str(volDB)
					else: # Rewrite mute command
						item[0] = 0
						item[1] = 0
						item[3] = 32

				# Tags from FX column:
				elif tagHasValue(k, 'Value'):
					fxValue = getValueFromTag(k, 'Value')

				elif tagHasValue(k, 'Number'):
					fxNumber = getValueFromTag(k, 'Number')

				elif fxNumber in patternList:		#---> Get the special pattern change command

					if fxNumber == '01':
						goTo = 1
					else:
						goTo = int(fxNumber) * 64 + int(fxValue)

					item[7] = str(goTo)

				if tagHasValue(k, 'Note') or tagHasValue(k, 'Instrument'):

					item[2] = shiftSampleDuration(note, inst, 0)
					item[4] = shiftSampleDuration(note, inst, 1)
					item[5] = 0
					item[6] = 0

		auxList[lineIndex] = item

	#------------------------------//------------------------------
	#---------------------store data structure---------------------

	songData[pattern][track].clear()
	songData[pattern][track] = dict(songData[pattern][track])

	songData[pattern][track] = auxList

	del auxList
	del thisList

	#------------------------------//------------------------------

def getTempo(thisList=songFile):

	# Get BPM value
	bpm = getValueFromTag(thisList[3], 'BeatsPerMin', 3)
	tempo = round((60000/bpm)/4, 2)		#--> Convert BPM to milliseconds

	return str(tempo)

def getInstruments(module=zip):

	instruments = []
	counter = -1
	
	for i in module.namelist():
		counter += 1

		if i.startswith('SampleData'):

			instruments.append(str(counter)+', read -resize sound/sample'+str(counter)+'.wav sample'+str(counter)+';')
			module.extract(i, '.')
			
	module.close()
	
	counter = 0
	
	if not os.path.exists('../Player/sound'):
		os.makedirs('../Player/sound')

	for directory in os.listdir('SampleData'):
		counter += 1

		path = 'SampleData/' + directory

		#Create samples folder
		for file in os.listdir(path):
			os.rename(path + '/' + file, '../Player/sound/sample' + str(counter) + '.wav')

	#Delete the old folder
	shutil.rmtree('SampleData', ignore_errors=True)
	
	return instruments

def getTotalLines(thisList=songFile, totalPatterns=0): 

	openTag = '<Pattern>'
	closedTag = '</Pattern>'

	for tag in thisList:

		if tag.find(openTag) > -1:

			totalPatterns += 1

	if totalPatterns >= 2:
		totalPatterns //= 2
		return str(totalPatterns*64)

def getPatternIds():

	patterns = [1]
	totalLines = getTotalLines()

	for i in range(1, int(totalLines)):

		if i % 64 == 0:

			patterns.append(i+1)

	return patterns

def getSongData():

	return songData


