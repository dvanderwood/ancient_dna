#This script take in vcf files in a folder and create consensus fasta file from a reference sequence.

import sys, os, subprocess, glob

'''
usage: vcf2fasta.py reference_fa
'''

#reference_fa = fasta containg the reference sequence for which the vcf was mapped to
#Should be run in the directory containing the vcfs to be used

#*********This script requires bcftools to be installed in the path directory*********#


#Determine the vcf.gz files in the current directories
files = glob.glob("*.vcf.gz")

print 'Working with these files:'
print files

for vcf in files:
	vcf_split = vcf.split('.')
	print 'Creating index for ' + vcf
	args_string = 'bcftools index ' + vcf
	print args_string
	args = str.split(args_string)
	subprocess.call(args)
	print 'Creating fasta for ' + vcf
	args_string2 = 'bcftools consensus -f ' + sys.argv[1] + ' -i ' + vcf +' > ' + vcf_split[0] + '.hg19.21.fa'
	print args_string2
	args2 = str.split(args_string2)
	print args2
	print subprocess.call([args_string2], shell=True) #Can I find a way to get this to work without shell=True since that can be a security vunerability


