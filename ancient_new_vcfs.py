#This script takes in the VCFs of ancient DNA made by mpileup and samtools (neandertal and denisova) and checks how many variant sites there are total.

import sys, os, subprocess, glob

'''
usage: ancient_vcf_stats.py
'''

files = glob.glob('*.vcf')

#with open('ancient_vcf_stats.txt', 'w') as output:
#	output.write('file number_of_variants number_of_low_quals number_with_map20_1\n')

file_dict = {}
i = 0
for file in files:
	print 'Working on file:' + file
	variant_counter = 0
	star_counter = 0
	dp_counter = 0
	no_star_counter = 0
	good_no_star_counter = 0
	pos_list = []
	output_info = []
	with open(file) as ancient_vcf:
		for line in ancient_vcf:
			if '#CHROM' in line:
				for line in ancient_vcf:
					line_info = line.split()
					if line_info[1] not in pos_list:
						if ('a' in line_info[4].lower() or 't' in line_info[4].lower() or 'c' in line_info[4].lower() or 'g' in line_info[4].lower()):
							pos_list.append(line_info[1])
							variant_counter += 1
							id_info = line_info[7]
							id_info_split = id_info.split(';')
							for id_sub in id_info_split:
								if id_sub.startswith('DP='):
									dp = id_sub.strip('DP=')
									if float(dp) >= 16 and float(dp) <= 46:
										dp_counter += 1
										print float(dp)
										print line_info[1]
										if '*' not in line_info[4]:
											good_no_star_counter += 1

						if '*' not in line_info[4]:
							no_star_counter += 1


								
	output_info.append(variant_counter)
	output_info.append(dp_counter)
	output_info.append(no_star_counter)
	file_dict[file] = output_info

with open('ancient_vcf_stats.txt', 'w') as output:
	output.write('file number_of_variants number_of_high_dps number_with_no_stars\n')
	for key in file_dict:
		info_text = file_dict[key]
		info_text_str = ''
		for info in info_text:
			info_text_str = info_text_str + ' ' + str(info)
		file_line = key + info_text_str + '\n'
		print file_line
		output.write(file_line)

print 'Good depth number'
print dp_counter
print 'No star in good depth'
print good_no_star_counter
print 'No star at all'
print no_star_counter
print 'total variants with *'
print variant_counter



