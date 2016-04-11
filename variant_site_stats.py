'''
usage: variant_site_stats.py path
'''

#path = absolute path to the folder containing the outputs from the prog script
		#i.e. ~/path/to/directory
		#type pwd into your terminal when in the wanted directory to determine this
		# use . to indicate current directory

import sys, os

###System argument clean up#################

path = sys.argv[1]

if  path == '.':
	path = os.getcwd()

############################################


###Homoplasy File Reading###################

chain_id_order = []
position_counter = 0
with open(path + '/homoplasy_order.txt', 'r') as genome_ordering:
	for line in genome_ordering:
		chain_id = line.strip('\n')
		chain_id_order.append(chain_id)
		if not chain_id.startswith('HG') and not chain_id.startswith('NA'): #The 1000genome ids all begin with either HG or NA
			ancient_position = position_counter #record the position of the ancient genome in the variant chain, which is the final column of the homoplasy.txt file. This also assumes only one ancient genome per set
		position_counter += 1

print '\nAncient DNA located at chain position:', ancient_position

if ancient_position is None:
	print '\nNo Ancient DNA identified, exiting script'
	sys.exit()

############################################


###Determine number of informative sites####

sample_seq = ''
with open(path + '/short.fa', 'r') as informative_sites_file:
	for line in informative_sites_file:
		if line[0] == '>':
			pass
			for line in informative_sites_file:
				if line[0] == '>':
					break
				sample_seq = sample_seq + line.strip('\n')
		break

informative_sites = len(sample_seq)
print '\nNumber of informative sites:', informative_sites

############################################


###Determine 'full' genome size#############   For the test case this is the length of the used exomes for the specific chromosome

all_seq = ''
with open(path + '/all_genomes.fa', 'r') as all_sites_file:
	for line in all_sites_file:
		if line[0] == '>':
			pass
			for line in all_sites_file:
				if line[0] == '>':
					break
				all_seq = all_seq + line.strip('\n')
		break

all_sites = len(all_seq)
print '\nNumber of total sites:', all_sites

############################################


###Load homoplasy data######################

#Initate lists for data conainted in homoplasy.txt
position = []
recombination = []
mutation = []
TYPE = []
singleton = []
chain = []

with open(path + '/homoplasy.txt', 'r') as homoplasy_info:
	next(homoplasy_info)
	for line in homoplasy_info:
		info = line.strip('\n').split('\t')
		position.append(int(info[0]))
		recombination.append(int(info[1]))
		mutation.append(int(info[2]))
		TYPE.append(int(info[3]))
		singleton.append(int(info[4][2]))
		chain.append(info[5])

############################################


###Find R sites with ancient variant########

i = 0
ancient_recombs = []
while i < len(position):
	if recombination[i] == 1 and chain[i][ancient_position] == '1':
		ancient_recombs.append(i)
	i += 1

print '\nNumber of recombination sites in which the ancient DNA has a variant:', len(ancient_recombs)

############################################


###Write output files#######################

with open(path + '/homoplasy_stats.txt', 'w') as stats_file:
	stats_file.write('Ancient_R_Sites\tInformative_Sites\tTotal_Sites\n')
	stats_file.write(str(len(ancient_recombs)) + '\t' + str(informative_sites) + '\t' + str(all_sites) + '\n')

with open(path + '/homoplasy_ancient_r_positions.txt', 'w') as position_file:
	for pos in ancient_recombs:
		position_file.write(str(position[pos]) + '\n')

############################################





























