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
	magnetisation = sum(sigmaz[::2])-sum(sigmaz[1:][::2])
	magnetisation_per_site = magnetisation/len(sigmaz)

	return magnetisation_per_site

def welcome_interface():
	if len(sys.argv) < 3:
		print("I need name of a pickle file as a command line argument.")
		print("Second argument is bond dimension for the entropy of ent. data.")
		#print("If you will give third argument, then output will be saved there:")
		print("$ python "+str(sys.argv[0])+" input.pkl D\n")
		sys.exit(0)

	file_name = sys.argv[1]
	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)
	return delta_scan, int(sys.argv[2])

def main():
	delta_scan, desired_D = welcome_interface()

	L = delta_scan[0]['L']
	beta = delta_scan[0]['beta']
	delta = delta_scan[0]['delta']

	l = np.arange(L//2)
	ee_x_axis = np.log((np.pi/L)*np.sin(np.pi*l/L))

	# leave only states with information about the used bond dimension
	states = delta_scan[2:]

	for psi in states:
		state = psi[0]

		max_bond_dim = psi[1]
		if max_bond_dim == desired_D:
			ee = state.entanglement_entropy(n = 1)
			# This is how you can get the right scope for the plot
			first_half_ee = ee[1:(L//2+1)]

			plt.plot(ee_x_axis, first_half_ee, linestyle='-', marker='.')
			plt.xlabel('$\log(\\frac{\pi}{L}\sin(\pi \mathrm{l}/L))$')
			plt.ylabel('$S_\mathrm{l}$')
			plt.ylim(0.0,1.5)
			plt.grid()
			plt.title("Entanglement entropy $S_\mathrm{l}$\n"+\
					"$\Delta = {d:.4f}$".format(d=delta) +\
					", max bond dim = {a}".format(a=max_bond_dim)+\
					", $\\beta = {b:.2f}$".format(b=beta))
			plt.show()
			plt.clf()

			for idx, Sl in enumerate(first_half_ee):
				line =  "{:.9f}\t".format(ee_x_axis[idx])+\
						"{:.9f}\t".format(Sl)+\
						"{:d}".format(l[idx])
				print(line)

if __name__ == '__main__':
	main()
