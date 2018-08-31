#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:48:42 2018
Updated on Wed Aug 29 14:52:33 2018
"""

from tenpy.models.fermion_on_spin_lattice import FermionOnSpinLattice
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg
import time
import pickle
import numpy as np


def main():
	L=30
	delta=0.904

	file_name="L"+str(L) + \
			"_D"+str(int(delta*1000))+\
			"_CHIall.pkl"

	verbose_model = 0
	verbose_dmrg = 0

	t=1.0
	alpha=0.5
	beta=0.02


	cnsrv_bsn = 'Sz'
	cnsrv_spn = None

	model_params = {'L': L, 'bc_MPS':'finite', 
					't':  t, 'alpha': alpha, 'delta': delta, 
					'beta': beta, 'conserve_fermionic_boson': cnsrv_bsn , 
					'conserve_spin': cnsrv_spn, 'verbose': verbose_model}
	M = FermionOnSpinLattice(model_params)
	initial_state = [0]*(L//2) + [2]*(L//2)

	pkl_pack = [model_params, M]

	chi_start = np.arange(10)+5
	chi_end = np.arange(35)*2+15

	chis = np.concatenate((chi_start, chi_end))
	for chi in chis:
		psi = MPS.from_product_state(M.lat.mps_sites(), initial_state, bc='finite')
		dmrg_params = {'mixer': None, 'verbose': verbose_dmrg, \
					   'trunc_params': {'chi_max': chi, 'svd_min': 1.e-10}}
		start_time = time.time()
		dmrg.run(psi, M, dmrg_params)
		end_time = time.time()
		print("D max = {c}\tDMRG time = {b}".format(c=chi,b=end_time-start_time))
		pkl_pack += [[psi, chi]]

	with open(file_name,'wb') as g:
		pickle.dump(pkl_pack, g)

	return 0



if __name__ == '__main__':
	main()
