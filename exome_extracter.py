#Extract exomes out of a fasta of the entire chromosome

import sys, os, subprocess, glob, linecache, numpy

'''
usage: exome_extracter.py common_exomes.txt
'''

#Should be run in the directory containing the fas to be used
#common_exomes.txt is an output of vcf_exome_checker.py


files = glob.glob("*.fa")

#create output diretory
if not os.path.exists('exomes'):
    os.makedirs('exomes')

common_exomes = sys.argv[1]

with open(common_exomes, 'r') as com_ex:
	start_pos = []
	end_pos = []
	for line1 in com_ex:
		line = line1.strip()
		ex_pos = line.split(':')
		start_pos.append(float(ex_pos[0]))
		end_pos.append(float(ex_pos[1]))


#Create a list of all the positions on the chromosome to extract for the common exomes
full_pos_list = []
k = 0
while k < len(start_pos):
	full_pos_list.extend(range(int(start_pos[k]), int(end_pos[k]+1)))
	k += 1

#Subtract 1 from every position, since python begins indexing at 0 not 1
full_pos_array = numpy.array(full_pos_list)
full_pos_array = full_pos_array - 1
full_pos_list = list(full_pos_array)



def exome_extracter(file, pos_list):
	line_ex= linecache.getline(file,2) # determine fasta line length
	line_ex_stripped = line_ex.strip()
	line_length = len(line_ex_stripped)

	with open(file, 'r') as fasta:

		#Read Current fasta
		next(fasta)
		full_seq_lines = []
		for line in fasta:
			line1 = line.strip()
			full_seq_lines.append(line1)
		full_seq = ''.join(full_seq_lines)
		
	full_seq = list(full_seq)

	#Extract only the positions from the exomes
	exome_seq = []
	for index in pos_list:
		exome_seq.append(full_seq[index])
	exome_seq = ''.join(exome_seq)


	file_split = file.split('.')
	new_file = 'exomes/' + file_split[0] + '.' + file_split[1] + '.exomes.fa' 
	new_filename = 'exomes/exomes_' + file
	with open(new_filename, 'w') as new_fasta:
		new_fasta.write(linecache.getline(file,1))
		#write the full modified sequence to the fasta file	
		i = 0
		while i < len(exome_seq):
			new_fasta.write(exome_seq[i:i+line_length] + '\n')
			i = i +line_length




#exome_extracter(files[0], full_pos_list)

for file in files:
	exome_extracter(file, full_pos_list)




