#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug  2 12:21:12 2018
"""

import numpy as np
import pickle
import sys

def get_expectation_values(delta_scan, finite_U):
	deltas = []
	occupations = []
	spins = []

	for psi in delta_scan:
		state = psi[0]
		delta = psi[1]['delta']

		deltas += [delta]
		spins += [state.expectation_value('Sigmaz1').tolist()]

		if finite_U:
			occupations += [state.expectation_value('N0').tolist()]
		else:
			n = state.expectation_value('Sz0')+0.5
			occupations += [n.tolist()]

	return [deltas, occupations, spins]

def save_output(out, deltas, occupations, spins):
	for idx, dd in enumerate(deltas):
		out.write("{:.4f}\n".format(dd))

		occ = ""
		for n in occupations[idx]:
			occ += "{:.4f}\t".format(n)
		occ += "\n"
		out.write(occ)

		spns = ""
		for spn in spins[idx]:
			spns += "{:.4f}\t".format(spn)
		spns += "\n"
		out.write(spns)
	return 0


def main():
	if len(sys.argv) != 3:
		print("I need name of a file as a command line argument!")
		print("$ python "+str(argv[0])+" filename.pkl out.dat")
		sys.exit()
		
	file_name = sys.argv[1]
	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	finite_U = ('U' in delta_scan[0][1])

	deltas, occupations, spins = get_expectation_values(delta_scan, finite_U)

	beta = delta_scan[0][1]['beta']
	if finite_U:
		U = "{:.2f}".format(delta_scan[0][1]['U'])
	else:
		U = "infty"

	out_filename = "U"+ U + \
			"_B{:.2f}_".format(beta) + str(sys.argv[2])
	out = open(out_filename, 'w')
	
	save_output(out, deltas, occupations, spins)

	return 0
	

if __name__ == '__main__':
	main()
