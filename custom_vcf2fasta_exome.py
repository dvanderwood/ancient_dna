#This script take in vcf files in a folder and create consensus fasta file from a reference sequence. The VCF files this is designed for show all positions and shows 
#reference - alternative and not two haplotypes.

#Filtering parameters taken from here: http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1004790#s4 , Lesecque et Al 2014
#Strictly F3 parameters were used

import sys, os, subprocess, glob, linecache

'''
usage: custom_vcf2fasta_exome.py common_exomes.txt
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


def new_fasta_generator_filter(vcf, reference_seq, common_exomes):
	line_ex= linecache.getline(reference_seq,2) # determine fasta line length of reference to match for the output
	line_ex_stripped = line_ex.strip()
	line_length = len(line_ex_stripped)
 
	vcf_file = open(vcf)
	vcf_file_name_split = vcf.split('.')
	vcf_file_name_1 = '.'.join(vcf_file_name_split[:-1]) + '.fa'
	vcf_file_name = '../all/filtered/' + vcf_file_name_1

	with open(common_exomes, 'r') as com_ex:
		start_pos = []
		end_pos = []
		for line1 in com_ex:
			line = line1.strip()
			ex_pos = line.split(':')
			start_pos.append(float(ex_pos[0]))
			end_pos.append(float(ex_pos[1]))
	print 'Common exomes read'


	#Create a list of all the positions on the chromosome to extract for the common exomes
	full_pos_list = []
	k = 0
	while k < len(start_pos):
		full_pos_list.extend(range(int(start_pos[k]), int(end_pos[k]+1)))
		k += 1
	print 'Exome positions read'

	with open(vcf_file_name, 'w') as vcf_fasta:
		fasta_header = vcf_file_name_split[0].split('_')
		vcf_fasta.write('>' + '.'.join(fasta_header[1:]) + '\n')

		#Create a string of the entire reference sequence
		with open(reference_seq) as ref_seq:
			next(ref_seq)
			full_seq_lines = []
			for line in ref_seq:
				line1 = line.strip()
				full_seq_lines.append(line1)
			full_seq = ''.join(full_seq_lines)
		print 'Refrence sequence read'
	
		#Find SNPs in the vcf, ignoring structural variants. Positions and alternative nucleotides are placed in a dictionary
		pos_dict = {}
		for line in vcf_file:
			if '#CHROM' in line:
				for line in vcf_file:
					tag = 0 #initiate tag variable
					line_info = line.split()
					if int(line_info[1]) in full_pos_list: # Make sure the variant is part of a common exome
						if len(line_info[3]) == 1: #make sure it isn't a deletion
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
									if len(line_info[4]) == 1 and tag == 3: #if there is one polymorphism possibility (non insertion) and the variant sites passes all filters, add the variant position to the dictionary
										pos_dict[line_info[1]] = line_info[4]
										print 'Map20 =' + map20
										print 'dp:'
										print dp
										print 'Counts for Human and Chimp possible paralogs:'
										print ts.count('H')
										print ts.count('P')
										#print line_info[1]
										#print line_info[4]
									elif ',' in line_info[4] and len(line_info[4]) == 3 and tag == 3: #if there are two polymorphism possibility (and non insertion) and the variant sites passes all filters, add the variant position to the dictionary
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
		print 'Full sequence with variants read'

		#Strip the full sequence down to the positions of the common exomes for which variants we extracted
		#exome_seq_list = []
		#for pos in full_pos_list:
		#	exome_seq_list.append(resu[pos-1])
		#exome_seq = ''.join(exome_seq_list)
		
		#Strip the full sequence down to the positions of the common exomes for which variants we extracted
		j = 0
		exome_seq_list = []
		exome_nts = []
		while j < len(start_pos):
			exome_nts = resu[(int(start_pos[j])-1):(int(end_pos[j]))]
			print exome_nts
			exome_seq_list.extend(exome_nts)
			exome_nts = []
			j += 1

		exome_seq = ''.join(exome_seq_list)
		print 'Exome only sequence read'

		#write the full modified sequence to the fasta file	
		print 'Writing exome sequence to fasta file'
		i = 0
		while i < len(exome_seq):
			vcf_fasta.write(exome_seq[i:i+line_length] + '\n')
			i = i +line_length


		



def new_fasta_generator(vcf, reference_seq, common_exomes):
	line_ex= linecache.getline(reference_seq,2) # determine fasta line length of reference to match for the output
	line_ex_stripped = line_ex.strip()
	line_length = len(line_ex_stripped)
 
	vcf_file = open(vcf)
	vcf_file_name_split = vcf.split('.')
	vcf_file_name_1 = '.'.join(vcf_file_name_split[:-1]) + '.fa'
	vcf_file_name = '../all/unfiltered/' + vcf_file_name_1

	with open(common_exomes, 'r') as com_ex:
		start_pos = []
		end_pos = []
		for line1 in com_ex:
			line = line1.strip()
			ex_pos = line.split(':')
			start_pos.append(float(ex_pos[0]))
			end_pos.append(float(ex_pos[1]))
	print 'Common exomes read'

	#Create a list of all the positions on the chromosome to extract for the common exomes
	full_pos_list = []
	k = 0
	while k < len(start_pos):
		full_pos_list.extend(range(int(start_pos[k]), int(end_pos[k]+1)))
		k += 1
	print 'Exome positions read'
	

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
		print 'Refrence sequence read'

	
		#Find SNPs in the vcf, ignoring structural variants. Positions and alternative nucleotides are placed in a dictionary
		pos_dict = {}
		for line in vcf_file:
			if '#CHROM' in line:
				for line in vcf_file:
					line_info = line.split()
					if int(line_info[1]) in full_pos_list: # Make sure the variant is part of the exome
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
		print 'Full sequence with variants read'

		#Strip the full sequence down to the positions of the common exomes for which variants we extracted
		#exome_seq_list = []
		#for pos in full_pos_list:
		#	exome_seq_list.append(resu[pos-1])
		#exome_seq = ''.join(exome_seq_list)

		#Strip the full sequence down to the positions of the common exomes for which variants we extracted
		j = 0
		exome_seq_list = []
		exome_nts = []
		while j < len(start_pos):
			exome_nts = resu[(int(start_pos[j])-1):(int(end_pos[j]))]
			print exome_nts
			exome_seq_list.extend(exome_nts)
			exome_nts = []
			j += 1

		exome_seq = ''.join(exome_seq_list)
		print 'Exome only sequence read'
		#print exome_seq
		#print len(exome_seq)


		#write the full modified sequence to the fasta file	
		print 'Writing exome sequence to fasta file'
		i = 0
		while i < len(exome_seq):
			vcf_fasta.write(exome_seq[i:i+line_length] + '\n')
			i = i +line_length

		#print len(pos_dict)


#new_fasta_generator(files[0], ref, sys.argv[1])	

#new_fasta_generator_filter(files[0], ref, sys.argv[1])		


for file in files:
	print 'Working on unfiltered: ' + file
	new_fasta_generator(file,ref, sys.argv[1])
	print 'Working on filtered: ' + file
	new_fasta_generator_filter(file,ref, sys.argv[1])	





