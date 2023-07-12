#!/usr/bin/python2
#====================
# Python2  Author: James@
# NOTICE : Must run in root !
# :  the source dict is like /...   dest dict is like /mnt/16orig/sdb1/...
#====================
import os
import sys
import codecs
import commands
import traceback

# input: filePath(string),data file: path+file
# output: list of Entry , one by one. 
#====================
def readEntries(filePath):
	ls = []
		
	fopen = codecs.open(filePath, 'r')
	#fopen = codecs.open(filePath, 'r', encoding='utf-32')
	ls = fopen.readlines()
	fopen.close()
	
	#debug:
	print("Entities: " + str(len(ls)))
	#print(ls)
	
	return ls

# input: list of Entry, one by one, to replace the wrong files.
# output:  Running result.
#====================
def placeThem(ls, notTest):
	partialCommand = 'cp -r --preserve '  # -y maybe? -p --preserve origin path .
	dest_path = '/mnt/16orig/sdb1'
	for ent in ls:
		ent1 = ent.strip()  # source
		path_l = ent.strip().split('/')  # dest
		
		#debug:
		#print('falsh get path_l:', path_l)
		path_l = path_l[1:-1]  # remove '' element of path_l's first.		
		path_l.insert(0, dest_path)  # add /mnt/16orig/sdb1 to first location of dest.
		#debug:
		#print('changed path_l:', path_l)
		#path_l = path_l[:-1]  # filter end dir due to /a/b/c/ -> cp -> /a/b/ || /a/b/c.txt -> /a/b/
		
		ent2 = '/'.join(path_l)  # no need to add first '/'.

		command = partialCommand + str(ent1) + ' ' + str(ent2)
		
		#debug:
		print(command)

		if notTest:
			
			copy_result = tryTwiceCopy(command, str(ent2))
			if copy_result == 0:
				print('replaceThem ok.')			 
			else:
				print('replaceThem error, return ' + str(copy_result))
				
	return 0

#Copy only try twice. The second try with mkdir.
#input: copy command.
#output: 0:Succeed; -1:fail;
#====================
def tryTwiceCopy(command, dest):
	try:
		(cp_status, cp_output) = cpFile(command)
	except Exception, err:
		print('Try copy once error: ' + str(Exception) + str(err))
		return -1
	if cp_status != 0:
		print('Cp error: ', str(cp_output))
		
		# ~~Try mkdir:~~
		
		mkdir = -2	
		try:
			mkdir = createDirectory(cp_output, dest)
		except Exception, err:
			print('Create dirctory error: ' + str(Exception) + str(err))
			
		if mkdir == -1:
			return -1
		elif mkdir == 0:
			try:
				(cp_status2, cp_output2) = cpFile(command)
			except Exception, err:
				print('Try copy twice error: ' + str(Exception) + str(err))
				return -1
			if cp_status2 != 0:
				print('Cp twice error: ', str(cp_output2))
			else:
				print('File created by mkdir: ', str(cp_output2))
				return 0

		else:  # mkdir == -2
			print('In mkdir of tryTwiceCopy error, check log.')
			return -1 
	else:
		print('File created: ', cp_output)
		return 0

#input : command is like cp -r.
#output: Succeed return (0, ""), fail return (-1, errormsg).
#====================
def cpFile(command):
	(result_status, result_output) = commands.getstatusoutput(command)
	if result_status != 0:
		print('In cpFile, cp error: ', result_output)
		return (-1, str(result_output))	
	else:
		print('File created by cpFile: ', result_output)
		return (0, "")

#====================
def createDirectory(cp_output, ent2):
	if True and ent2:
		(rsl_status, rsl_output) = commands.getstatusoutput('mkdir -pv ' + str(ent2))
		if rsl_status != 0:
			print('Mkdir error: ', str(rsl_output))
			return -1
		else:
			print('Direcoty created: ', str(rsl_output))
			return 0

#====================
def main(argv):
	#debug:
	print('Len(argv)=' + str(len(argv)) + '; argv[0]=' + argv[0])
	if len(argv) < 3:
		if len(argv) == 1 :
			print("Lack arguments. Not run. Notice: Place the data-file in /home/cuibe/work/replace/, and invoke it explicitly.")
			return -1
		elif len(argv) == 2 and (argv[1] == '--help' or argv[1] == '-h'):
			print("\nReplacer.py [-t|--exec|-h|--help] datafile \n-h --help   get the help notice.\n--exec   do real copy\n-t   do not real copy,test and verbos it only. ")
			return -1
		elif len(argv) == 2:
			print("Bad or lack option. Please reference help to give correct one.")
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
		filePath = "./" + file
		
		#debug:
		print(filePath)
		print(argv)
	except Exception, err:
		print('Make path error: ' + str(Exception) + str(err))
		
	entities = []
	try:
		entities = readEntries(filePath)
	except Exception, err:
		print('Reading file error: ' + str(Exception) + str(err))
	result = -1
	if len(entities) > 0:
		try:
			result = placeThem(entities, notTest)
		except Exception, err:
			print('Replacing error: ' + str(Exception) + str(err))
			traceback.print_exc()
	else:
		print("No file to copy, check your source-data file.")
	print("------------------------------")
	if result == 0:
		print("Done.")
		return 0
	else:
		print("Proceed with error, check logs.")
		return -1

if __name__ == '__main__' : main(sys.argv)
