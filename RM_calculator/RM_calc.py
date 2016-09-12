#This script should be run in a folder containing identical length fastas. 

###REQUIREMENTS###

	#Modules: sys, glob, subprocess, linecache, shutil, math, random, argparse
	#fasta files (.fa or .fasta) in the current directory
	#Fasta header names should contain only the essential genome name or should be have the essential info before a period	

'''
usage: RM_calc.py 
'''

import sys, subprocess, os, argparse

from RM_functions import *
from RM_classes import *
from RM_setup import *
from RM_parallizer import *


###Create arguement parser

parser = argparse.ArgumentParser(description='Create RM graph and polymorphic stats of given genomes')

parser.add_argument('-p', '--path', type = str, default = os.getcwd(), help = 'Path where the genome to be run are located')

parser.add_argument('-f', '--family_run' , type = str, default = True, 
	help = 'New family combinations should not be compiled and thus a path to the ones to be used must be supplied. If this is selected, no identical genomes can be be present in the sample set')

parser.add_argument('-l', '--family_size', action = 'store_true', default = False, help = 'Denotes that the large families of genomes should be run. This uses more combinations but results in a longer run time.')

parser.add_argument('-t', '--threads', type = int, default = 1, help = 'The number of threads to be used')

parser.add_argument('-c', '--cutoff', type = float, default = 0.00005, help = 'The cutoff to decide if two genomes are identical')

parser.add_argument('-s', '--skip', action = 'store_true', default = False, help = 'Skip to RM calculation if the working directory has already been prepared')

parser.add_argument('-r', '--rm_hold', action = 'store_true', default = False, help = 'Hold off on RM calculations and only run the set up')

parser.add_argument('-g', '--grapher', action = 'store_true', default = False, help = 'Only perform graphing on already completed RM calculations')

parser.add_argument('-o', '--homoplasy', action = 'store_true', default = False, help = 'Run homoplasy stats, no other processes will be run but the working directory must be completed')

args = parser.parse_args()


###Arguement testing space

#print('path: ',getattr(args, 'path'))
#print('family_run: ',getattr(args, 'family_run'))
#print('family_size: ',getattr(args, 'family_size'))
#print('threads: ',getattr(args, 'threads'))
#print('skip: ',getattr(args, 'skip'))
#print('rm_hold: ',getattr(args, 'rm_hold'))


###Arguement clean-up

path = getattr(args, 'path')

if getattr(args, 'family_run') == True:
	family_run = 'run'
else:
	family_run = getattr(args, 'family_run')

if getattr(args, 'family_size') == False:
	family_size = 'small'
elif getattr(args, 'family_size') == True:
	family_size = 'large'

id_cutoff = getattr(args, 'cutoff')

threads = getattr(args, 'threads')

skip = getattr(args, 'skip')

rm_hold = getattr(args, 'rm_hold')

grapher = getattr(args, 'grapher')

homoplasy = getattr(args, 'homoplasy')


###Only graphing
if grapher == True:
	print('\nOnly running graphing on already completed RM calculations.')
	rm_graph()
	sys.exit()


###Homoplasy info running
if homoplasy == True:
	if not os.path.exists(path + '/homoplasy'):
		os.makedirs('homoplasy')

	current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	cmd = 'python3 ' + current_path + '/variant_site_searcher.py ' + path 
	cmd_str = cmd.split(' ')
	print('Running %r in %r\n' % (cmd, path) + '\n')
	homoplasy_finder = subprocess.Popen(cmd_str)
	homoplasy_finder.wait()
	cmd = 'python3 ' + current_path + '/variant_site_stats.py ' + path 
	cmd_str = cmd.split(' ')
	print('Running %r in %r\n' % (cmd, path) + '\n')
	homoplasy_stats = subprocess.Popen(cmd_str)
	homoplasy_stats.wait()



	sys.exit()

###Arguement Checker

print('\nPath to fastas of same length: ', path)
if family_run == 'run':
	print('Generating new families of genomes (new combinations of genomes)')
else:
	print('Location of family texts to be used: ', family_run)

if family_size == 'small':
	print('Using small families of genomes')
elif family_size == 'large':
	print('Using large families of genomes')

print('Using ', id_cutoff, ' as the cutoff for identical genomes')

print('Using ', threads, ' threads')

if skip == False:
	print('Preparing working directory')
elif skip == True:
	print('Skipping data setup, the working directory should be already prepared in the given path')

if rm_hold == False:
	print('Running RM calculations')
elif rm_hold == True:
	print('Holding off on running RM calculations')


###Create file structure
if not os.path.exists(path + '/working'):
    os.makedirs('working')

working_path = path + '/working'

if not os.path.exists(path + '/RM'):
    os.makedirs('RM')

if not os.path.exists(path + '/graph'):
    os.makedirs('graph')


###Run setup

if skip == False:
	print('\nRunning data setup...')
	rm_setup(path, working_path, id_cutoff, family_run)


###Run RM calculations

if rm_hold == False:
	print('\nRunning RM calculations...')
	rm_parallizer(path, family_size, threads, family_run)


if grapher == False:
	rm_graph(path)












