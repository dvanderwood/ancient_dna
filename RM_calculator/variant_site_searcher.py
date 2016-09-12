'''
usage: variant_site_searcher.py path
'''

#path = absolute path to the folder containing the fasta and phylip file for the organisms.
		#i.e. ~/path/to/directory
		#type pwd into your terminal when in the wanted directory to determine this
		# use . to indicate current directory

import sys, os

###System argument clean up#################

path = sys.argv[1]

############################################



# Load genome IDs
strains=[]
f=open(path + '/working/sample.txt','r')
for l in f:
	a=l.strip("\n")
	strains.append(a)
	
f.close()


# Load distances
dist={}
f=open(path + "/working/RAxML_distances.dist","r")
for l in f:
	a=l.strip("\n").split("\t")
	sp1,sp2 = a[0].split(" ")[0], a[0].split(" ")[1]
	#print sp1," ",sp2
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



# Load concatenate
tmp={}
f=open(path + "/working/all_genomes.fa", "r")
for l in f:
	if l[0] == '>':
		nb=0
		tag=0
		sp = l.strip('>').strip('\n').split('.')
		tmp[sp[0]] = []
	else:
		nb += len(l.strip('\n'))
		if tag ==0:
			tmp[sp[0]].append(l.strip('\n'))

f.close()


strains.sort()
with open(path + '/homoplasy/homoplasy_order.txt', 'w') as ordered:
	for sp in strains:
		ordered.write(sp + '\n')
		
seq = {}
for sp in strains:
	seq[sp] = ''.join(tmp[sp])

print('Loaded data')


#gene={}
#f=open(chemin + 'results/concatrim/positions/positions_' + SP + '.txt','r')
#for l in f:
#	a=l.strip('\n').split('\t')
#	id = a[0]
#	deb = int(a[1]) + 1
#	fin = int(a[2]) + 1
#	i = deb
#	while i <= fin:
#		gene[i] = id
#		i+=1
#
#f.close()




h=open(path + '/homoplasy/homoplasy.txt','w')

h.write('Position' + '\t' + 'Recombination' + '\t' + 'Mutation' + '\t' + 'Type' + '\t' + 'Singleton' + '\t' + 'Chain' + '\n' )


longueur = len(seq[sp])

print(longueur,' nt')

print('START')

print('Position r m type')

bip=[]
singleton,more=0,0
alpha=['A','C','G','T']
i = 0
r,m=0,0
while i < longueur:
	r,m=0,0
	singleton=0
	chain=''
	tmp,tmp2=[],[]
	memo=[]
	for sp in strains:
		N = seq[sp][i]
		if N in alpha:
			tmp.append(N)
			memo.append(sp)
		tmp2.append(N)
	tot = len(tmp)
	common = list(set(tmp))
	TYPE=str(len(common)-1)
	unique,number=[],[]
	for N in common:
		number.append(tmp.count(N))
		if tmp.count(N) >1:
			unique.append(N)
	if len(number) > 1 and len(tmp) > 4:
		while 1 in number:
			number.remove(1)
			singleton+=1
			toto='m'
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
					chain+='1'
				else:
					other.append(sp)
					chain+='0'
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
					if check2 == 0:
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
					chain+='1'
				elif N == minor2:
					sac2.append(sp)
					chain+='2'
				else:
					other.append(sp)
					chain+='0'
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
					chain+='1'
				elif N == minor2:
					sac2.append(sp)
					chain+='2'
				elif N == minor3:
					sac3.append(sp)
					chain+='3'
				else:
					other.append(sp)
					chain+='0'
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
		pos = i + 1
		print(pos,' ',r,' ',m,' ',TYPE)
		if singleton > 0:
			for N in tmp2:
				if N not in unique:
					chain += '1'
				else:
					chain +='0'
		if len(chain) != len(strains):
			chain='NA'
		h.write(str(pos) + '\t' + str(r) + '\t' + str(m) + '\t' + TYPE + '\tS=' + str(singleton) + '\t' + chain + '\n' )
	i+=1


h.close()




#print singleton,' singleton'
#print more,' more'
#print 'r= ',r,' m= ',m
#print 'r/m= ', float(r)/m


print('\nBips:')
print('r= ',bip.count('r'))
print('m= ',bip.count('m'))


