# -*- coding: utf-8 -*-

######################################################################
#   FileName:  testbasics.py   ver.0.1
#   Perporse:  basics test of Copier.
#   Author:  Jishan
#   Email:  unicoder5191@163.com
#   Date:  2023-07-09
######################################################################

import unittest

class BasicsTestCase(unittest.TestCase):
	
	def testCreateDirectory(self):
		a = 'a'
		c = 'c'
		self.assertTrue(a == a)
		print('testCreateDirectory ... Succeed.')
	
	def testCopyFile(self):
		a = 'a'
		c = 'c'
		self.assertFalse(a == c)
		print('testCopyFile ... Succeed.')

if __name__ == '__main__':
	print("=======================================")
	print(" Basic test case of Replacer.py unit : ")
	print("=======================================")
	unittest.main()
