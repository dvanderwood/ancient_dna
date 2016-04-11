import sys, os, subprocess, glob, linecache

'''
usage: tmp.py
'''

#reference fasta should also be in the folder and have the file type .fa
#Should be run in the directory containing the vcfs to be used
#common_exomes.txt is an output of vcf_exome_checker.py

files = glob.glob("*.vcf")

print 'Working with these files:'
print files

reference = glob.glob("*.fa")
print 'Working with this reference'
print reference[0]
ref = reference[0]

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

		#Create a string of the entire reference sequence
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
					if len(line_info[3]) == 1: #make sure it isn't a deletion
						if line_info[4] != '.': #check to see if there is any type of variant
							if len(line_info[4]) == 1: #if there is one polymorphism possibility (non insertion), add the variant position to the dictionary
								pos_dict[line_info[1]] = line_info[4]
								#print line_info[1]
								#print line_info[4]
							elif ',' in line_info[4] and len(line_info[4]) == 3: #if there are two polymorphism possibility (and non insertion), add the variant position to the dictionary
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

		#Strip the full sequence down to the positions of the common exomes for which variants we extracted
		#exome_seq_list = []
		#for pos in full_pos_list:
		#	exome_seq_list.append(resu[pos-1])
		#exome_seq = ''.join(exome_seq_list)


		exome_seq = ''.join(resu)
		#print exome_seq
		#print len(exome_seq)


		#write the full modified sequence to the fasta file	
		i = 0
		while i < len(exome_seq):
			vcf_fasta.write(exome_seq[i:i+line_length] + '\n')
			i = i +line_length

		#print len(pos_dict)


#new_fasta_generator(files[0], ref, sys.argv[1])	

#new_fasta_generator_filter(files[0], ref, sys.argv[1])		


for file in files:
	new_fasta_generator(file,ref)
	