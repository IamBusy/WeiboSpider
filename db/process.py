#!/usr/bin/python3


import os
import sys
import base64
from array import array
import re
import time





patternHttp = re.compile(r'http[\w\?\\/:\.]*')
patternRepMark = re.compile(r'\,+|\.+|\。+|\，+')
patternKeyWord = re.compile(r'#')
patternTitle = re.compile('【[^】]+】')
patternForward = re.compile(r'//@[^:]+\:')
patternAt = re.compile(r'@[\S]+\s')

def filterUrl(line):
	return patternHttp.sub('',line)

def _removeRep(match):
	return match.group(0)[0]
def filterRepMark(line):
	return patternRepMark.sub(_removeRep,line)

def filterKeyWord(line):
	return patternKeyWord.sub('',line)

def filterTitle(line):
	return patternTitle.sub('',line)

def filterAt(line):
	return patternAt.sub('',line)

def filterForward(line):
	#match = re.match(r'//@.*', line)
	#match = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
	match = patternForward.split(line)
	res = ''
	i = len(match) - 1
	while i>=0:
		res=res+match[i]
		i = i-1
	#print res
	return res

def process(line):
	line = filterForward(line)
	line = filterTitle(line)
	line = filterAt(line)
	line = filterKeyWord(line)
	line = filterRepMark(line)
	line = filterUrl(line)
	return line


def openData():
	try:
		fsock = open(source, 'r')
		return fsock
	except IOError:
		print (IOError)
		print ("The file don't exist, Please double check!")
		exit()
