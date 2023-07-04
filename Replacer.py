# -*- using: utf-32 -*-
import sys
import codecs
import commands

# input: filePath(string),data file: path+file
# output: list of Entry , one by one. 
def readEntries(filePath):
	ls = []
		
	fopen = codecs.open(filePath, 'r')
	#fopen = codecs.open(filePath, 'r', encoding='utf-32')
	ls = fopen.readlines()
	fopen.close()
	#debug:
	print(ls)
	return ls

# input: list of Entry, one by one, to replace the wrong files.
# output:  Running result.
def replaceThem(ls, notTest):
	partialCommand = 'cp -r -y '
	for ent in ls:
		ent1 = ent.strip()
		path_l = ent.strip().split('/')
		path_l = path_l[2:]
		ent2 = ''.join(path_l)
		command = partialCommand + str(ent1) + ' ' + str(ent2)
		#debug:
		print(command)
		if notTest:
			(result_status, result_output) = commands.getstatusoutput(command)
			if result_status != 0:
				print('Error: ', result_output)
			else:
				print('File created:', result_output)
	return 0



def main(argv):
	if len(argv) == 1 or len(argv) == 2:
		print("Lack arguments. Not run. Notice: Place the data-file in /home/cuibe/work/replace/, and invoke it explicitly.")
		return -1
	else:
		if argv[1] == '--exec':
			notTest = True
		elif argv[1] == '-t':
			notTest = False
		else:
			print("You provides wrong option.Try again.")
			return -1	
	
	try:
		file = str(argv[2])
		filePath = "/home/cubie/work/replace/" + file
		
		#debug:
		print(filePath)
		print(argv)
	except Exception, err:
		print('Make path error:' + str(Exception) + str(err))
		
	result = 1
	entities = []
	try:
		entities = readEntries(filePath)
	except Exception, err:
		print('Reading file error:' + str(Exception) + str(err))
	if len(entities) > 0:
		try:
			result = replaceThem(entities, notTest)
		except Exception, err:
			print('Replacing error:' + str(Exception) + str(err))
	else:
		print("No file to copy, check your source-data file.")
	print("------------------------------")
	if result == 0:
		print("Done.")
	else:
		print("Proceed with error, check logs.")

if __name__ == '__main__' : main(sys.argv)
