import sys, glob, subprocess, linecache, shutil, os, math, random

###Graph functions
def mean(echantillon):
	size = len(echantillon)
	moyenne = float(sum(echantillon)) / float(size)
	return moyenne


def stat_variance(echantillon):
    n = float(len(echantillon)) # taille
    mq = mean(echantillon)**2
    s = sum([x**2 for x in echantillon])
    variance = s / n - mq
    return variance


def stat_ecart_type(echantillon):
    variance = stat_variance(echantillon)
    ecart_type = math.sqrt(variance)
    return ecart_type

def median(echantillon):
	echantillon.sort()
	size = len(echantillon)
	if len(echantillon) % 2 == 0:
		M= float(echantillon[size // 2 - 1] + echantillon[size // 2]) / 2
	else:
		M= echantillon[size // 2]
	return M

def ninetyfive(echantillon):
	echantillon.sort()
	size = len(echantillon)
	i95 = int(float(size) * 95/100) - 1
	return echantillon[i95]


def five(echantillon):
	echantillon.sort()
	size = len(echantillon)
	i5 = int(float(size) * 5/100) - 1
	return echantillon[i5]

###Fasta List Generator
	#Find all the fasta files in the given directory

def fasta_list_generator(directory):
	fastas1 = glob.glob(directory + '/*.fa')
	fastas2 = glob.glob(directory + '/*.fasta')
	fastas = fastas1 + fastas2
	
	if not fastas:
		print('**** No fasta files present in current directory ****')
		sys.exit()
	
	print('\nCombining these fastas:')
	print(fastas)
	return fastas



###Phylip Creator
	#Combine all the fasta files in a given list into a phylip file and output to a given directory

def phylip_generator(fastas, output_dir):
	phylip_header1 = str(len(fastas))
	
	seq_list = []
	id_list = []
	for file in fastas:
		#phylip_id = file
		phylip_id = linecache.getline(file,1)
		phylip_id = phylip_id.strip('\n').split('.')
		phylip_id = phylip_id[0]
		with open(file) as fasta:
			next(fasta)
			full_seq_lines = []
			for line in fasta:
				line1 = line.strip()
				full_seq_lines.append(line1)
		full_seq = ''.join(full_seq_lines)
		seq_list.append(full_seq)
		id_list.append(phylip_id[1:])
		phylip_header2 = str(len(full_seq))
	
	
	
	with open(output_dir + '/all_genomes.phy', 'w') as phylip:
		phylip_header = phylip_header1 + ' ' + phylip_header2 + '\n'
		phylip.write(phylip_header)
		i = 0
		while i < len(id_list):
			phylip_line = id_list[i] + '\t' + seq_list[i] + '\n'
			phylip.write(phylip_line)
			i += 1
		
###Fasta Concatenater
	#Combine fasta files in a give list into a single concatenate and write to an output directory

def fasta_concat(fastas, output_dir):
	with open(output_dir + '/all_genomes.fa', 'w') as outfile:
	    for infile in fastas:
	        shutil.copyfileobj(open(infile), outfile)




###RAxML distance matrix constructer

def raxml_distance(path, phylip):
	print('\nGenerating distance matrix via RAxML')
	args_string = 'raxmlHPC -f x -p 12345 -s ' + phylip + ' -m GTRGAMMA -n dist -w ' + path
	args = args_string.split()
	subprocess.call(args)
	
	distances = glob.glob(path + "/RAxML_distances.dist")
	if not distances:
		print('\n**** Error in RAxML, RAxML_distances.dist file not created')
		sys.exit()
	
	print('\nRaXML completed')



###Fasta concatenate loader
def fasta_concat_loader(fasta): #Requires a fasta file that is a concatante of many fasta files
	print('\nLoading concatenate fastsa')
	names=[]
	tmp={}
	with open(fasta, 'r') as fasta_file:
		for l in fasta_file:
			if l[0]=='>':
				id = l.strip('\n').strip('>').split('.')[0] #Assumes the fastas have have a period in the name and that the part before it is the essential part
				tmp[id]=[]
				names.append(id)
			else:
				tmp[id].append(l.strip('\n').upper())
		
			
	names.sort()
	
	seq={}
	for id in names:
		seq[id]=''.join(tmp[id])
		tmp[id]=''
		
	print('\nSequences loaded')
	return (seq, names)


###Informative site finder
def info_site_finder(fasta_dic, names, output_dir):  #Requires a dictionary containing names form the fasta headers and the sequence and a list of those fasta headers. fasta_concat_loader produces these variables.
	short={}										 #All the sequences must be the same exact length
	for name in names:
		short[name]=''
	
	i=0
	while i < len(fasta_dic[names[0]]):
		tmp=[]
		for name in names:
			N = fasta_dic[name][i]
			tmp.append(N)
		toto = list(set(tmp))
		if len(toto) > 1:
			#print i,' ',toto
			for name2 in names:
				short[name2]+=fasta_dic[name2][i]
		i+=1
		
		
	print('\nWriting informative site fasta')
	with open(output_dir + '/short.fa','w') as output_file:
		for name in names:
			output_file.write('>' + name + '\n')
			i=0
			while i < len(short[name]):
				output_file.write(short[name][i:i+60] + '\n')
				i+=60
	
	
###Phylogenetic distance loader
def phylo_dist_loader(path): #Requires raxml to be run, such as by the raxml_distance function 
	with open(path + "/RAxML_distances.dist","r") as dist_file:
		dist={}
		for l in dist_file:
			a=l.strip("\n").split("\t")
			sp1,sp2 = a[0].strip(" ").split(" ")[0], a[0].strip(" ").split(" ")[1]
			if sp1 in dist:
				pass
			else:
				dist[sp1] = {}
			if sp2 in dist:
				pass
			else:
				dist[sp2] = {}
			dist[sp1][sp2] = float(a[1])
			dist[sp2][sp1] = float(a[1])
	
	return dist


###Remove identical genomes
def identical_checker(distances, low_cutoff): #Requires the dictionary of distances, the output of phylo_dist_loader
	sub=list(distances.keys())
	i=0
	while i in range(len(sub)):
		name1 = sub[i]
		for name2 in sub:
			if name1 != name2:
				if float(distances[name1][name2]) <= low_cutoff:
					print('\nIdentical Genomes: ', name1," ",name2)
					if name2 in sub:
						sub.remove(name2)
						i= -1
				elif float(distances[name1][name2]) > 1:
					print('**** PROBLEM in one of the below alignments ****')
					print(name1," ",name2)
		i+=1
	
	names= list(sub)
	print('\n', len(sub)," genomes left after identical genomes removed and these genomes are:")
	print(names)
	return names
	

###Create family files, or a list of genome combinations
def family_generator(output_dir, species):
	with open(output_dir + "/families.txt","w") as h:
		familles=[]
		combin={}
		i=4
		while i <= len(species):
			toto=0
			#print(i)
			combin[i] = []
			reservoire=[]
			mifa=i
			j=1
			limit = i**2
			while j <= 1000:
				tmp=[]
				for truc in range(i):
					sp = random.choice(species)
					while sp in tmp:
						sp = random.choice(species)
					tmp.append(sp)
				tmp.sort()
				subset = "-".join(tmp)
				if subset not in combin[i]:
					toto+=1
					print(i,' ',toto)
					combin[i].append(subset)
					familles.append(subset)
					h.write(str(i) + "\t" + subset + "\n")
					j+=1
				elif subset not in reservoire:
					reservoire.append(subset)
					if len(reservoire) == len(combin[i]):
						print('OK')
						break
			i+=1

	###Create small family size file############

	dico={}
	f=open(output_dir + '/families.txt','r')
	h=open(output_dir + '/families100.txt','w')
	for l in f:
		a=l.strip('\n').split('\t')
		nb = int(a[0])
		if nb in dico:
			pass
		else:
			dico[nb] = 0
		if dico[nb] < 100:
			dico[nb] +=1
			h.write(l)

	f.close()
	h.close()


def rm_graph(path):
	dico={}
	liste=[]
	f=open(path + "/RM/rm_all.txt","r")
	for l in f:
		a=l.strip("\n").split("\t")
		subset = a[0]
		b=subset.split("-")
		nb = len(b)
		if 1==1:
			if nb > 3:
				if float(a[2]) > 0:
					rm = float(a[1])/float(a[2])
					if nb in dico:
						dico[nb].append(rm)
					else:
						dico[nb] = [rm]
						liste.append(nb)
	
	f.close()
	
	
	
	
	liste.sort()
	
	h=open(path + "/graph/graph.txt","w")
	h.write("Nb\tMean\tMedian\tSD\tCI05\tCI95\n")
	for nb in liste:
		h.write(str(nb) + "\t" + str(mean(dico[nb])) + "\t" + str(median(dico[nb])) + "\t"  +  str(stat_ecart_type(dico[nb])) + "\t" + str(five(dico[nb])) + "\t" + str(ninetyfive(dico[nb])) + "\n"  )
	
	h.close()

	current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	graph_path = path + '/graph'
	cmd = 'Rscript ' + current_path + '/grapher.R ' + graph_path 
	print('Running ' + 'Rscript ' + current_path + '/grapher.R ' + graph_path + ' ...Please wait')
	cmd_str = cmd.split(' ')
	grapher_process = subprocess.Popen(cmd_str)
	grapher_process.wait()
	print('Script finished... RM graph can be found in the graph directory')



















