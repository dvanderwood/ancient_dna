import sys, os, subprocess, glob, random, linecache

'''
usage: 1000g_stats.py
'''

path = 'integrated_call_samples_v3.20130502.ALL.panel'
eur = []
eas = []
afr = []
sas = []
amr = []
ceu = []
tsi = []
fin = []
gbr = []
ibs = []
chb = []
jpt = []
chs = []
cdx = []
khv = []
yri = []
lwk = []
gwd = []
msl = []
esn = []
asw = []
acb = []
gih = []
pjl = []
beb = []
stu = []
itu = []
mxl = []
pur = []
clm = []
pel = []

final = []

with open(path) as info:
	line_num = 1
	for line in info:
		line_info = line.split()
		if line_info[2] == 'EUR':
			eur.append(line_num)
			if line_info [1] == 'CEU':
				ceu.append(line_num)
			elif line_info [1] == 'TSI':
				tsi.append(line_num)
			elif line_info [1] == 'FIN':
				fin.append(line_num)
			elif line_info [1] == 'GBR':
				gbr.append(line_num)
			elif line_info [1] == 'IBS':
				ibs.append(line_num)
		elif line_info[2] == 'EAS':
			eas.append(line_num)
			if line_info [1] == 'CHB':
				chb.append(line_num)
			elif line_info [1] == 'JPT':
				jpt.append(line_num)
			elif line_info [1] == 'CHS':
				chs.append(line_num)
			elif line_info [1] == 'CDX':
				cdx.append(line_num)
			elif line_info [1] == 'KHV':
				khv.append(line_num)
		elif line_info[2] == 'AFR':
			afr.append(line_num)
			if line_info [1] == 'YRI':
				yri.append(line_num)
			elif line_info [1] == 'LWK':
				lwk.append(line_num)
			elif line_info [1] == 'GWD':
				gwd.append(line_num)
			elif line_info [1] == 'MSL':
				msl.append(line_num)
			elif line_info [1] == 'ESN':
				esn.append(line_num)
			elif line_info [1] == 'ASW':
				asw.append(line_num)
			elif line_info [1] == 'ACB':
				acb.append(line_num)
		elif line_info[2] == 'SAS':
			sas.append(line_num)
			if line_info [1] == 'GIH':
				gih.append(line_num)
			elif line_info [1] == 'PJL':
				pjl.append(line_num)
			elif line_info [1] == 'BEB':
				beb.append(line_num)
			elif line_info [1] == 'STU':
				stu.append(line_num)
			elif line_info [1] == 'ITU':
				itu.append(line_num)
		elif line_info[2] == 'AMR':
			amr.append(line_num)
			if line_info [1] == 'MXL':
				mxl.append(line_num)
			elif line_info [1] == 'PUR':
				pur.append(line_num)
			elif line_info [1] == 'CLM':
				clm.append(line_num)
			elif line_info [1] == 'PEL':
				pel.append(line_num)
		line_num += 1


with open('stats.txt', 'w') as stt:
	stt.write('EUR: ')
	for item in eur:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('EAS: ')
	for item in eas:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('AFR: ')
	for item in afr:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('SAS: ')
	for item in sas:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('AMR: ')
	for item in amr:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('CEU: ')
	for item in ceu:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('TSI: ')
	for item in tsi:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('FIN: ')
	for item in fin:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('GBR: ')
	for item in gbr:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('IBS: ')
	for item in ibs:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('CHB: ')
	for item in chb:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('JPT: ')
	for item in jpt:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('CHS: ')
	for item in chs:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('CDX: ')
	for item in cdx:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('KHV: ')
	for item in khv:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('YRI: ')
	for item in yri:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('LWK: ')
	for item in lwk:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('GWD: ')
	for item in gwd:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('MSL: ')
	for item in msl:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('ESN: ')
	for item in esn:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('ASW: ')
	for item in asw:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('ACB: ')
	for item in acb:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('GIH: ')
	for item in gih:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('PJL: ')
	for item in pjl:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('BEB: ')
	for item in beb:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('STU: ')
	for item in stu:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('ITU: ')
	for item in itu:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('MXL: ')
	for item in mxl:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('PUR: ')
	for item in pur:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('CLM: ')
	for item in clm:
		stt.write(str(item) + ' ')
	stt.write('\n')
	stt.write('PEL: ')
	for item in pel:
		stt.write(str(item) + ' ')
	stt.write('\n')


if len(ceu) < 20:
	print 'Too Short'
if len(tsi) < 20:
	print 'Too Short'
if len(fin) < 20:
	print 'Too Short'
if len(gbr) < 20:
	print 'Too Short'
if len(ibs) < 20:
	print 'Too Short'
if len(chb) < 20:
	print 'Too Short'
if len(jpt) < 20:
	print 'Too Short'
if len(chs) < 20:
	print 'Too Short'
if len(cdx) < 20:
	print 'Too Short'
if len(khv) < 20:
	print 'Too Short'
if len(yri) < 15:
	print 'Too Short'
if len(lwk) < 15:
	print 'Too Short'
if len(gwd) < 15:
	print 'Too Short'
if len(msl) < 15:
	print 'Too Short'
if len(esn) < 15:
	print 'Too Short'
if len(asw) < 15:
	print 'Too Short'
if len(acb) < 15:
	print 'Too Short'
if len(gih) < 20:
	print 'Too Short'
if len(pjl) < 20:
	print 'Too Short'
if len(beb) < 20:
	print 'Too Short'
if len(stu) < 20:
	print 'Too Short'
if len(itu) < 20:
	print 'Too Short'
if len(mxl) < 25:
	print 'Too Short'
if len(pur) < 25:
	print 'Too Short'
if len(clm) < 25:
	print 'Too Short'
if len(pel) < 25:
	print 'Too Short'


import numpy as np

ceu_random = random.sample(xrange(len(ceu)), 20)
tsi_random = random.sample(xrange(len(tsi)), 20)
fin_random = random.sample(xrange(len(fin)), 20)
gbr_random = random.sample(xrange(len(gbr)), 20)
ibs_random = random.sample(xrange(len(ibs)), 20)
chb_random = random.sample(xrange(len(chb)), 20)
jpt_random = random.sample(xrange(len(jpt)), 20)
chs_random = random.sample(xrange(len(chs)), 20)
cdx_random = random.sample(xrange(len(cdx)), 20)
khv_random = random.sample(xrange(len(khv)), 20)
yri_random = random.sample(xrange(len(yri)), 15)
lwk_random = random.sample(xrange(len(lwk)), 15)
gwd_random = random.sample(xrange(len(gwd)), 15)
msl_random = random.sample(xrange(len(msl)), 15)
esn_random = random.sample(xrange(len(esn)), 15)
asw_random = random.sample(xrange(len(asw)), 15)
acb_random = random.sample(xrange(len(acb)), 15)
gih_random = random.sample(xrange(len(gih)), 20)
pjl_random = random.sample(xrange(len(pjl)), 20)
beb_random = random.sample(xrange(len(beb)), 20)
stu_random = random.sample(xrange(len(stu)), 20)
itu_random = random.sample(xrange(len(itu)), 20)
mxl_random = random.sample(xrange(len(mxl)), 25)
pur_random = random.sample(xrange(len(pur)), 25)
clm_random = random.sample(xrange(len(clm)), 25)
pel_random = random.sample(xrange(len(pel)), 25)

ceu_np = np.array(ceu)
tsi_np = np.array(tsi)
fin_np = np.array(fin)
gbr_np = np.array(gbr)
ibs_np = np.array(ibs)
chb_np = np.array(chb)
jpt_np = np.array(jpt)
chs_np = np.array(chs)
cdx_np = np.array(cdx)
khv_np = np.array(khv)
yri_np = np.array(yri)
lwk_np = np.array(lwk)
gwd_np = np.array(gwd)
msl_np = np.array(msl)
esn_np = np.array(esn)
asw_np = np.array(asw)
acb_np = np.array(acb)
gih_np = np.array(gih)
pjl_np = np.array(pjl)
beb_np = np.array(beb)
stu_np = np.array(stu)
itu_np = np.array(itu)
mxl_np = np.array(mxl)
pur_np = np.array(pur)
clm_np = np.array(clm)
pel_np = np.array(pel)

final.extend(list(ceu_np[ceu_random]))
final.extend(list(tsi_np[tsi_random]))
final.extend(list(fin_np[fin_random]))
final.extend(list(gbr_np[gbr_random]))
final.extend(list(ibs_np[ibs_random]))
final.extend(list(chb_np[chb_random]))
final.extend(list(jpt_np[jpt_random]))
final.extend(list(chs_np[chs_random]))
final.extend(list(cdx_np[cdx_random]))
final.extend(list(khv_np[khv_random]))
final.extend(list(yri_np[yri_random]))
final.extend(list(lwk_np[lwk_random]))
final.extend(list(gwd_np[gwd_random]))
final.extend(list(msl_np[msl_random]))
final.extend(list(esn_np[esn_random]))
final.extend(list(asw_np[asw_random]))
final.extend(list(acb_np[acb_random]))
final.extend(list(gih_np[gih_random]))
final.extend(list(pjl_np[pjl_random]))
final.extend(list(beb_np[beb_random]))
final.extend(list(stu_np[stu_random]))
final.extend(list(itu_np[itu_random]))
final.extend(list(mxl_np[mxl_random]))
final.extend(list(pur_np[pur_random]))
final.extend(list(clm_np[clm_random]))
final.extend(list(pel_np[pel_random]))

print final
print len(final)


with open('lines.txt', 'w') as line_doc:
	for item in final:
		line_doc.write(str(item) + '\n')

sample_list = 'samples.txt'
samp_list = []

with open('lines.txt') as lines_doc:
	with open('sample_selected.txt', 'w') as sample_selected:
		for line in lines_doc:
			sample_selected.write(linecache.getline(sample_list,int(line)))
			to_append = linecache.getline(sample_list,int(line))
			samp_list.append(to_append.strip())

samp_info_list = []
full_samp_list = ' '.join(samp_list)
print full_samp_list
with open(path) as info_dox:
	for line in info_dox:
		line_split = line.split()
		if line_split[0] in full_samp_list:
			samp_info_list.append(line)


with open('sample_selected_info.txt', 'w') as samp:
	for item in samp_info_list:
		samp.write(item)
