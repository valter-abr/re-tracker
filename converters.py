
global sampleData
sampleData = []

#Check if tag has value
def tagHasValue(targetText, tagName, isClosed=False):

	if isClosed:
		tag = '</' + tagName + '>'
	else:
		tag = '<' + tagName + '>'

	if targetText.find(tag) > -1:
		return True
	else:
		return False

#Get value from tag
def getValueFromTag(var, tag, valueType=0):
	### valueType: 
	#-> Default for STR,
	#-> 1 for MIDI, 
	#-> 2 for HEX, 
	#-> 3 for INT

	openTag = '<' + tag + '>'
	closedTag = '</' + tag + '>'

	value = var.split(openTag)[1].split(closedTag)[0]

	if valueType == 1:
		return noteToMIDI(value)

	elif valueType == 2:
		return int(value, 16)

	elif valueType == 3:
		return int(value)

	else:
		return value

#Note to MIDI values
def noteToMIDI(note):

	notes = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]
	counter = -1
	midiData = {}

	for octave in range(12):
		
		for i in range(128):

			if i % 12 == 0:
				counter += 1

				if counter > 10:
					counter = 0

				key = notes[octave] + str(counter)
				midiData[key] = str(i + octave)


	if note in midiData.keys():

		return int(midiData[note])
			
	else:
		return 0

#MIDI velocity to Decibel
def midiToDB(value):
	midiList = open('midiToDB.txt', 'r')
	dbList = []

	for i in midiList.readlines():
		dbList.append(i.split(';')[1].rstrip('\n'))
	
	midiList.close()
	return dbList[value]

#Samples to milliseconds at 44.1:
def samplesToMilliseconds(totalSamples, index=0):

	if index == 0:
		value = 1000/(44100/totalSamples)
		return round(value, 3)
	else:
		value = 1000/(22050/totalSamples)
		return round(value, 3)		

def isLooping(instrument):

	sampler_data = open('sampler_data.txt', 'r')
	array = []

	for i in sampler_data:

		item = i.rstrip().split(',')
		del item[4]

		array.append(item)

	sampler_data.close()

	return int(array[int(instrument-1)][3])

def shiftSampleDuration(note, instrument, index=0):
#def shiftSampleDuration():
	### Indexes:
	# 0 - Start location
	# 1 - Duration

	sampler_data = open('sampler_data.txt', 'r')
	array = []

	for i in sampler_data:

		item = i.rstrip().split(',')
		del item[3]

		array.append(item)

	sampler_data.close()

	if note != '-' and instrument != '-':

		nextNote = int(note) - int(array[int(instrument-1)][0])

		startLocation = float(array[int(instrument-1)][1])
		duration = float(array[int(instrument-1)][2])/2**(nextNote/12)

		if index == 0:
			return str(round(duration, 3))
		else:
			return str(round(startLocation, 3))

