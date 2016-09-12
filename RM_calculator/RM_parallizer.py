import subprocess, glob, shutil, os, sys

def rm_parallizer(path, family_size, threads, family_run):
		
	print('\nStarting all instances... Please wait')
	
	current_path = os.path.dirname(os.path.realpath(sys.argv[0]))

	process_dict = {}
	for i in range(1, threads+1):
		newpath = path + 'RM/rm'+ str(i) + '.txt'
		cmd = 'python3 ' + current_path + '/RM_run.py ' + path + ' ' + family_size + ' ' + str(i) + ' ' + str(threads) + ' ' + family_run
		cmd_str = cmd.split(' ')
		print('Running %r in %r\n' % (cmd, newpath) + '\n')
		process_dict[str(i)] = subprocess.Popen(cmd_str)
	############################################
	
	
	###Combine completed progs##################
	
	[process_dict[process].wait() for  process in process_dict.keys()]
	
	print('Completed all instances... Combining files')
	
	rms = glob.glob(path + '/RM/*.txt')
	with open(path + '/RM/rm_all.txt', 'w') as outfile:
	    for infile in rms:
	        shutil.copyfileobj(open(infile), outfile)
	
	############################################
	
	
	###Remove any duplicate combinations########

	#Shouldn't be needed
	
	#lines_seen = set() # holds lines already seen
	#outfile = open(path + '/RM/rm_final.txt', "w")
	#for line in open(path + '/RM/rm_all.txt', "r"):
	#    if line not in lines_seen: # not a duplicate
	#        outfile.write(line)
	#        lines_seen.add(line)
	#outfile.close()