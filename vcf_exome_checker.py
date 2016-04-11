#Check the positions of the exomes on a reference genome from a vcf file containing only exomes

import glob

'''
usage: vcf_exome_checker.py
'''

files = glob.glob('*.vcf')

exome_dict = {}
for file in files:
	exome_list = []
	previous_line = 0
	exome_pos = []
	print 'Working on file: ' + file
	with open(file) as vcf:
		for line in vcf:
			if '#CHROM' in line:
				for line in vcf:
					line_info = line.split()
					if previous_line == 0 or float(line_info[1]) == previous_line + 1 or float(line_info[1]) == previous_line:
						exome_pos.append(line_info[1])
						if float(line_info[1]) == previous_line:
							print 'Repeated Position:'
							print line_info[1]
					else:
						exome_out = exome_pos[0] + ':' + exome_pos[-1]
						exome_list.append(exome_out)
						exome_pos = [line_info[1]]
					previous_line = float(line_info[1])
	file_split = file.split('_')
	exome_dict[file_split[1]] = exome_list

most_exomes = []
for key in exome_dict:
	exomes = exome_dict[key]
	filename = key + '_exomes.txt'
	with open(filename, 'w') as exome_output:
		for exome in exomes:
			output_line = exome + '\n'
			exome_output.write(output_line)

	if len(exomes) > len(most_exomes):
		most_exomes = exomes

print 'Max number of Exomes in a genome: ' + str(len(most_exomes))

common_exomes = []
key_list = list(exome_dict.keys())
#print 'Exomes present in all 3 with the exact same positioning: '
for exome in most_exomes:
	i = 0
	commonality_counter = 0
	while i < len(key_list):
		if exome in exome_dict[key_list[i]]:
			commonality_counter +=1
		i += 1
	if commonality_counter == len(key_list):
		#print exome
		common_exomes.append(exome)

with open('common_exomes.txt', 'w') as common_exomes_output:
	for exome in common_exomes:
		output_line = exome + '\n'
		common_exomes_output.write(output_line)
	
alternate_checking_file = key_list[0] + '_exomes.txt'
exome_start_list = []
exome_end_list = []
with open(alternate_checking_file, 'r') as alternate:
	for line in alternate:
		exome = line.split(':')
		start_pos = float(exome[0])
		end_pos = float(exome[1])
		exome_start_list.append(start_pos)
		exome_end_list.append(end_pos)

alternate_counter = 0		
with open(alternate_checking_file, 'r') as alternate:
	for line_check in alternate:
		exome_check = line_check.split(':')
		exome_check_start = float(exome_check[0])
		exome_check_end = float(exome_check[1])
		k = 0
		while k < len(exome_start_list):
			start_pos = exome_start_list[k]
			end_pos = exome_end_list[k]
			#if (start_pos >= exome_check_start and start_pos <= exome_check_end) or (end_pos <= exome_check_end and end_pos >= exome_check_start):
			#	alternate_counter += 1
			if (start_pos > exome_check_start and start_pos < exome_check_end) or (end_pos < exome_check_end and end_pos > exome_check_start):
				alternate_counter += 1
			k += 1
print 'Number of Exomes which overlap for ' + key_list[0] + ': ' + str(alternate_counter)










