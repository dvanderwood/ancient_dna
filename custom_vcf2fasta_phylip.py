#Take in fastas output by custom_vcf2fasta and output a single phylip file.

import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta_phylip.py
'''


files = glob.glob('*.fa')

phylip_header1 = str(len(files))

seq_list = []
id_list = []
for file in files:
	phylip_id = linecache.getline(file,1)
	phylip_id = phylip_id.split('.')
	phylip_id = phylip_id[0]
	with open(file) as fasta:
		next(fasta)
		full_seq_lines = []
		for line in fasta:
			line1 = line.strip()
			full_seq_lines.append(line1)
	full_seq = ''.join(full_seq_lines)
	seq_list.append(full_seq)
	id_list.append(phylip_id[1:])
	phylip_header2 = str(len(full_seq))



with open('all_genomes.phy', 'w') as phylip:
	phylip_header = phylip_header1 + ' ' + phylip_header2 + '\n'
	phylip.write(phylip_header)
	i = 0
	while i < len(id_list):
		phylip_line = id_list[i] + ' ' + seq_list[i] + '\n'
		phylip.write(phylip_line)
		i += 1