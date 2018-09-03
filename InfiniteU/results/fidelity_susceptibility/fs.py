#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 23 12:25:12 2018

TODO:
	There are regions where the behaviour of 
	$\Chi(\delta\Delta) = -2\ln(|\langle \Psi(\Delta) | \Psi(\Delta +\delta\Delta) \rangle)|)/\delta\Delta^2$
	is not linear in $\delta\Delta$. Therefore the limit $\delta\Delta \rightarrow 0$ 
	in that region is not just an lintersection of the linear fit with the x=0 axis.

	Such region is located in the nearest neighbourhood of the phase transition.  The 
	linear behaviour will appear only after the sampling of the transition region will become finer. 

	There is a need to find a way to determine quantitatively if the 
	function is linear in the specified region or not and what to do if not.

	[done?]
	Now there is an arbitrary test which checks if the behaviour is linear or not. If not then 
	fidelity susceptibility at that point is returned as a value of $\Chi(\delta\Delta)$ at the
	smalles known $\delta\Delta$.
"""

import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

def get_states(filename):
	with open(filename, 'rb') as g:
		data = pickle.load(g)

	states = []
	deltas = []

	for sample in data:
		states += [sample[0]]
		deltas += [sample[1]['delta']]
	return (states,deltas)

def fidelity(states, deltas, reach):
	"""
	This is the time consuming step.

	psi_d is a tuple of (psis,deltas):
		psis is a list of ground states of a hamiltionians which differ in the value of delta
		deltas is a list of corresponding values of the paramter 
	"""

	fidelities = []
	data_len = len(states)
	if data_len != len(deltas):
		print("in fidelity:")
		print("len(states) != len(deltas)")
		sys.exit(-1)
		

	for i in range(data_len-1):
		psi = states[i]
		delta = deltas[i]

		loc_fi = []
		loc_ddelta = []
		range_forward = min(reach, (data_len-1)-i)
		for j in range(range_forward):
			fi = psi.overlap(states[i+j+1])[0]
			fi = abs(fi)
			loc_fi += [fi]
			loc_ddelta += [deltas[i+j+1] - delta]

		fidelities += [[loc_fi,loc_ddelta, delta]]
	return fidelities

def linear_model(xvalues,yvalues):
	"""
	assumes: yvalues = a*xvalues + c
	returns: (a,c)
	"""
	dy = yvalues[1]-yvalues[0]
	dx = xvalues[1]-xvalues[0]

	a = dy/dx
	c = yvalues[0] - a*xvalues[0] 
	return (a,c)


def is_linear(xvalues,yvalues):
	"""
	It's very arbitrary. Just one of ideas that 
	came to my mind.
	"""
	arbitrary_limit = 1.0
	a,c = linear_model(xvalues,yvalues)

	first_jump = abs(yvalues[1] - yvalues[0])

	lin_model_last_y_value = a*xvalues[-1] + c
	diff_from_lin = abs(yvalues[-1] - lin_model_last_y_value) 

	the_ratio = diff_from_lin/first_jump

	return (the_ratio < arbitrary_limit)


def fidelity_susceptibility_extrapolation(fidelities, fs_reach):
	"""
	arguments:
	fidelistes	list of pairs [a,b] a is a list of overlaps of ground states
									b is a list of differences of deltas
	fs_reach	an integer which gives a number of points where I look for linear behaviour
	"""

	susceptibilities = []
	deltas = []
	delta = 0.0
	for ff in fidelities:
		if ff == fidelities[0]:
			delta = ff[2]
			continue
		else:
			delta = ff[2]


		if len(ff[0]) != fs_reach:
			continue

		overlaps = np.array(ff[0])
		overlaps_abs = np.abs(overlaps)
		logs = -2.0*np.log(overlaps_abs)

		distances = np.array(ff[1])
		denominators = distances*distances

		suscp = logs/denominators

		a,c = linear_model(distances, suscp)

		deltas += [delta]
		
		linear_behaviour = is_linear(suscp, distances)
		if linear_behaviour:
			susceptibilities += [c]
		else:
			susceptibilities += [suscp[0]]

		# plot start
		x = np.linspace(-0.5*distances[0], distances[0]*6, 1000)

		plt.plot(distances, suscp, 'k*')
		plt.plot(0.0, c, 'r.')
		plt.plot(x,a*x+c,'-g')
		plt.ylabel("-2.0 $\\frac{\ln f}{\delta \Delta^2}$")
		plt.xlabel("-$\delta \Delta$")
		plt.xlim(-0.5*distances[0],distances[0]*6)
		if not linear_behaviour:
			plt.title("$\Delta = {d:.6f}$\n".format(d=delta) + \
					"not linear behaviour")
		else:
			plt.title("$\Delta = {d:.6f}$".format(d=delta))
		plt.draw()
		plt.pause(0.01)
		plt.clf()
		# end plot

	return (deltas,susceptibilities)


def main():
	fs_reach = 5
	if len(sys.argv) != 3:
		print("Give filename as the command line argument.")
		print("python "+sys.argv[0]+" dmrg_results.pkl output_name")
		sys.exit(-1)

	out_name = sys.argv[2]
	fidelity_out = 'fidelities_'+out_name+'.pkl'
	stts, dts = get_states(sys.argv[1])

	print("Now overlaps will be computed. It takes a lot of time (5 min)")
	fidelities = fidelity(stts, dts, fs_reach)

	print("OK, done. Now overlaps will be saved to "+fidelity_out)
	with open(fidelity_out, 'wb') as g:
		pickle.dump(fidelities, g)

	"""
	sys.exit(0)
	with open(filename,'rb') as g:
		fidelities = pickle.load(g)
	"""

	plt.ion()
	deltas, susceptibilities = \
	 fidelity_susceptibility_extrapolation(fidelities, fs_reach)


	max_fs = max(susceptibilities)
	idx_c = susceptibilities.index(max_fs)
	delta_c = deltas[idx_c]

	plt.ioff()
	plt.plot(deltas,  susceptibilities)
	plt.xlabel("$\Delta$")
	plt.ylabel("$\chi_\mathrm{FS}$")
	plt.title("Fidelity susceptibility\n extrapolation"+
			" of a linear model to the $\delta\Delta \\rightarrow 0$ limit.\n"+\
					"$\Delta_c = {d:06f}$".format(d=delta_c))
	plt.show()


	fs_out = "fs_"+ out_name + '.tsv'
	out = open(fs_out, 'a+')

	for idx in range(len(deltas)):
		a_line = "{d:.9f}\t{fs:.9f}".format(d=deltas[idx],fs=susceptibilities[idx])
		print(a_line)
		out.write(a_line+"\n")

	out.close()

	return 0

if __name__ == '__main__':
	main()
