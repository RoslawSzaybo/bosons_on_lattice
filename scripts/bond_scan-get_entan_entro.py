#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug  2 12:21:12 2018
"""

import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt


def order_parameter(psi):
	# [-1] as I dont want to count the extra spin dangling at the end of chain
	sigmaz = psi.expectation_value('Sigmaz1')[:-1]
	staggered_magnetisation = sum(sigmaz[::2])-sum(sigmaz[1:][::2])
	magnetisation_per_site = staggered_magnetisation/len(sigmaz)

	return magnetisation_per_site


def main():
	if len(sys.argv) < 2:
		print("I need name of a pickle file as a command line argument!")
		print("If you will give second filename also, then output will be saved there:")
		print("python "+str(sys.argv[0])+" input.pkl [output.tsv]")
		sys.exit()
	file_name = sys.argv[1]


	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	entglmt_entr = []
	bnd_dim = []

	L = delta_scan[0]['L']
	beta = delta_scan[0]['beta']
	delta = delta_scan[0]['delta']

	delta_scan = delta_scan[2:]

	for psi in delta_scan:
		state = psi[0]

		max_bond_dim = psi[1]
		bnd_dim += [max_bond_dim]

		ee = state.entanglement_entropy(n = 1)
		first_half_ee = ee[:(L//2)]
		# I want to be on the top series
		entglmt_entr += [max(ee[L//2],ee[L//2-1])]

	plt.plot(bnd_dim, entglmt_entr, 'k*')
	plt.xlabel('D - max bond dimension')
	plt.ylabel('Entanglement entropy\nat middle of the chain - $S_\mathrm{L/2}$')
	plt.grid()
	plt.title('Entanglement entropy at middle of the chain\n'+
			"$\Delta = {d:.4f}$".format(d=delta) +\
			", L = {l}".format(l=L)+\
			", U = $\infty$"+\
			", $\\beta = {b:.2f}$".format(b=beta))
	plt.show()
	plt.clf()

	if len(sys.argv) > 2:
		output = open(sys.argv[2],'w')

	for idx, ee in enumerate(entglmt_entr):
		line = "{D:d}\t".format(D = bnd_dim[idx]) +\
				"{e:.9f}".format(e = ee)
		print(line)
		if len(sys.argv) > 2:
			output.write(line+"\n")


if __name__ == '__main__':
	main()
