# -*- using: utf-32 -*-
#====================
# Python2  Author: Adriatic@
#====================
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

def main(argv):
	if len(argv) > 1:
		print("Use user data-file. The file must in ~/work/replace/test/.")
		filePath = "/home/cuibe/work/replace/test/" + str(argv[1])
	else:
		filePath = "/home/cubie/work/replace/test/proving.txt"

	entities = []	
	try:
		entities = readEntries(filePath)
	except Exception, err:
		print('Reading file error:' + str(Exception) + str(err))

	print("------------------------------")
	if len(entities) > 0:
		print("Done.")
	else:
		print("Proceed with error or no Entities exists. check logs.")
if __name__ == '__main__' : 
	main(sys.argv)
