links_prob_file = open('/Users/dasha/PhD/data/only_best_prob_SKO7.txt','r')
freec_file = open('/Users/dasha/PhD/FREEC_Linux64/SKOV3_sort.bam.bam_CNVs','r')
links_file = open('/Users/dasha/PhD/data/clusters_files/SKO/clust_15_10_22.txt','r')
out = open('freec_vs_svbay.txt','w')
links_names=[]
links_name_beg =dict()
links_names_sh =[]
#for i in links_prob_file:
#	if '0]]' not in i:
#		line = i.split(' ')
#		links_names.append([line[4],line[10:16]])
#		links_names_sh.append(line[4])
#links_prob_file.close()
#chromosomes = []
#chromosome collection
#for i in links_names:
#	print i
#	name = i[0].split('_')
#	for j in name:
#		if 'chr' in j :
#			chrom = j.replace('chr','')
#			if chrom not in chromosomes:
#				chromosomes.append(chrom)
print chromosomes
#dictionary collection
for chrom in chromosomes:
	links_name_beg[chrom]=[]
print links_names
for i in links_file:
	if i:
		line = i.split(';')
		name = line[0]
		beg = line[1]
		end = line[2]
		numb_el = line[5]
		name_chr = name.split('_')[1].replace('chr','')
		if int(numb_el)>5:
			links_name_beg[name_chr].append([name,[beg,end]])
freec_chr =[]
freec_lines = freec_file.readlines()
print links_name_beg
for chrom in chromosomes:
	print 'chr',chrom
	freec_chr =[]
	for line in freec_lines:
		line = line.split()
		if line[0] == chrom:
			freec_chr.append(line)
	print freec_chr
	for freec in freec_chr:
		print freec 
		for link in links_name_beg[chrom]:
			print link
			if abs(int(freec[1])-int(link[1][0]))<=10000 or abs(int(freec[2])-int(link[1][0]))<=12120000:
				out.write(str(link)+' '+str(freec))
			if int(link[1][0]) - int(freec[1])>10000:
				break
out.close()
freec_file.close()
links_file.close()
