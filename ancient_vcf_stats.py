#This script takes in the VCFs of ancient DNA (neandertal and denisova) and checks how many variant sites there are total, and how many of those have map20 scores of 1 and are not low qual(based on
#the low qual filter already applied).

import sys, os, subprocess, glob

'''
usage: ancient_vcf_stats.py
'''

files = glob.glob('*.vcf')

with open('ancient_vcf_stats.txt', 'w') as output:
	output.write('file number_of_variants number_of_low_quals number_with_map20_1\n')

file_dict = {}
i = 0
for file in files:
	print 'Working on file:' + file
	variant_counter = 0
	map20_counter = 0
	low_qual_counter = 0
	pos_list = []
	output_info = []
	with open(file) as ancient_vcf:
		for line in ancient_vcf:
			if '#CHROM' in line:
				for line in ancient_vcf:
					line_info = line.split()
					if line_info[1] not in pos_list:
						if line_info[4] != '.':
							if len(line_info[4]) == 1 or (',' in line_info[4] and line_info[4] == 3):
								print line_info[1]
								pos_list.append(line_info[1])
								variant_counter += 1
								if line_info[6] == 'LowQual':
									low_qual_counter += 1
								if 'Map20=1' in line_info[7]:
									map20_counter += 1
								#id_info = line_info[7]
								#id_info_split = id_info.split(';')
								#if any('Map20=1' in s for s in id_info_split):
								#	print id_info_split
								#	map20_counter += 1
	output_info.append(variant_counter)
	output_info.append(low_qual_counter)
	output_info.append(map20_counter)
	file_dict[file] = output_info

with open('ancient_vcf_stats.txt', 'w') as output:
	output.write('file number_of_variants number_of_low_quals number_with_map20_1\n')
	for key in file_dict:
		info_text = file_dict[key]
		info_text_str = ''
		for info in info_text:
			info_text_str = info_text_str + ' ' + str(info)
		file_line = key + info_text_str + '\n'
		print file_line
		output.write(file_line)





