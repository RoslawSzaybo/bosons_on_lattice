The program fs.py generates the plot of fidelity susceptibility as a function
of delta. This data representes a peak at the phase transistion.


fs_*.tsv 		this files contain values of fidelity susceptibility as a function 
				of \Delta.
fidelity_*.pkl	this files contain fidelities as a list of lists. Each list element 
				contains a list of overlaps between the selected state and next
				int(reach) states. Additionaly, every pack contains value of delta 
				at which the selected state representes the ground state.


TODO:
[done] - fix the nonlinearity region: 
			= possible approach = 
		 Do the is_linear.
			if the last dy/dx is more than 0.3 * (dy/dx [0]) away from linear fit then
		it's not linear. And for the fidelity suscpetibility use the value of y[0].

- 0.3 is just an arbitrary value. It would be good to find something better.


