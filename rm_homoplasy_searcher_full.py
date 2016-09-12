#This script should be run in a folder containing identical length fastas. 

###REQUIREMENTS###

	#Modules: sys, glob, subprocess, linecache, shutil
	#fasta files (.fa or .fasta) in the current directory
	

'''
usage: rm_homoplasy_searcher_full.py 
'''

import sys, glob, subprocess, linecache, shutil, os, math, argparse


###Create arguement parser

parser = argparse.ArgumentParser(description='Create RM graph and polymorphic stats of given genomes')

parser.add_argument('-p', '--path', type = str, default = os.getcwd(), help = 'path where the genome to be run are located')

parser.add_argument('-f', '--family_run' , type = str, default = 'TRUE', help = 'New family combinations should not be compiled and thus a path to the ones to be used must be supplied')

parser.add_argument('-l', '--family_size', action = 'store_true', default = 'FALSE', help = 'Denotes that the large families of genomes should be run')

parser.add_argument('-t', '--threads', type = int, default = 1, help = 'The number of threads to be used')

args = parser.parse_args()


###Arguement testing space

#print(getattr(args, 'path'))
#print(getattr(args, 'family_run'))
#print(getattr(args, 'family_size'))
#print(getattr(args, 'threads'))


###Arguement clean-up

path = getattr(args, 'path')

if getattr(args, 'family_run') == 'TRUE':
	family_run = 'run'
else:
	family_run = getattr(args, 'family_run')

if getattr(args, 'family_run') == 'FALSE':
	family_size = 'small'
elif getattr(args, 'family_run') == 'TRUE':
	family_size = 'large'

threads = getattr(args, 'threads')


###Fasta list generator

fastas = fasta_list_generator(path)



