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


def show_fermionic_expectation_values(state, delta, beta, L):
	plt.ion()

	boson_site_number = np.arange(L)
	n = state.expectation_value('Sz0')+0.5
	plt.subplot(2, 1, 1)
	plt.title("Ground state expectation values\n$U=\infty$"+\
			", $\Delta$ = {a:.6f}".format(a=delta)+\
			", $\\beta$ = {b:.3f}".format(b=beta))
	plt.plot(boson_site_number, n, 'k*')
	plt.ylabel('$\langle n\\rangle$')
	plt.ylim(-0.15,1.15)
	plt.grid()

	bond_site_number = np.arange(L-1) + 0.5
	sigmaz = state.expectation_value('Sigmaz1')[:-1]
	plt.subplot(2, 1, 2)
	plt.plot(bond_site_number, sigmaz, 'r.')
	plt.xlabel('site number')
	plt.ylabel('$\langle\sigma^z\\rangle$')
	plt.ylim(-1.15,1.15)
	plt.grid()

	plt.draw()
	plt.pause(0.01)
	plt.clf()


def show_bosonic_expectation_values(state, U, delta, beta, L):
	plt.ion()

	boson_site_number = np.arange(L)
	n = state.expectation_value('N0')
	plt.subplot(2, 1, 1)
	plt.title("Ground state expectation values\n"+\
			"$U = $" + U + ", " +\
			"$\Delta$ = {a:.6f}, ".format(a=delta)+\
			"$\\beta$ = {b:.3f}".format(b=beta))
	plt.plot(boson_site_number, n, 'k*')
	plt.ylabel('$\langle n\\rangle$')
	plt.ylim(-0.15,1.15)
	plt.grid()

	bond_site_number = np.arange(L-1) + 0.5
	sigmaz = state.expectation_value('Sigmaz1')[:-1]
	plt.subplot(2, 1, 2)
	plt.plot(bond_site_number, sigmaz, 'r.')
	plt.xlabel('site number')
	plt.ylabel('$\langle\sigma^z\\rangle$')
	plt.ylim(-1.15,1.15)
	plt.grid()

	plt.draw()
	plt.pause(0.01)
	plt.clf()


def show_order_parameter(deltas, ord_params, beta, L, U):
	plt.ioff()
	plt.plot(deltas, ord_params, 'k*')
	plt.xlabel('$\Delta$')
	plt.ylabel('Staggered magnetisation')
	plt.ylim(-1.15,1.15)
	#plt.xlim(0.35,0.38)
	plt.grid()
	plt.title("Order parameter vs $\Delta$\n"+\
			  "L={a:d}, ".format(a=L) +\
			  "$\\rho = 0.5$, "+\
			  "$\\beta = {b:.3f}$, ".format(b=beta) +\
                "$U = $" + U)
	plt.show()
	plt.clf()


def find_magnetisation(delta_scan, quick, finite_U):
	L = delta_scan[0][1]['L']
	beta = delta_scan[0][1]['beta']

	deltas = []
	ord_params = []

	for psi in delta_scan:
		state = psi[0]
		delta = psi[1]['delta']
		deltas += [delta]
		magnetisation_every_second = order_parameter(state)
		ord_params += [magnetisation_every_second]
		if finite_U:
			U = psi[1]['U']
			U = "{:.4f}".format(U)
			if not quick:
				show_bosonic_expectation_values(state, U, delta, beta, L)
		else:
         		U = "$\infty$"
         		if not quick:
         			show_fermionic_expectation_values(state, U, delta, beta, L)
 
	show_order_parameter(deltas, ord_params, beta, L, U)
	return 0


def main():
	if len(sys.argv) < 2:
		print("I need name of a file as a command line argument!")
		print("$ python "+str(argv[0])+" filename.pkl")
		print("Alternatively if you only want to see the order parameter:")
		print("$ python "+str(argv[0])+" filename.pkl quick")
		sys.exit()
		
	file_name = sys.argv[1]
	with open(file_name, 'rb') as g:
		delta_scan = pickle.load(g)

	finite_U = ('U' in delta_scan[0][1])

	quick = len(sys.argv) > 2
	find_magnetisation(delta_scan, quick, finite_U)
	return 0
	

if __name__ == '__main__':
	main()
