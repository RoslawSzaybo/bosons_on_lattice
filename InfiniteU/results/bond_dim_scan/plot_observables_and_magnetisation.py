#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug  2 12:21:12 2018
"""

import numpy as np
import pickle
import sys

if len(sys.argv) != 2:
	print("I need name of a file as a command line argument!")
	sys.exit()

file_name = sys.argv[1]


with open(file_name, 'rb') as g:
    delta_scan = pickle.load(g)

def order_parameter(psi):
	# [-1] as I dont want to count the extra spin dangling at the end of chain
	sigmaz = psi.expectation_value('Sigmaz1')[:-1]
	magnetisation = sum(sigmaz[::2])-sum(sigmaz[1:][::2])
	magnetisation_per_site = magnetisation/len(sigmaz)

	return magnetisation_per_site

import matplotlib.pyplot as plt

occupation = 1.0-np.arange(61)/60.0
ord_params = []
bnd_dim = []


L = delta_scan[0]['L']

boson_site_number = np.arange(L)
bond_site_number = np.arange(L-1)+0.5

delta_scan = delta_scan[2:]

for psi in delta_scan:
	state = psi[0]
	n = state.expectation_value('Sz0')+0.5
	sigmaz = state.expectation_value('Sigmaz1')[:-1]

	magnetisation_every_second = order_parameter(state)
	ord_params += [magnetisation_every_second]

	max_bond_dim = psi[1]
	bnd_dim += [max_bond_dim]

	plt.subplot(2, 1, 1)
	plt.title('Ground expectation values\nmax bond dim = {a:d}'.format(a=max_bond_dim))
	plt.plot(boson_site_number, n, 'k*')
	plt.ylabel('$\langle n\\rangle>$')
	plt.ylim(-0.15,1.15)
	plt.grid()


	plt.subplot(2, 1, 2)
	plt.plot(bond_site_number, sigmaz, 'r.')
	plt.xlabel('site $i$')
	plt.ylabel('$\langle\sigma^z\\rangle$')
	plt.ylim(-1.35,1.15)
	plt.text(0, -1.25, 'order parameter = {a:.4f}'.format(a = magnetisation_every_second))
	plt.grid()

	plt.show()
	plt.clf()
    

plt.plot(bnd_dim, ord_params, 'k*')
plt.xlabel('$\langle n\\rangle$')
plt.ylabel('Staggered magnetisation')
plt.grid()
plt.title('Order parameter vs max bond dimension\n @ $\Delta = 0.85$')
plt.show()
plt.clf()
