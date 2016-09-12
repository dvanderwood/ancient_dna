import glob, sys
from RM_functions import *

def rm_setup(path, working_path, id_cutoff, family_run):	
	###Fasta list generator
	
	fastas = fasta_list_generator(path)
	
	
	###Generate phylip file in the working directory
	
	phylip_generator(fastas, working_path)
	
	
	###Generate fasta concatenate in the working directory
	
	fasta_concat(fastas, working_path)
	
	
	###Pre calculation file loading
		#Error messages shouldn't be needed since the code would fail before this if there were problems
	
	working_phylips = glob.glob(working_path + '/*.phy')
	if not working_phylips:
		working_phylips = glob.glob(working_path + '/*.phylip')
	
	if len(working_phylips) != 1:
		print('**** phylip file either not present, or multiple are present ****')
		sys.exit()
	
	working_phylip = working_phylips[0]
	print('\nWorking with this phylip file: ' + working_phylip)
	
	working_fastas = glob.glob(working_path + '/*.fa')
	if not working_fastas:
		working_fastas = glob.glob(working_path + '/*.fasta')
	
	if len(working_fastas) != 1:
		print('\n**** fasta file either not present, or multiple are present ****')
		sys.exit()
	
	working_fasta = working_fastas[0]
	print('\nWorking with this fasta file: ' + working_fasta)
	
	
	###RAxML distance matrix construction
	
	raxml_distance(working_path, working_phylip)
	
	
	###Load fasta concatenate file
	
	genome_sequences, genome_names = fasta_concat_loader(working_fasta)
	
	
	###Create short.fa, a fasta concatenate containing only informative sites
	
	info_site_finder(genome_sequences, genome_names, working_path)
	
	
	###Load phylogenetic distances
	
	distances = phylo_dist_loader(working_path)
	
	
	###Remove any identical genomes
	
	unique_genome_names = identical_checker(distances, id_cutoff)
	
	
	###Create the sample list and family combinations texts
	
	if family_run == 'run':
		with open(working_path + "/sample.txt","w") as sample_output:
			for name in unique_genome_names:
				sample_output.write(name + "\n")
	
		family_generator(working_path, unique_genome_names)