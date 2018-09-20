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


def main():
	if len(sys.argv) != 2:
		print("I need name of a file as a command line argument!")
		sys.exit()

	file_name = sys.argv[1]


	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	ord_params = []
	entglmt_entr = []
	bnd_dim = []

	old = len(delta_scan[0]) > 3
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

		staggered_magnetisation = order_parameter(state)
		ord_params += [staggered_magnetisation]

		max_bond_dim = 0
		if old:
			max_bond_dim = psi[1]
		else:
			max_bond_dim = psi[2]['trunc_params']['chi_max']
		bnd_dim += [max_bond_dim]

		ee = state.entanglement_entropy(n = 1)
		# I want to be on the top series
		entglmt_entr += [max(ee[L//2],ee[L//2-1])]


		plt.ion()

		n = state.expectation_value('Sz0')+0.5
		plt.subplot(2, 1, 1)
		plt.title("Ground state expectation values\n"+\
				"max bond dim = {a:d}".format(a=max_bond_dim))
		plt.plot(boson_site_number, n, 'k*')
		plt.ylabel('$\langle n\\rangle$')
		plt.ylim(-0.15,1.15)
		plt.grid()


		sigmaz = state.expectation_value('Sigmaz1')[:-1]
		plt.subplot(2, 1, 2)
		plt.plot(bond_site_number, sigmaz, 'r.')
		plt.xlabel('site $i$')
		plt.ylabel('$\langle\sigma^z\\rangle$')
		plt.ylim(-1.35,1.15)
		plt.text(0, -1.25, "order parameter = "+\
				"{a:.6f}".format(a = staggered_magnetisation))
		plt.text(30, -1.25, 
				'entropy of entanglement = {a:.6f}'.format(a = entglmt_entr[-1]))
		plt.grid()

		plt.draw()
		plt.pause(0.25)
		plt.clf()

	plt.ioff()
	plt.plot(bnd_dim, ord_params, 'k*')
	plt.xlabel('D - max bond dimension')
	plt.ylabel('Staggered magnetisation')
	plt.grid()
	plt.title("Order parameter vs max bond dimension\n"+
			"$\Delta = {d:.4f}$".format(d=delta) +\
			", L = {l}".format(l=L)+\
			", U = $\infty$"+\
			", $\\beta = {b:.2f}$".format(b=beta))
	plt.show()
	plt.clf()

	plt.plot(bnd_dim, entglmt_entr, 'k*')
	plt.xlabel('D - max bond dimension')
	plt.ylabel('Entanglement entropy\nat middle of the chain - $S_\mathrm{L/2}$')
	plt.grid()
	plt.title('Entanglement entropy at the middle of the chain\n'+
			"$\Delta = {d:.4f}$".format(d=delta) +\
			", L = {l}".format(l=L)+\
			", U = $\infty$"+\
			", $\\beta = {b:.2f}$".format(b=beta))
	plt.show()
	plt.clf()

if __name__ == '__main__':
	main()
