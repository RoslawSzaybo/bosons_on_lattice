I have submitted extra delta85 scan to explor chi_max < 32. Because
I am afraid that the results are not much impressive because 
the region where I scan is all staturated already.


A fig similar to Fig. 6. from supplementary materials.

How does the system properties depend on a max bond dimension?

Parameters used in simulation:

	rho = 0.5
	alpha = 0.5
	beta = 0.02
	delta = 0.85
	t = 1.0

This parameters corresponds to the cBOW_{1/2} phase. 


Structure of pickle:
- first element is model_params (see above)
- secon is model <tenpy.models.fermion_on_spin_lattice.FermionOnSpinLattice>
- remaining are: [state,max_bond_dim]

Remarks:
analayse ptlots nicely, however, not what is interesting so far.

{'_used_param': {'t', 'conserve_spin', 'conserve_fermionic_boson', 'L',
'bc_MPS', 'beta', 'alpha', 'delta'}, 't': 1.0, 'bc_MPS': 'finite', 'beta':
0.02, 'conserve_spin': None, 'alpha': 0.5, 'L': 60,
'conserve_fermionic_boson': 'Sz', 'delta': 0.85, 'verbose': 0}
