Scan through delta values at fixed density = 0.5 at chi_max = 65 


This work is a toy model for finding the critical exponents in a
phase transition between cBOW_{1/2} and SF. Here I develop all necessary 
functionalities and test their working for $U \rightarrow \infty$ case which
is analitically solvable.


Warnings:
Strange behaviour at Delta ~ 0.7



Initiall paramters:
dmgr_params = {'LP_age': 0, 'norm_tol': 0.001, 'E_tol_to_trunc': None,
'update_env': 0, 'P_tol_to_trunc': None, 'trunc_params': {'chi_max': 50,
'trunc_cut': 1e-14, 'svd_min': 1e-10, '_used_param': {'symmetry_tol',
'chi_max', 'trunc_cut', 'chi_min', 'svd_min'}, 'symmetry_tol': None,
'chi_min': None, 'verbose': 0.0}, 'max_hours': 8760, 'chi_list': {0: 50},
'max_sweeps': 1000, 'start_env': 0, 'max_S_err': 0.1, 'lanczos_params':
{'E_tol': 5e-15, 'N_cache': 6, 'P_tol': 1e-14, 'N_max': 20, 'verbose': 0.0,
'N_min': 2, '_used_param': {'N_min', 'E_tol', 'N_cache', 'P_tol', 'N_max',
'min_gap'}, 'min_gap': 1e-12}, 'LP': None, 'RP': None, 'engine':
'EngineCombine', 'N_sweeps_check': 10, 'norm_tol_iter': 10, 'mixer': None,
'max_E_err': 0.1, '_used_param': {'update_env', 'P_tol_to_trunc',
'lanczos_params', 'max_hours', 'LP', 'RP', 'engine', 'N_sweeps_check',
'min_sweeps', 'RP_age', 'max_E_err', 'LP_age', 'norm_tol', 'E_tol_to_trunc',
'start_env', 'trunc_params', 'mixer', 'chi_list', 'verbose', 'max_sweeps',
'max_S_err', 'norm_tol_iter', 'sweep_0'}, 'min_sweeps': 15.0, 'RP_age': 0,
'sweep_0': 0, 'verbose': 0} 

model_params = {'bc_MPS': 'finite',
'conserve_fermionic_boson': 'Sz', 't': 1.0, 'alpha': 0.5, 'verbose': 0,
'_used_param': {'conserve_fermionic_boson', 'conserve_spin', 'beta', 'delta',
'bc_MPS', 'alpha', 'L', 't'}, 'conserve_spin': None, 'L': 60, 'delta': scan,
'beta': 0.02}.


I also test different chi_max values as well as different system sizes L = 20,
30, 34, 40, 46, 50.
