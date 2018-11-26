#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 24 12:24:12 2018
"""

import numpy as np
import pickle
import sys


def delta(pkl):
	return pkl[1]['delta']

zero = 1e-14
def the_same(a,b):
	delta_a = delta(a)
	delta_b = delta(b)
	diff = abs(delta_b-delta_a)
	return (diff < zero)

def repetitions(c):
	repeted_idxes = []
	for idx, elem in enumerate(c):
		if idx == 0:
			continue

		if the_same(c[idx-1], elem):
			repeted_idxes += [idx] 

	return repeted_idxes

def clean_repetitions(c):
	to_del = repetitions(c)

	print("Initial number of data points\t\t {dp}".format(dp=len(c)))
	print("Number of elements to be removed\t {td}".format(td=len(to_del)))

	for idx in reversed(to_del):
		c.pop(idx)

	print("Final number of data points\t\t {dp}".format(dp=len(c)))

	return c


def main():
	if len(sys.argv) != 6:
            print("it joins four!!!")
            print("it joins four!!!")
            print("it joins four!!!")
            print("I need name of a file as a command line argument! like this:")
            print("$ python join.py A.pkl B.pkl C.pkl D.pkl E.pkl output.pkl")
            sys.exit()

	in_a = sys.argv[1]
	in_b = sys.argv[2]
	in_c = sys.argv[3]
	in_d = sys.argv[4]
	out = sys.argv[5]
	 

	print("="*80)
	print("Join")
	print("="*80)
	print("Reading files in progress")
	with open(in_a, 'rb') as g:
		a = pickle.load(g)

	with open(in_b, 'rb') as g:
		b = pickle.load(g)

	with open(in_c, 'rb') as g:
		x = pickle.load(g)

	with open(in_d, 'rb') as g:
		y = pickle.load(g)

	print("Files are open.")

	c = sorted(a+b+x+y, key = delta)
	print("Data in now united to a one, sorted file.")
	d = clean_repetitions(c)
	print("All repetitions are removed.")

	with open(out, 'wb') as g:
		pickle.dump(d,g)
	print("Data is saved to {}".format(out))

	return 0

if __name__ == '__main__':
	main()
