#This script take in the fastas (he outputs of custom_vcf2fasta) and checks to see if they are all the same length, the N content, and the pairwise variations.



import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta_checker.py
'''

files = glob.glob('*.fa')

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
	print dict_key[1:]
	print 'length of sequence: ' + str(len(full_seq))
	print 'number of Ns: ' + str(full_seq.count('N'))


#Not Working!!!
with open('n_content.txt', 'w') as output1:
	output1.write('Sample	Sequence_Length	Number_of_Ns\n')
	for key in N_dict:
		output1_line = key + '	' + str(fasta_dict[key]) + '	' + str(N_dict[key]) + '\n'



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
		pairwise_dict_key = pairwise_dict_key1[1:] + '+' + pairwise_dict_key2[1:]
		pairwise_dict[pairwise_dict_key] = z
		print pairwise_dict_key
		print z
		y += 1
	i += 1

with open('pairwise_variants.txt', 'w') as output2:
	output2.write('Combintation	Number of Variants\n')
	for key in pairwise_dict:
		output2_line = key + '	' + str(pairwise_dict[key]) + '\n'
		output2.write(output2_line)








