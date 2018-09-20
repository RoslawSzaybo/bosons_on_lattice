#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug  2 12:21:12 2018
"""

import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt


def main():
	if len(sys.argv) != 2:
		print("I need name of a file as a command line argument!")
		sys.exit()

	file_name = sys.argv[1]


	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)


	old = len(delta_scan[0]) > 3
	if old:
		U_finite = False
	else:
		U_finite = ('U' in delta_scan[0][1])
	
	if U_finite:
		U = "${}$".format(delta_scan[0][1]['U'])
	else:
		U = "$\infty$"
		


	entglmt_entr = []
	bnd_dim = []


	if old:
		L = delta_scan[0]['L']
		beta = delta_scan[0]['beta']
		delta = delta_scan[0]['delta']
	else:
		L = delta_scan[0][0].L
		beta = delta_scan[0][1]['beta']
		delta = delta_scan[0][1]['delta']

	boson_site_number = np.arange(L)
	bond_site_number = np.arange(L-1)+0.5
	l = np.arange(L//2)
	ee_x_axis = np.log((np.pi/L)*np.sin(np.pi*l/L))

	if old:
		delta_scan = delta_scan[2:]

	for psi in delta_scan:
		state = psi[0]

		max_bond_dim = 0
		if old:
			max_bond_dim = psi[1]
		else:
			max_bond_dim = psi[2]['trunc_params']['chi_max']
		bnd_dim += [max_bond_dim]

		ee = state.entanglement_entropy(n = 1)
		first_half_ee = ee[:(L//2)]
		# I want to be on the top sequence
		entglmt_entr += [max(ee[L//2],ee[L//2-1])]

		plt.ion()
		plt.plot(ee_x_axis, first_half_ee, linestyle='-', marker='.')
		plt.xlabel('$\log(\\frac{\pi}{L}\sin(\pi \mathrm{l}/L))$')
		plt.ylabel('$S_\mathrm{l}$')
		plt.ylim(0.0,1.5)
		plt.grid()
		plt.title("Entanglement entropy $S_\mathrm{l}$\n"+\
				"$\Delta = {d:.4f}$".format(d=delta) +\
				", max bond dim = {a}".format(a=max_bond_dim)+\
				", $\\beta = {b:.2f}$".format(b=beta))
		plt.draw()
		plt.pause(0.25)
		plt.clf()


	plt.ioff()

	plt.plot(bnd_dim, entglmt_entr, 'k*')
	plt.xlabel('D - max bond dimension')
	plt.ylabel('Entanglement entropy\nat middle of the chain - $S_\mathrm{L/2}$')
	plt.grid()
	plt.title('Entanglement entropy at middle of the chain\n'+
			"$\Delta = {d:.4f}$".format(d=delta) +\
			", L = {l}".format(l=L)+\
			", U = " + U +\
			", $\\beta = {b:.2f}$".format(b=beta))
	plt.show()
	plt.clf()

if __name__ == '__main__':
	main()
