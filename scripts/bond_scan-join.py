#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 24 12:24:12 2018
"""

import numpy as np
import pickle
import sys


def chi(pkl):
	return pkl[1]


def main():
	if len(sys.argv) != 4:
		print("I need name of a file as a command line argument! like this:")
		print("$ python join.py A.pkl B.pkl output.pkl")
		sys.exit()

	in_a = sys.argv[1]
	in_b = sys.argv[2]
	out = sys.argv[3]


	with open(in_a, 'rb') as g:
		a = pickle.load(g)

	with open(in_b, 'rb') as g:
		b = pickle.load(g)

	if not a[0] == b[0]:
		print("CAREFUL!")
		print( " a[0] is different from b[0]")

	c = a[:2]
	
	c += sorted(a[2:]+b[2:], key = chi)

	with open(out, 'wb') as g:
		pickle.dump(c,g)

	return 0


if __name__ == '__main__':
	main()
