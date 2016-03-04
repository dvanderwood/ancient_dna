#THIS IS AWFUL DON'T USE IT


#This script take in concatanated fasta of the outputs of custom_vcf2fasta and checks to see if they are all the same length.

#File should be titiled all_*.fa

import sys, os, subprocess, glob, linecache

'''
usage: vcf2fasta_checker.py
'''

files = glob.glob('all*.fa' or 'all*.fasta')
cat_fasta = files[0]

fasta_dict = {}
with open(cat_fasta) as fasta:
	fasta = fasta.read()
	fasta_list = fasta.split('>')
	fasta_list = fasta_list[1:]
	i = 0
	while i < len(fasta_list):
		dict_key = []
		dict_out = []
		for char in fasta_list[i]:
			dict_key.append(char)
			if char == '\n':
				for char in fasta_list[i]:
					if char != '\n':	
						dict_out.append(char)
		fasta_dict[''.join(dict_key)] = ''.join(dict_out)
		i += 1

print len(fasta_dict)


