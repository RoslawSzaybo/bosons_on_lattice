#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 23 12:25:12 2018

This code computes overlaps between states. And saves them in a form usefull for 
later computations of fidelity susceptibility.
"""

import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

def get_states(filename):
	with open(filename, 'rb') as g:
		data = pickle.load(g)

	states = []
	deltas = []

	for sample in data:
		states += [sample[0]]
		deltas += [sample[1]['delta']]
	return (states,deltas)


def fidelity(states, deltas, reach):
	"""
	This is the time consuming step.

	psi_d is a tuple of (psis,deltas):
		psis is a list of ground states of a hamiltionians which differ in the value of delta
		deltas is a list of corresponding values of the paramter 
	"""

	fidelities = []
	data_len = len(states)
	if data_len != len(deltas):
		print("in fidelity:")
		print("len(states) != len(deltas)")
		sys.exit(-1)
		

	for i in range(data_len-1):
		psi = states[i]
		delta = deltas[i]

		loc_fi = []
		loc_ddelta = []
		range_forward = min(reach, (data_len-1)-i)
		for j in range(range_forward):
			fi = psi.overlap(states[i+j+1])[0]
			fi = abs(fi)
			loc_fi += [fi]
			loc_ddelta += [deltas[i+j+1] - delta]

		fidelities += [[loc_fi,loc_ddelta, delta]]
	return fidelities


def main():
	fs_reach = 5
	if len(sys.argv) != 3:
		print("Give filename as the command line argument.")
		print("python "+sys.argv[0]+" dmrg_results.pkl fiedlities_filename.pkl")
		sys.exit(-1)

	stts, dts = get_states(sys.argv[1])

	fidelity_filename = sys.argv[2]
	print("Now overlaps will be computed. It takes a lot of time (5 min)")
	fidelities = fidelity(stts, dts, fs_reach)

	print("OK, done. Now overlaps will be saved to "+fidelity_filename)
	with open(fidelity_filename, 'wb') as g:
		pickle.dump(fidelities, g)

	return 0

if __name__ == '__main__':
	main()
