#This script take in vcf files in a folder and create consensus fasta file from a reference sequence.

import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta.py
'''

#reference fasta should also be in the folder
#Should be run in the directory containing the vcfs to be used

files = glob.glob("*.vcf")

print 'Working with these files:'
print files

reference = glob.glob("*.fa" or "*.fasta")
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
					line_info = line.split()
					if line_info[1] not in pos_dict:
						if line_info[4] != '.':
							if len(line_info[4]) == 1:
								pos_dict[line_info[1]] = line_info[4]
								#print line_info[1]
								#print line_info[4]
							elif ',' in line_info[4]:
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
		#or pos in pos_dict:
			#full_seq_list = list(full_seq)
			#full_seq_list[int(pos)] = pos_dict[pos]
		#ull_seq_mod = ''.join(full_seq_list)

		#write the full modified sequence to the fasta file	
		i = 0
		while i < len(resu):
			vcf_fasta.write(resu[i:i+line_length] + '\n')
			i = i +line_length


		

#new_fasta_generator(files[0],reference[0])		


for file in files:
	new_fasta_generator(file,reference[0])











