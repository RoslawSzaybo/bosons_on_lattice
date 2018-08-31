#!/usr/bin/env python3
"""
Created on Thu Jul 12 17:48:42 2018
Upgraded on Wed Aug 29 14:44:21 2018
"""

from tenpy.models.fermion_on_spin_lattice import FermionOnSpinLattice
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg
import time
import pickle


def main():
	L=54
	chi = 50

	file_name="L"+str(L)+"_D09E_CHI"+str(chi)+".pkl"

	verbose_model = 0
	verbose_dmrg = 0

	t=1.0
	alpha=0.5
	beta=0.02


	cnsrv_bsn = 'Sz'
	cnsrv_spn = None
	pkl_pack = []

	for ddelta in range(101):
		delta = 0.9063 + ddelta*0.000063
		model_params = {'L': L, 'bc_MPS':'finite', 'filling': 0.5,
						't':  t, 'alpha': alpha, 'delta': delta,
						'beta': beta, 'conserve_fermionic_boson': cnsrv_bsn,
						'conserve_spin': cnsrv_spn, 'verbose': verbose_model}
		M = FermionOnSpinLattice(model_params)
		initial_state = [0]*(L//2) + [2]*(L//2)
		psi = MPS.from_product_state(M.lat.mps_sites(), initial_state , bc='finite')
		dmrg_params = {'mixer': None, 'verbose': verbose_dmrg, \
					   'trunc_params': {'chi_max': chi, 'svd_min': 1.e-10}}
		start_time = time.time()
		dmrg.run(psi, M, dmrg_params)
		end_time = time.time()
		print("Delta = {a:.04f}\tDMRG time = {b}".format(a=delta,b=end_time-start_time))
		pkl_pack += [[psi,model_params,dmrg_params]]

	with open(file_name,'wb') as g:
		pickle.dump(pkl_pack, g)

	return 0

if __name__ == '__main__':
	main()
