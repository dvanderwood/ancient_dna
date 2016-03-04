#This script take in concatanated fasta of the outputs of custom_vcf2fasta and checks to see if they are all the same length.

#File should be titiled all_*.fa

import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta_checker.py
'''

files = glob.glob('*.fa' or '*.fasta')

fasta_dict = {}
N_dict = {}
for file in files:
	dict_key = linecache.getline(file,1)
	dict_key = dict_key.strip()
	with open(file) as fasta:
		next(fasta)
		full_seq_lines = []
		for line in fasta:
			line1 = line.strip()
			full_seq_lines.append(line1)
		full_seq = ''.join(full_seq_lines)
	fasta_dict[dict_key[1:]] = full_seq
	N_dict[dict_key[1:]] = full_seq.count('N')
	print dict_key
	print len(full_seq)
	print full_seq.count('N')


pairwise_dict = {}
i = 1
for file in files:
	pairwise_dict_key1 = linecache.getline(file,1)
	pairwise_dict_key1 = pairwise_dict_key1.strip()
	with open(file) as fasta:
		next(fasta)
		full_seq_lines = []
		for line in fasta:
			line1 = line.strip()
			full_seq_lines.append(line1)
	y = i
	while y < len(files):
		with open(files[y]) as fasta2:
			pairwise_dict_key2 = linecache.getline(files[y],1)
			pairwise_dict_key2 = pairwise_dict_key2.strip()
			next(fasta2)
			full_seq_lines2 = []
			for line in fasta2:
				line1 = line.strip()
				full_seq_lines2.append(line1)
		j = 0
		z = 0
		while j < len(full_seq_lines):
			if full_seq_lines[j] != full_seq_lines2[j]:
				k = 0
				while k < len(full_seq_lines[j]):
					if full_seq_lines[j][k] != full_seq_lines2[j][k]:
						z += 1
					k += 1
			j +=1
		pairwise_dict_key = pairwise_dict_key1 + '+' + pairwise_dict_key2
		pairwise_dict[pairwise_dict_key] = z
		print pairwise_dict_key
		print z
		y += 1
	i += 1


