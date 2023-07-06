# -*- using: utf-32 -*-
#====================
# Python2  Author: Unic@
#====================
import sys
import codecs
import commands
import logging

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
def mkdir():
	partialCommand = 'mkdir -pv '
	#for ent in ls:
	#	ent1 = ent.strip()
	#	path_l = ent.strip().split('/')
	#	path_l = path_l[2:]
	#	ent2 = ''.join(path_l)
	#	command = partialCommand + str(ent1) + ' ' + str(ent2)
	
	command = partialCommand + './test/google/baidu/suning/newegg'
	#debug:
	print(command)
	
	(result_status, result_output) = commands.getstatusoutput(command)
	if result_status != 0:
		print('Error: ', result_output)
	else:
		print('File created:', result_output)
	return 0

def main(argv):
	if len(argv) > 1:
		print("Use user data-file. The file must in ~/work/replace/test/.")
		filePath = "/home/cuibe/work/replace/test/" + str(argv[1])
	else:
		filePath = "/home/cubie/work/replace/test/mkdir.txt"

	result = None
	try:
		result = mkdir()
	except Exception, err:
		print('Mkdir error:' + str(Exception) + str(err))

	print("------------------------------")
	#debug
	print(result)	
	if result == 0:
		print("Done.")
	else:
		print("Proceed with error or no Entities exists. check logs.")
if __name__ == '__main__' : 
	main(sys.argv)
