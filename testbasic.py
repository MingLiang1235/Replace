# -*- coding: utf-8 -*-

######################################################################
#   FileName:  testbasic.py   ver.0.1
#   Perporse:  basics test of Copier.
#   Author:  Jishan
#   Email:  unicoder5191@163.com
#   Date:  2023-07-09
######################################################################

import unittest
import Replacer
import os

class BasicsTestCase(unittest.TestCase):
	
	def testCreateDirectory(self):
		path = 'test/testDirDest/abc/321'  # 'test/testDirDest/abc/123/qsl'
		Replacer.createDirectory("test", path)	
		self.assertTrue(os.path.exists(path))
		print('testCreateDirectory ... Succeed.')
	
	def testCpFile(self):
		sou_path = 'test/testCp/abc/123/a3.txt'
		des_path = 'test/testCpDest/abc/123/a3.txt'
		command = 'cp -r ' + sou_path + ' ' + des_path		
		Replacer.cpFile(command)
		self.assertTrue(os.path.exists(des_path))
		print('testCopyFile ... Succeed.')

	def testTwiceCopy(self):
		sou_path = 'test/testCp/abc/1/qsl/a2.txt'
		des_path = 'test/testCpDest/abc/1/qsl'
		command = 'cp -r ' + sou_path + ' ' + des_path		
		Replacer.tryTwiceCopy(command, des_path)  # here catch a hugh mistake!
		self.assertTrue(os.path.exists(des_path))
		print('testTwiceCopy ... Succeed!')		

	def testRplaceThem(self):
		ls = ['/home/cubie/work/replace/test/testCp/abc/1/qsl/a2.txt','/home/cubie/work/replace/test/testCp/abc/1/qsl','/home/cubie/work/replace/test/testDir/abc/123/qsl']
		notTest = True
		print(ls)
		Replacer.replaceThem(ls, notTest)  # here catch a hugh mistake, too!
		self.assertTrue(os.path.isfile('/replace/test/testCp/abc/1/qsl/a2.txt'))
		self.assertTrue(os.path.exists('/replace/test/testCp/abc/1/qsl'))
		self.assertTrue(os.path.isdir('/replace/test/testDir/abc/123/qsl'))
		print('testTwiceCopy ... Succeed!')		

if __name__ == '__main__':
	print("=======================================")
	print(" Basic test case of Replacer.py unit : ")
	print("=======================================")
	unittest.main()
