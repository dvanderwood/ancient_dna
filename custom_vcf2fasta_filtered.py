#This script take in vcf files in a folder and create consensus fasta file from a reference sequence. The VCF files this is designed for show all positions and shows 
#reference - alternative and not two haplotypes.

#Filtering parameters taken from here: http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004790#s4 , Lesecque et Al 2014
#Strictly F3 parameters were used

import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta.py
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


#Function to determine the number of initial Ns in the reference fasta
def initial_n_counter(reference_seq):
	init_n_counter = 0
	with open(reference_seq) as ref_seq:
		next(ref_seq)
		for line in ref_seq:
			line1 = line.strip()
			for base in line1:
				if base == 'N':
					init_n_counter = init_n_counter + 1
				else:
					return(init_n_counter)


number_of_Ns = initial_n_counter(reference[0])

def vcf_initial_position(vcf_files):
	with open(vcf_files[0]) as first_vcf:
		for line in first_vcf:
			if '#CHROM' in line:
				for line in first_vcf:
					line_info = line.split()
					return(line_info[1])

initial_nucleotide_vcf = int(vcf_initial_position(files))

if number_of_Ns == (initial_nucleotide_vcf - 1):
	print '*****Initial Ns match, script may proceed*****'
else:
	sys.exit()


print '*****Checking if first vcf file has any gaps*****'
positions = []
with open(files[0]) as f:
	for line in f:
			if '#CHROM' in line:
				for line in f:
					line_info = line.split()
					positions.append(int(line_info[1]))


					
positions_len = len(positions)
seq_id = positions[-1] - positions[0]
if positions_len != seq_id:
	print "*****Assuming positions in the vcf are sequentially listed, there are gaps in the sequence*****"
else:
	print "*****There are no gaps in the vcf sequence*****"

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
					tag = 0 #initiate tag variable
					line_info = line.split()
					if line_info[1] not in pos_dict: #check if it is a new position
						if line_info[4] != '.': #check to see if there is any type of variant
							if line_info[6] == '.': #filter out LowQual and Sys Error
								id_info = line_info[7].split(';') #split id sectio into a list
								for id_type  in id_info:
									if id_type.startswith('Map20='): #confirm Map20 is equal to 1 to avoid mapping errors
										map20 = id_type.strip('Map20=')
										if map20 == '1':
											tag += 1
									elif id_type.startswith('TS='): #confirm the EPO alginment block has only one human and one chimp sequence, to avoid paralogies
										ts = id_type.strip('TS=')
										if ts.count('H') == 1 or ts.count('P') == 1:
											tag += 1
									elif id_type.startswith('DP='): #confirm the depth is within 16 and 46 to avoid unreliable and repeated/duplciated regions
										dp = float(id_type.strip('DP='))
										if dp >= 16 and dp <= 46:	
											tag += 1
								if len(line_info[4]) == 1 and tag == 3:
									pos_dict[line_info[1]] = line_info[4]
									print 'Map20 =' + map20
									print 'dp:'
									print dp
									print 'Counts for H and P:'
									print ts.count('H')
									print ts.count('P')
									#print line_info[1]
									#print line_info[4]
								elif ',' in line_info[4] and len(line_info[4]) == 3 and tag == 3:
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



							#if line_info[6] == '.': #filter out LowQual and Sys Error
							#	bulk_info = line_info[7].split(';')
							#	if any('Map20=1' in s for s in bulk_info): #Make sure Map20 score is 1
							#		for s in bulk_info:
							#			if s.startswith('DP='):
							#				depth = s.strip('DP=')
							#				if depth >= 16 and depth <= 46: #Make sure coverage is between 16 and 46
							#					print depth[1]
							#					if s.startswith('TS='): #Assumes TS is always after DP in the info section
							#						ts = s.split('=')
#
							#							if len(line_info[4]) == 1:
							#								pos_dict[line_info[1]] = line_info[4]
							#								#print line_info[1]
							#								#print line_info[4]
							#							elif ',' in line_info[4] and len(line_info[4]) == 3:
							#								if 'a'  in line_info[4].lower() and 'g' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'R'
							#									#print line_info[1]
							#									#print 'R'
							#								if 'c' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'Y'
							#									#print line_info[1]
							#									#print 'Y'
							#								if 'g' in line_info[4].lower() and 'c' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'S'
							#									#print line_info[1]
							#									#print 'S'
							#								if 'a' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'W'
							#									#print line_info[1]
							#									#print 'W'
							#								if 'g' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'K'
							#									#print line_info[1]
							#									#print 'K'
							#								if 'a' in line_info[4].lower() and 'c' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'M'
							#									#print line_info[1]
							#									#print 'M'
							#								if 'c' in line_info[4].lower() and 'g' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'B'
							#									#print line_info[1]
							#									#print 'B'
							#								if 'a' in line_info[4].lower() and 'g' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'D'
							#									#print line_info[1]
							#									#print 'D'
							#								if 'a' in line_info[4].lower() and 'c' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'H'
							#									#print line_info[1]
							#									#print 'H'
							#								if 'a' in line_info[4].lower() and 'c' in line_info[4].lower() and 'g' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'V'
							#									#print line_info[1]
							#									#print 'V'
							#								if 'a' in line_info[4].lower() and 'g' in line_info[4].lower() and 'c' in line_info[4].lower() and 't' in line_info[4].lower():
							#									pos_dict[line_info[1]] = 'N'
							#									#print line_info[1]
							#									#print 'N'
			
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
		#or pos in pos_dict:
			#full_seq_list = list(full_seq)
			#full_seq_list[int(pos)] = pos_dict[pos]
		#ull_seq_mod = ''.join(full_seq_list)



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











