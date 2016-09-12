###Fasta list generator

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