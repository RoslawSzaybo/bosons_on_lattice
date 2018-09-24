#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug  2 12:21:12 2018
"""

import numpy as np
import pickle
import sys


def welcome_interface(len_sys_argv):
	if len_sys_argv > 3 or len_sys_argv < 2:
		print("Put pickle filename first and output filename as the second argument.")
		print("Skip the second argument to get only stdout output.")
		sys.exit(-1)
	return 0

def order_parameter(psi):
	# [-1] as I dont want to count the extra spin dangling at the end of chain
	sigmaz = psi.expectation_value('Sigmaz1')[:-1]
	magnetisation = sum(sigmaz[::2])-sum(sigmaz[1:][::2])
	magnetisation_per_site = magnetisation/len(sigmaz)
	return magnetisation_per_site

def main():
	len_sys_argv = len(sys.argv)
	welcome_interface(len_sys_argv)

	file_name = sys.argv[1]

	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	# get some system parameters
	finite_U = ('U' in delta_scan[0][1])
	beta = delta_scan[0][1]['beta']
	if finite_U:
		U = "{:.2f}".format(delta_scan[0][1]['U'])
	else:
		U = "infty"


	# if the second argument is given then 
	# output is printed to the file
	if len_sys_argv == 3:
		out_filename = "U"+ U + \
			"_B{:.2f}_".format(beta) + str(sys.argv[2])
		out = open(out_filename, 'w')

	for psi in delta_scan:
		state = psi[0]
		delta = psi[1]['delta']

		staggered_magnetisation = order_parameter(state)

		data = "{d:.9f}\t{m:.9f}".format(d=delta,m=staggered_magnetisation)
		print(data)
		if len_sys_argv == 3:
			out.write(data+"\n")

	if len_sys_argv == 3:
		out.close()

	return 0


if __name__ == '__main__':
	main()
