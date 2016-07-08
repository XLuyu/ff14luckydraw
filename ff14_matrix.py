import copy
import sys
import time
import operator
award = [0]*6+[10000,36,720,360,80,252,108,72,54,180,72,180,119,36,360,1080,144,1800,3600]

# def gen_case(depth,state):
# 	if depth>9:
# 		yield state
# 	else:
# 		for i in range(1,10):
# 			if i not in state:
# 				for yd in gen_case(depth+1,state+[i]): yield yd
# def rows_sum(c):
# 	r1 = c[1]+c[2]+c[3]
# 	r2 = c[4]+c[5]+c[6]
# 	r3 = c[7]+c[8]+c[9]
# 	c1 = c[1]+c[4]+c[7]
# 	c2 = c[2]+c[5]+c[8]
# 	c3 = c[3]+c[6]+c[9]
# 	d1 = c[1]+c[5]+c[9]
# 	d2 = c[3]+c[5]+c[7]
# 	return [r1,r2,r3,c1,c2,c3,d1,d2]
# allmaps = [copy.copy(i) for i in gen_case(1,[0])]
# mapsum = [rows_sum(i) for i in allmaps]

# def rows_expectation(mask):

# 	cnt = 0
# 	select = [0]*8
# 	for idx,c in enumerate(allmaps):
# 		for i in range(1,10):
# 			if mask[i] not in [0,c[i]]: break
# 		if mask[i] not in [0,c[i]]: continue
# 		rcd = mapsum[idx]
# 		for i in range(8):
# 			select[i] += award[rcd[i]]
# 		cnt += 1
# 	select = [i/float(cnt) for i in select]
# 	return select
#############################
allmaps = {}
def row_case_expectation(slc,avail):
	if len(slc)==3:
		return float(award[sum(slc)])
	exp = 0
	if len(avail)==0: return 0
	for i in avail:
		exp += row_case_expectation(slc+(i,),filter(lambda x:x!=i,avail))
	return exp/len(avail)
	
def gen_case(depth,slc,avail):
	if depth>9:
		global allmaps
		exp = row_case_expectation(slc,avail)
		allmaps[(slc,avail)] = exp
	else:
		gen_case(depth+1,slc,avail) # not avail
		if len(slc)<3: gen_case(depth+1,slc+(depth,),avail) # selected
		gen_case(depth+1,slc,avail+(depth,)) # avail
gen_case(1,(),())
# print len(allmaps)
# fout = open("allmaps","w")
# for i in allmaps:
# 	fout.write("%s %s\n"%(str(i),str(allmaps[i])))
def rows_expectation(mask):
	avail = tuple(filter(lambda x:x not in filter(lambda x:x!=0,mask),range(1,10)))
	r1 = [mask[1],mask[2],mask[3]]
	r2 = [mask[4],mask[5],mask[6]]
	r3 = [mask[7],mask[8],mask[9]]
	c1 = [mask[1],mask[4],mask[7]]
	c2 = [mask[2],mask[5],mask[8]]
	c3 = [mask[3],mask[6],mask[9]]
	d1 = [mask[1],mask[5],mask[9]]
	d2 = [mask[3],mask[5],mask[7]]
	rows = [r1,r2,r3,c1,c2,c3,d1,d2]
	rows = [tuple(sorted(filter(lambda x:x!=0,row))) for row in rows]
	select = [allmaps[row,avail] for row in rows]
	return select

mask = [0]*10

def fill_slots(slots,depth,mask):
	if depth>9:
		return max(rows_expectation(mask))
	if depth not in slots:
		return fill_slots(slots,depth+1,mask+[0])
	else:
		allslc = 0
		for i in range(1,10):
			if i not in mask:
				allslc += fill_slots(slots,depth+1,mask+[i])
		return allslc

num_slots = 4
total_cnt = float(reduce(operator.mul,[1]+range(10-num_slots,10)))
strategy = {}
def gen_slots(depth,begin,slots):
	if depth>num_slots:
		global cnt,strategy
		print slots,":",
		select = fill_slots(slots,1,[0])/total_cnt
		strategy[tuple(slots)] = select
		print select
	else:
		for i in range(begin,10):
			gen_slots(depth+1,i+1,slots+[i])

# gen_slots(1,1,[0])
ms={}
def next_step(case,max_reveal=4):
	# print case
	if tuple(case) in ms: return ms[tuple(case)]
	if len(filter(lambda x:x!=0,case))==max_reveal:
		select = [(idx,i) for idx,i in enumerate(rows_expectation(case))]
		select.sort(key=lambda x:-x[1])
		return select[0]
	exps = []
	for pos in range(1,10):
		if case[pos]==0:
			exp = cnt = 0
			tmp = copy.copy(case)
			for i in range(1,10):
				if i not in case:
					tmp[pos] = i
					exp += next_step(tmp)[1]
					cnt += 1
			exps += [(pos,exp/float(cnt))]
	exps.sort(key=lambda x:-x[1])
	ms[tuple(case)] = exps[0]
	return exps[0]

def case_pos_exp(case,max_reveal=4): # -1 for selected position
	pos = case.index(-1)
	exp = cnt = 0
	tmp = copy.copy(case)
	for i in range(1,10):
		if i not in case:
			tmp[pos] = i
			exp += next_step(tmp)[1]
			cnt += 1
	return exp/float(cnt)

import Tkinter
from Tkinter import *
class MyLabel(Label):
	def __init__(self,*l,**k):
		self.txt = StringVar()
		self.txt.set("")
		k["textvariable"]=self.txt
		Label.__init__(self,*l,**k)
	def set(self,s):
		self.txt.set(s)

def cal_rate(event):
	global Labels
	m = [0]*10
	for i in range(9):
		num = blocks[i].get()
		num = 0 if num=="" else int(num)
		m[i+1] = num
	select = rows_expectation(m)
	for i in range(8):
		Labels[i].set("%.1f"%(select[i]))
	for i in range(8):
		print i,select[i]
	print next_step(m)

root = Tkinter.Tk()
Lpos = [(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(0,0),(0,4)]
Labels = [MyLabel(root,width=4,border=5) for i in range(8)]
for i,label in enumerate(Labels):
	label.grid(row = Lpos[i][0],column=Lpos[i][1])
blocks = [Entry(root,width=2,border=5) for i in range(9)]
for i in range(9):
	blocks[i].grid(row=i/3+1,column=i%3+1)
button = Button(root,text="expectation",width=20)
button.grid(row=4,column = 1,columnspan=3)
button.bind('<Button-1>',cal_rate)
# root.geometry("120x120")
root.mainloop()
