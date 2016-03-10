#This script take in vcf files in a folder and create consensus fasta file from a reference sequence.

import sys, os, subprocess, glob, linecache, random

'''
usage: custom_vcf2fasta_standard_vcf.py
'''

#reference fasta should also be in the folder and have the file type .fa
#Should be run in the directory containing the vcfs to be used

files = glob.glob("*.vcf")

print 'Working with these files:'
print files

reference = glob.glob("*.fa")
print 'Working with this reference'
print reference[0]

#create output diretory
if not os.path.exists('output'):
    os.makedirs('output')

def new_fasta_generator(vcf, reference_seq):
	line_ex= linecache.getline(reference_seq,2) # determine fasta line length of reference to match for the output
	line_ex_stripped = line_ex.strip()
	line_length = len(line_ex_stripped)
 
	vcf_file = open(vcf)
	vcf_file_name_split = vcf.split('.')
	vcf_file_name_1 = '.'.join(vcf_file_name_split[:-1]) + '.fa'
	vcf_file_name = 'output/' + vcf_file_name_1

	with open(vcf_file_name, 'w') as vcf_fasta:
		vcf_fasta.write('>' + '.'.join(vcf_file_name_split[:-1]) + '\n')
		with open(reference_seq) as ref_seq:
			next(ref_seq)
			full_seq_lines = []
			for line in ref_seq:
				line1 = line.strip()
				full_seq_lines.append(line1)
			full_seq = ''.join(full_seq_lines)

		#Find SNPs in the vcf, ignoring structural variants. Positions and alternative nucleotides are placed in a dictionary
		pos_dict = {}
		for line in vcf_file:
			if '#CHROM' in line:
				for line in vcf_file:
					line_info = line.split()
					rand_int = random.randint(1,2)
					if line_info[9] == '1|1' or (line_info[9] == '1|0' and rand_int == 1) or (line_info[9] == '0|1' and rand_int == 1):
						if line_info[1] not in pos_dict: #never repeat a position
							if len(line_info[3]) == 1: 
								if line_info[4] != '.': #check to make there is an alternative, should always be the case for this style of vcf
									if len(line_info[4]) == 1: #make sure it is not a structural variance
										pos_dict[line_info[1]] = line_info[4]
										#print line_info[1]
										#print line_info[4]
									elif (',' in line_info[4] and len(line_info[4]) == 3):
										if 'a'  in line_info[4].lower() and 'g' in line_info[4].lower():
											pos_dict[line_info[1]] = 'R'
											#print line_info[1]
											#print 'R'
										if 'c' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'Y'
											#print line_info[1]
											#print 'Y'
										if 'g' in line_info[4].lower() and 'c' in line_info[4].lower():
											pos_dict[line_info[1]] = 'S'
											#print line_info[1]
											#print 'S'
										if 'a' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'W'
											#print line_info[1]
											#print 'W'
										if 'g' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'K'
											#print line_info[1]
											#print 'K'
										if 'a' in line_info[4].lower() and 'c' in line_info[4].lower():
											pos_dict[line_info[1]] = 'M'
											#print line_info[1]
											#print 'M'
										if 'c' in line_info[4].lower() and 'g' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'B'
											#print line_info[1]
											#print 'B'
										if 'a' in line_info[4].lower() and 'g' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'D'
											#print line_info[1]
											#print 'D'
										if 'a' in line_info[4].lower() and 'c' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'H'
											#print line_info[1]
											#print 'H'
										if 'a' in line_info[4].lower() and 'c' in line_info[4].lower() and 'g' in line_info[4].lower():
											pos_dict[line_info[1]] = 'V'
											#print line_info[1]
											#print 'V'
										if 'a' in line_info[4].lower() and 'g' in line_info[4].lower() and 'c' in line_info[4].lower() and 't' in line_info[4].lower():
											pos_dict[line_info[1]] = 'N'
											#print line_info[1]
											#print 'N'

		i=0
		resu=[]
		while i < len(full_seq):
			if pos_dict.has_key(str(i+1)):
				resu.append(pos_dict[str(i+1)])
				print i+1,' ',pos_dict[str(i+1)]
			else:
				resu.append(full_seq[i])
			i+=1
		resu = ''.join(resu)
		




		#write the full modified sequence to the fasta file	
		i = 0
		while i < len(resu):
			vcf_fasta.write(resu[i:i+line_length] + '\n')
			i = i +line_length


	###*************CHECK IF WORKING******************###
	#Create a file of every position and its variant that passed filtering
	pos_dict_name_1 = '.'.join(vcf_file_name_split[:-1]) + '.txt'
	pos_dict_name = 'output/' + pos_dict_name_1
	with open(pos_dict_name, 'w') as pos_file:
		pos_file.write('position variant\n')
		for key in pos_dict:
			pos_line = key + ' ' + pos_dict[key] + '\n'
			pos_file.write(pos_line)

		

#new_fasta_generator(files[0],reference[0])		


for file in files:
	new_fasta_generator(file,reference[0])


#k = 0
#while k < 100:
#	new_fasta_generator(files[k],reference[0])
#	k += 1





