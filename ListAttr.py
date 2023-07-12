#!/usr/bin/python2
#====================
# Python2  Author: James@
# NOTICE : Must run in root !
#====================
import os
import sys
import codecs
import commands
import traceback
from stat import *
import pwd
import grp
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
	print(ls)
	
	return ls

# input: list of Entry, to insert head on each of one
# output: Modify the outputfile ,return 0 if success, -1 if fail.
#====================
def printAttr(ls, notTest, outfile='./git-attr.log'):
	#outfile = "./git.new-input.txt"
	fwrite = codecs.open(outfile, 'w')
	for each in ls:  # each with '\n'.
		path = each.strip()
		line = get_file_attr(path)
		
		(user_, group_, list_access_) = get_user_attr(path)
		usr_attr_ = ''
		for item in list_access_:
			usr_attr_ += item
		usr_attr_ = usr_attr_ + ' ' + user_ + ':' + group_ + ' '
		# singtax not support:#line = line.insert(6, usr_attr_)  # '_file ' is 5 , insert before index 6.
		tuple_line = line.partition(line[0:6])  # for insert before index 6
		#debug
		#print('line.partition(line[0:6])', tuple_line)
		ls_line = list(tuple_line)[1:]
		#debug
		#print('list(tuple_line)[1:]',ls_line)
		ls_line.insert(1, usr_attr_)  # must convert to list to insert one .
		#debug
		#print(ls_line)
		line = ''.join(ls_line)
		#debug
		print(line.strip())  # line with '\n',so strip.
		if notTest:
			fwrite.write(line)
	fwrite.close()
	return 0
# input: full path of an Entry, for user and group and access privilige to get
# output: (user,group,listofprivilige) of that Entry
def get_user_attr(path):
	stat = os.stat(path)
	mode = os.stat(path).st_mode
	uid = stat.st_uid
	gid = stat.st_gid
	
	is_readable_u = 'r' if (mode & S_IRUSR > 0) else '-'
	is_readable_g = 'r' if (mode & S_IRGRP > 0) else '-'
	is_readable_o = 'r' if (mode & S_IROTH > 0) else '-'

	is_writable_u = 'w' if (mode & S_IWUSR > 0) else '-'
	is_writable_g = 'w' if (mode & S_IWGRP > 0) else '-'
	is_writable_o = 'w' if (mode & S_IWOTH > 0) else '-'

	is_execable_u = 'x' if (mode & S_IXUSR > 0) else '-'
	is_execable_g = 'x' if (mode & S_IXGRP > 0) else '-'
	is_execable_o = 'x' if (mode & S_IXOTH > 0) else '-'

	user_info_ = pwd.getpwuid(uid)
	user = user_info_.pw_name
	
	group_info_ = grp.getgrgid(gid)
	group = group_info_.gr_name

	ls_access = []
	ls_access.append(is_readable_u)
	ls_access.append(is_writable_u)
	ls_access.append(is_execable_u)
	ls_access.append(is_readable_g)
	ls_access.append(is_writable_g)
	ls_access.append(is_execable_g)
	ls_access.append(is_readable_o)
	ls_access.append(is_writable_o)
	ls_access.append(is_execable_o)

	return (user, group, ls_access)
# input: full path of an Entry, may represents a file, a dir ,a link, and a ?
# output: line of the path Entry's attribute, with '\n', for write to output file.
def get_file_attr(path):
	
	retStr = "null"
	mode = os.stat(path).st_mode
	if S_ISDIR(mode):
		retStr = '_dir  ' + path + '\n'
	elif S_ISREG(mode):
		retStr = '_file ' + path + '\n'
	elif S_ISLNK(mode):
		retStr = '_lnk  ' + path + '\n'
	else:
		retStr = '?___  ' + path + '\n'
	return retStr
# input: list of Entry, one by one, to replace the wrong files.
# output:  Running result.
#====================
def replaceThem(ls, notTest):
	partialCommand = 'cp -r --preserve '  # -y maybe? -p --preserve origin path .
	for ent in ls:
		ent1 = ent.strip()
		end_ls = ent1
		path_l = ent.strip().split('/')
		
		#debug:
		#print('path_l:', path_l)
		
		path_l = path_l[4:]  # filter /mnt/16orig/sdb2.
		
		if (os.path.isfile(end_ls)):
			path_l = path_l[:-1]  # filter end file of path.
		elif (os.path.isdir(end_ls)):
			path_l = path_l[:-1]  # filter end dir due to /a/b/c/ -> cp -> /a/b/
		
		ent2 = '/' + '/'.join(path_l)  # add first '/'.

		command = partialCommand + str(ent1) + ' ' + str(ent2)
		
		#debug:
		print(command)

		if notTest:
			copy_results = -1
			copy_result = tryTwiceCopy(command, str(ent2))
			if copy_result == 0:
				continue			 
			else:
				print('tryTwice return ' + str(copy_result))
				continue
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
			print('In mkdir of replaceThem error, check log.')
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
		
		define_outfile = False
		if len(argv) > 3 :
			outfile = './' + str(argv[3])  # argv[3] must have if len > 3.
			define_outfile = True
		#debug:
		print(filePath, outfile)
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
			if define_outfile == True:
				result = printAttr(entities, notTest, outfile)
			else:
				result = printAttr(entities, notTest)
		except Exception, err:
			print('Changing error: ' + str(Exception) + str(err))
			traceback.print_exc()
	else:
		print("No Entity to change, check your source-data file.")
	print("------------------------------")
	if result == 0:
		print("Done.")
		return 0
	else:
		print("Proceed with error, check logs.")
		return -1

if __name__ == '__main__' : main(sys.argv)
