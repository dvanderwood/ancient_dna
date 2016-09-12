'''
usage: prog_parallel.py path families_size instance threads family_run
'''

import os, sys, linecache


###System argument clean up#################

path = sys.argv[1]
instance = sys.argv[3]
threads = sys.argv[4]
family_run = sys.argv[5]

############################################


###Determining family size##################

if sys.argv[2] == 'small':
	family_size = '/families100.txt'
elif sys.argv[2] == 'large':
	family_size = '/families.txt'
else:
	print('**** Please enter a family size, either small or large ****')
	sys.exit()
	
############################################



###Load distances###########################

strains=[]
f=open(path + '/working/sample.txt','r')
for l in f:
	a=l.strip("\n").split("\t")
	strains.append(a[0])


f.close()


dist={}
f=open(path + "/working/RAxML_distances.dist","r")
for l in f:
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

f.close()

############################################


###Check for completed combinations#########
	
memo_subset={}
tmp = os.listdir(path + "/RM/")
for file in tmp:
	if file.startswith("rm"):
		f=open( path + "/RM/" + file,"r")
		for l in f:
			a=l.strip("\n").split("\t")
			if len(a) == 5:									
				memo_subset[a[0]] = a[1:]
		f.close()

		
############################################


###Load families for current instance#######
if family_run == 'run':
	family_size_path = path + '/working/' + family_size
else:
	family_size_path = family_run + family_size

i = int(instance)

subsets = []
while True:
	line = linecache.getline(family_size_path, i)
	if line == '':
		break
	i += int(threads)
	combination = line.strip('\n').split('\t')
	if not combination[1] in memo_subset:	
		subsets.append(combination[1])

print('Number of combinations for this instance: ' + str(len(subsets)))	
	
############################################


###Initialize output file###################
if not os.path.exists(path + '/RM/rm' + instance + '.txt'):
	f_subset=open(path + "/RM/rm" + instance + ".txt","w")
	f_subset.close()

############################################


###Load informative sites###################

tmp={}
f=open(path + "/working/short.fa","r")
for l in f:
	if l[0] == '>':
		nb=0
		tag=0
 		sp = l.strip('>').strip('\n')
		tmp[sp] = []
	else:
		nb += len(l.strip('\n'))
		tmp[sp].append(l.strip('\n'))


f.close()

############################################



###

seq = {}
for sp in strains:
	seq[sp] = ''.join(tmp[sp])

print(len(seq))


print('GO')

alpha=['A','C','G','T']

LONGUEUR=len(seq[sp])
for truc in subsets:
	strains = truc.split('-')
	bip=[]
	singleton,more=0,0
	i = 0
	r,m=0,0
	while i < LONGUEUR:
		tmp=[]
		memo=[]
		for sp in strains:
			N = seq[sp][i]
			if N in alpha:
				tmp.append(N)
				memo.append(sp)
		tot = len(tmp)
		all = list(set(tmp))
		unique,number=[],[]
		for N in all:
			number.append(tmp.count(N))
			if tmp.count(N) >1:
				unique.append(N)
		if len(number) > 1:
			while 1 in number:
				number.remove(1)
				singleton+=1
				m+=1
			if len(number) == 2:																		##### 2 #####
				more += 1
				N1,N2 = unique[0],unique[1]
				nt1,nt2 = tmp.count(N1),tmp.count(N2)
				if nt1 <= nt2:
					minor = N1
				elif nt1 > nt2:
					minor = N2
				sac,other=[],[]
				j=0
				while j < len(tmp):
					N,sp = tmp[j],memo[j]
					if N == minor:
						sac.append(sp)
					else:
						other.append(sp)
					j+=1
				INTRA,INTER=[],[]
				for sp1 in sac:
					for sp2 in sac:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1
				#print i,' ',tot,' ',unique,' ',number,' ',minor,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
			elif len(number) == 3:																		##### 3 #####
				N1,N2,N3 = unique[0],unique[1],unique[2]
				check,check2=0,0
				done=[]
				k=0
				while k < 3:
					N,nt = unique[k],number[k]
					if nt == min(number):
						if check == 0:
							minor1 =  N
							done.append(N)
							check=1
					elif nt == max(number):
						if check2==0:
							major = N
							done.append(N)
							check2=1
					k+=1
				for N in unique:
					if N not in done:
						minor2 = N
				sac1,sac2,other=[],[],[]
				j=0
				while j < len(tmp):
					N,sp = tmp[j],memo[j]
					if N == minor1:
						sac1.append(sp)
					elif N == minor2:
						sac2.append(sp)
					else:
						other.append(sp)
					j+=1
				INTRA,INTER=[],[]
				for sp1 in sac1:
					for sp2 in sac1:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1	
				#print i,' ',tot,' ',unique,' ',number,' ',minor1,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
				INTRA,INTER=[],[]
				for sp1 in sac2:
					for sp2 in sac2:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1
				#print i,' ',tot,' ',unique,' ',number,' ',minor2,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
			elif len(number) == 4:																		##### 4 #####
				N1,N2,N3,N4 = unique[0],unique[1],unique[2],unique[3]
				done=[]
				check,check2=0,0
				k=0
				while k < 4:
					N,nt = unique[k],number[k]
					if nt == min(number):
						if check==0:
							minor1 =  N
							done.append(N)
							check=1
					elif nt == max(number):
						if check2==0:
							major = N
							done.append(N)
							check2=1
					k+=1
				left=[]
				for N in unique:
					if N not in done:
						left.append(N)
				souvenir=[]
				k=0
				while k < 4:
					N,nt = unique[k],number[k]
					if N in left:
						souvenir.append(nt)
					k+=1
				if souvenir[0] <= souvenir[1]:
					minor2,minor3 = left[0],left[1]
				else:
					minor2,minor3 = left[1],left[0]
				sac1,sac2,sac3,other=[],[],[],[]
				j=0
				while j < len(tmp):
					N,sp = tmp[j],memo[j]
					if N == minor1:
						sac1.append(sp)
					elif N == minor2:
						sac2.append(sp)
					elif N == minor3:
						sac3.append(sp)
					else:
						other.append(sp)
					j+=1
				INTRA,INTER=[],[]
				for sp1 in sac1:
					for sp2 in sac1:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1	
				#print i,' ',tot,' ',unique,' ',number,' ',minor1,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
				INTRA,INTER=[],[]
				for sp1 in sac2:
					for sp2 in sac2:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1
				#print i,' ',tot,' ',unique,' ',number,' ',minor2,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
				INTRA,INTER=[],[]
				for sp1 in sac3:
					for sp2 in sac3:
						if sp1 != sp2:
							INTRA.append(dist[sp1][sp2])
					for sp2 in other:
						INTER.append(dist[sp1][sp2])
				if max(INTRA) > min(INTER):
					r+=1
					toto='r'
				else:
					toto='m'
					m+=1
				#print i,' ',tot,' ',unique,' ',number,' ',minor3,' ',min(INTRA),' ',min(INTER),' ',toto
				bip.append(toto)
		i+=1
	try:
		rm = float(r)/m
	except ZeroDivisionError:
		rm = 'NA'
	print('Number of genomes = %r, r/m= %r' % (len(strains), rm)) #,' r= ',r,' m= ',m	, '   Bips:  r= ',bip.count('r'),'  m= ',bip.count('m'),' |  for ',singleton,' singleton'
	h=open(path + "/RM/rm" + instance + ".txt","a")
	h.write(truc + '\t' + str(r) + '\t' + str(m) + '\t' + str(rm) + '\t' + str(len(bip)) + '\n'   )
	h.close()
