from converters import *

def main():

	#-----------------------------
	import parser
	module = open('../Player/module.txt', 'w+')
	module_info = open('../Player/module_info.txt', 'w+')
	module_samples = open('../Player/module_samples.txt', 'w+')
	module_patterns = open('../Player/module_patterns.txt', 'w+')

	parser.start()

	song = parser.getSongData()

	# Example for printing:
	# print(song['Pattern 0']['Track 1'])
	#-----------------------------

	#### Write the track ####
	counter = 0
	for pattern in song:

		for line in range(64):

			counter += 1
			module.write(str(counter) + ', ')

			for track in song[pattern]:

				for i in range(8):
					module.write(str(song[pattern][track][line][i]) + ' ')

			module.write(';\n')

	#### Write track global info ####
	module_info.write('1, tempo ' + parser.getTempo() + ';\n')
	module_info.write('2, totalLines ' + parser.getTotalLines() + ';\n')

	#### Write samples list ####
	for i in parser.getInstruments():

		module_samples.write(i + '\n')

	#### Write patterns info ####
	counter = 0
	for k in parser.getPatternIds():
		counter += 1

		module_patterns.write(str(counter) + ', ' + str(k) + ';\n')

	module.close()
	module_info.close()
	module_samples.close()
	module_patterns.close()

if __name__ == '__main__':
	main()