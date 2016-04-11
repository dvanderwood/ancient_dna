'''
usage: variant_site_comparer.py path
'''

#path = absolute path to the folder containing the prog script
		#i.e. ~/path/to/directory
		#type pwd into your terminal when in the wanted directory to determine this
		# use . to indicate current directory

import sys, os, linecache

###System argument clean up#################

path = sys.argv[1]

if  path == '.':
	path = os.getcwd()

############################################


#Get all the subdirectories in the working directory
directories = filter(os.path.isdir, os.listdir(path))

print 'Working with these directories:'
print directories


#Get all possible sub directory types, and add them to a new variable
sub_directories = []
for dirs in directories:
	temp_path = path + '/' + dirs + '/combos'
	temp_subs = os.listdir(temp_path)
	for sub in temp_subs:
		if sub == '.DS_Store':
			pass
		elif sub not in sub_directories:
			sub_directories.append(sub)


print '\nWorking with these sub_directories:'
print sub_directories


#Initiate output file and erase a previous one
try:
    os.remove(path + '/all_homoplasy_stats.txt')
except OSError:
    pass

f = open(path + '/all_homoplasy_stats.txt', 'w')
f.write('Chromosome\tSample_Group\tAncient_R_Sites\tInformative_Sites\tTotal_Sites\n')
f.close()


#Load homoplasy stat data from completed homoplasy_stats.txt files
for chromosome in directories:
	for sample_group in sub_directories:
		sub_path = path + '/' + chromosome + '/combos/' + sample_group
		if os.path.exists(sub_path + '/working/homoplasy_stats.txt'):
			print '\nLoading data for: ' + chromosome + ' and sample group: ' + sample_group + '\n'
			sample_info = linecache.getline(sub_path + '/working/homoplasy_stats.txt',2)
			sample_info_output = chromosome + '\t' + sample_group + '\t' + sample_info
			with open(path + '/all_homoplasy_stats.txt', 'a') as output_file:
				output_file.write(sample_info_output)

