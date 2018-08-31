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


def find_magnetisation(delta_scan):
	deltas = []
	ord_params = []


	L = delta_scan[0][1]['L']
	boson_site_number = np.arange(L)
	bond_site_number = np.arange(L-1) + 0.5

	for psi in delta_scan:
		state = psi[0]
		delta = psi[1]['delta']
		deltas += [delta]
		magnetisation_every_second = order_parameter(state)
		ord_params += [magnetisation_every_second]

		sigmaz = state.expectation_value('Sigmaz1')[:-1]
		n = state.expectation_value('Sz0')+0.5

		plt.ion()
		plt.subplot(2, 1, 1)
		plt.title('Ground expectation values\n @ $\Delta$ = {a:.6f}'.format(a=delta))
		plt.plot(boson_site_number, n, 'k*')
		plt.ylabel('$\langle n\\rangle$')
		plt.ylim(-0.15,1.15)
		plt.grid()


		plt.subplot(2, 1, 2)
		plt.plot(bond_site_number, sigmaz, 'r.')
		plt.xlabel('site number')
		plt.ylabel('$\langle\sigma^z\\rangle$')
		plt.ylim(-1.35,1.15)
		plt.text(0, -1.25, 'order parameter = {a:.6f}'.format(a = magnetisation_every_second))
		plt.grid()

		plt.draw()
		plt.pause(0.01)
		plt.clf()


	plt.plot(deltas, ord_params, 'k*')
	plt.xlabel('$\Delta$')
	plt.ylabel('Staggered magnetisation')
	#plt.ylim(0.0,1.0)
	#plt.xlim(0.35,0.38)
	plt.grid()
	plt.title('Order parameter vs $\Delta$\n @ L={a:d} sites with half filling'.format(a=state.L))
	plt.show()
	plt.clf()

	return (deltas, ord_params)


def main():
	if len(sys.argv) != 2:
		print("I need name of a file as a command line argument!")
		sys.exit()
		
	file_name = sys.argv[1]

	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	find_magnetisation(delta_scan)

	return 0
	

if __name__ == '__main__':
	main()
