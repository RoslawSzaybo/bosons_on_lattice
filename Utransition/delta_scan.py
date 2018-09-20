#!/usr/bin/env python3

"""
Created on Thu Jul 12 17:48:42 2018
"""

from tenpy.models.boson_spin import BosonSpin 
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg
import time
import pickle

def main():
	L = 40
	chi = 60
	U = 1.0
	beta = 0.02

	file_name = "U" + str(int(U)) +\
			"_L"+str(L)+\
			"_Ds_ch"+str(chi)+\
			".pkl"

	verbose_model = 0
	verbose_dmrg = 0

	t=1.0
	Mu=16.0
	alpha=0.5

	cnsrv_bsn = 'N'
	cnsrv_spn = None
	pkl_pack = []

	for ddelta in range(51):
		delta = 0.50 + ddelta*0.01
		model_params = {'n_max': 2, 'L': L, 'bc_MPS':'finite', 'filling': 0.5,
						't':  t, 'U': U, 'mu': Mu, 'alpha': alpha, 'delta': delta,
						'beta': beta, 'conserve_boson': cnsrv_bsn ,
						'conserve_spin': cnsrv_spn, 'verbose': verbose_model}
		M = BosonSpin(model_params)
		initial_state = [0]*(L//2) + [2]*(L//2)
		psi = MPS.from_product_state(M.lat.mps_sites(), initial_state , bc='finite')
		dmrg_params = {'mixer': None, 'verbose': verbose_dmrg, \
					   'trunc_params': {'chi_max': chi, 'svd_min': 1.e-10}}
		start_time = time.time()
		dmrg.run(psi, M, dmrg_params)
		end_time = time.time()
		print("$\Delta = {a:.04f}$\tDMRG time = {b}".format(a=delta,b=end_time-start_time))
		pkl_pack += [[psi,model_params,dmrg_params]]

	with open(file_name,'wb') as g:
		pickle.dump(pkl_pack, g)

	return 0

if __name__ == '__main__':
	main()
