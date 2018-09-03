The program fs.py generates the plot of fidelity_susceptibility as a function
of delta. This data representes a peak at the phase transistion.


fs_*.tsv 		this files contains values of fidelity susceptibility as a function 
				of \Delta.
fidelity_*.pkl	this files contains fidelities a a list of list each list element 
				contains a list of overlaps between the selected state and next
				int(reach) states.  additionaly evey pack contains value of delta 
				at which the selected state representes ground state.


TODO:
[done] - fix the nonlinearity region: 
			= possible approach = 
		 Do the is_linear.
			if the last dy/dx is more than 0.3 * (dy/dx [0]) away from linear fit then
		it's not linear. And for the fidelity suscpetibility use the value of y[0].

- 0.3 is just an arbitrary value. It would be good to find something better.


