#!/usr/bin/python

# find duplicate files recursively in a directory tree

import sys
import hashlib
import os.path
from os.path import join

def hash_sha256(file_path):
	f = open(file_path, 'rb')
	h = hashlib.sha256()
	h.update(f.read())
	f.close()
	return h.hexdigest()
	
def hash_md5(file_path):
	f = open(file_path, 'rb')
	h = hashlib.md5()
	h.update(f.read())
	f.close()
	return h.hexdigest()

def check_root_dir(root_path):
	if os.path.isdir(root_path):
		return True
		
	return False


if len(sys.argv) < 2:
	print 'Usage: find_duplicates.py "root_directory" <extensions>'
	print 'ex: find_duplicates.py /home/my_user jpg png'
	exit()

root_path = sys.argv[1]

if not check_root_dir(root_path):
	print root_path, 'not found'
	exit()

exts = set()
ext_filter = False

if len(sys.argv) > 2:	# add extensions filter
	ext_filter = True
	for i in sys.argv[2:]:
		exts.add(('.' + i).lower())
	
	print 'Looking for files of type:'
	for i in exts:
		print i

	print


d = {}		# hash table: file hash -> file path
duplicates = []		# list of duplicates


for root, dirs, files in os.walk(root_path):
	for f in files:
		
		if ext_filter:		# check file extension
			name, ext = os.path.splitext(f)
			if ext.lower() not in exts:
				continue
		
		file_path = join(root, f)
		hash_val = hash_md5(file_path)
		#hash_val = hash_sha256(file_path)
		print file_path, ' ', hash_val
		
		if hash_val not in d:
			d[hash_val] = file_path
		else:
			duplicates.append((d[hash_val], file_path))
		
print; print
if len(duplicates) == 0:
	print 'No duplicates!'
else:
	print 'Duplicates:'
	for i in duplicates:
		print i[0], '<--->', i[1]

