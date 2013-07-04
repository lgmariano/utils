#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find duplicate files recursively in a directory tree.
# The files are compared using hashes, therefore the name does 
# not matter for comparison. The files to be compared can be 
# filtered by the file extension.
#
# To run, simply call this script with a root directory and optional 
# file extensions.
# ex: find_duplicates.py /home/user/pictures jpg png
# Will search for duplicate files of type .jpg and .png on the directory
# /home/user/pictures and its subdirectories. Omitting file extensions 
# will search all files.

import sys
import hashlib
import os.path

def hash_sha256(file_path):
	with open(file_path, 'rb') as f:
		h = hashlib.sha256()
		h.update(f.read())
		return h.hexdigest()
	
def hash_md5(file_path):
	with open(file_path, 'rb') as f:
		h = hashlib.md5()
		h.update(f.read())
		return h.hexdigest()

def check_root_dir(root_path):
	if os.path.isdir(root_path):
		return True
		
	return False

# check parameters
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

if len(sys.argv) > 2:	# check extensions filter
	ext_filter = True
	for i in sys.argv[2:]:
		exts.add(('.' + i).lower())
	
	print 'Looking for files of type:'
	for i in exts:
		print i

	print


d = {}		# hash table: file hash -> file path
duplicates = []		# list of duplicates
hash = hash_md5		# hash function to be used

for root, dirs, files in os.walk(root_path):
	for f in files:
		
		if ext_filter:		# check file extension
			name, ext = os.path.splitext(f)
			if ext.lower() not in exts:
				continue
		
		file_path = os.path.join(root, f)
		hash_val = hash(file_path)
		print file_path, ' ', hash_val
		
		if hash_val not in d:
			d[hash_val] = file_path
		else:
			duplicates.append((d[hash_val], file_path))
		
print; print
if len(duplicates) == 0:
	print 'No duplicates!\n'
else:
	print 'Duplicates:'
	count = 0
	for i in duplicates:
		count += 1
		print count, '-', i[0], '<--->', i[1]
	
	print '\n', count, 'duplicate files found\n'

