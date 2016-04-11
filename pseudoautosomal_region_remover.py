#This script removes any exomes from a fasta file containing only exomes which fall in the pseudoautosomal region of the X chromosome.

import sys, os, subprocess, glob, linecache

'''
usage: pseudoautosomal_region_remover.py common_exomes.txt
'''

#reference fasta should also be in the folder and have the file type .fa
#Should be run in the directory containing the vcfs to be used
#common_exomes.txt is an output of vcf_exome_checker.py

#create output diretory
if not os.path.exists('par_removed'):
    os.makedirs('par_removed')

files = glob.glob("*.fa")

print 'Working with these files:'
print files

common_exomes = sys.argv[1]


#The start and ending positions of the pseudoautosomal regions at both the beginning and the end of the X chromosome for hg19.
pseudo_begin_start = 60001
pseudo_begin_end = 2699520
pseudo_end_start = 154931044
pseudo_end_end = 155270560

with open(common_exomes, 'r') as com_ex:
	begin_start_pos = []
	begin_end_pos = []
	end_start_pos = []
	end_end_pos = []
	for line1 in com_ex:
		line = line1.strip()
		ex_pos = line.split(':')
		if float(ex_pos[0]) > pseudo_begin_start and float(ex_pos[1]) < pseudo_begin_end:
			begin_start_pos.append(float(ex_pos[0]))
			begin_end_pos.append(float(ex_pos[1]))
		if float(ex_pos[0]) > pseudo_end_start and float(ex_pos[1]) < pseudo_end_end:
			end_start_pos.append(float(ex_pos[0]))
			end_end_pos.append(float(ex_pos[1]))

i = 0
begin_removal = 0
while i < len(begin_start_pos):
	begin_removal += len(range(int(begin_start_pos[i]),int(begin_end_pos[i]+1)))
	i += 1


j = 0
end_removal = 0
while j < len(end_start_pos):
	end_removal += len(range(int(end_start_pos[j]),int(end_end_pos[j]+1)))
	j += 1

for file in files:
	fasta_header = linecache.getline(file,1)

	line_ex= linecache.getline(file,2) # determine fasta line length
	line_ex_stripped = line_ex.strip()
	line_length = len(line_ex_stripped)

	with open(file) as fasta:
			next(fasta)
			full_seq_lines = []
			for line in fasta:
				line1 = line.strip()
				full_seq_lines.append(line1)
			full_seq = ''.join(full_seq_lines)

	full_seq_list = list(full_seq)

	out_seq_list = full_seq_list[begin_removal:-end_removal]
	out_seq = ''.join(out_seq_list)


	#write the stripped down sequence to a new fasta file
	new_file = 'par_removed/' + file
	with open(new_file, 'w') as new_fasta:
		new_fasta.write(fasta_header)
		i = 0
		while i < len(out_seq):
			new_fasta.write(out_seq[i:i+line_length] + '\n')
			i = i +line_length

		















