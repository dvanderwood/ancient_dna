#Combine multiple RM by genome graphs into one pdf and title each. For each combination, all chromosomal graphs will be grouped.

#File structure is assumed to be, for example: current_directory/chromosome/combination/graph where chromosome is now referred to as directory and combination as sub directory

import os, Image

'''
usage: graph_combiner.py
'''

#Get the current working diretory path
path = os.getcwd() 


#Get all the subdirectories in the working directory
directories = os.listdir(path) 

print 'Working with these directories:'
print directories


#Get all possible sub directory types, and add them to a new variable
sub_directories = []
for dirs in directories:
	temp_subs = os.listdir(path + '/' + dirs)
	for sub in temp_subs:
		if sub == '.DS_Store':
			pass
		elif sub not in sub_directories:
			sub_directories.append(sub)


print '\nWorking with these sub_directories:'
print sub_directories


im = Image.open(path + '/' + directories[14] + '/' + sub_directories[0] + '/Graph.pdf')
im.show()


#Create files for each subdirectory type
