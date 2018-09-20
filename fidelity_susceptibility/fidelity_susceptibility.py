#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 23 12:25:12 2018

This program computes fidelity susceptibility. It uses the file prepared by program fidelity.py 
as an input.

It returns the values of fidelity susceptibility at all values of delta in a segment.
Also, all deltas for which nonlinear behaviour was detected are printed to stdout.

Issue:
	There are regions where the behaviour of 
	$\Chi(\delta\Delta) = -2\ln(|\langle \Psi(\Delta) | \Psi(\Delta +\delta\Delta) \rangle)|)/\delta\Delta^2$
	is not linear in $\delta\Delta$. Therefore the limit $\delta\Delta \rightarrow 0$ 
	in that region is not just an intersection of the linear fit to $\Chi(\delta\Delta)$ with the 
	$\delta\Delta = 0$ axis.

	Such region is located in the nearest neighbourhood of the phase transition. The 
	linear behaviour will appear only after the sampling of the region will become finer. 

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
	diff_from_lin_model = abs(yvalues[-1] - lin_model_last_y_value) 

	the_ratio = diff_from_lin_model/first_jump

	return (the_ratio < arbitrary_limit)

def get_fidelity_susceptibility(fidelities, fs_reach):
	"""
	arguments:
	fidelistes	list of pairs [a,b] a is a list of overlaps of ground states
									b is a list of $\delta\Delta$'s
	fs_reach	an integer which gives a number of points where I look for a linear behaviour
	"""

	susceptibilities = []
	deltas = []
	delta = 0.0
	for ff in fidelities:
		delta = ff[2]
		if ff == fidelities[0]:
			continue

		if len(ff[0]) != fs_reach:
			continue

		overlaps = np.array(ff[0])
		overlaps_abs = np.abs(overlaps)
		logs = -2.0*np.log(overlaps_abs)

		distances = np.array(ff[1])
		denominators = distances*distances

		fractions = logs/denominators

		a,c = linear_model(distances, fractions)

		deltas += [delta]
		
		linear_behaviour = is_linear(fractions, distances)
		if linear_behaviour:
			susceptibilities += [c]
		else:
			susceptibilities += [fractions[0]]

		# plot starts
		x = np.linspace(-0.5*distances[0], distances[0]*6, 1000)

		plt.plot(x,a*x+c, color = 'grey', linestyle = '--', 
				label = 'linear fit')
		plt.plot(distances, fractions, 'k*', 
				label = "$\\frac{-2 \ln F_i}{\delta\Delta_i^2}$")
		plt.plot(0.0, c, 'r*', label = "$\chi_{F}$")
		plt.ylabel("-2.0 $\\frac{\ln f}{\delta \Delta^2}$")
		plt.xlabel("-$\delta \Delta$")
		plt.xlim(-0.5*distances[0],distances[0]*6)
		if not linear_behaviour:
			plt.title("$\Delta = {d:.6f}$\n".format(d=delta) + \
					"not linear behaviour")
			print("{}".format(delta))
		else:
			plt.title("$\Delta = {d:.6f}$".format(d=delta))
		plt.draw()
		plt.pause(0.01)
		plt.legend()
		#plt.show()
		plt.clf()
		# end plot

	return (deltas,susceptibilities)

def get_critical_delta(susceptibilities, deltas):
	max_fs = max(susceptibilities)
	idx_c = susceptibilities.index(max_fs)
	delta_c = deltas[idx_c]
	return delta_c

def main():
	fs_reach = 5
	if len(sys.argv) != 3:
		print("Give filename as the command line argument.")
		print("python "+sys.argv[0]+" fidelities.pkl fidelity_susceptibility.tsv")
		sys.exit(-1)

	fidelity_filename = sys.argv[1]

	with open(fidelity_filename,'rb') as g:
		fidelities = pickle.load(g)

	plt.ion()
	deltas, susceptibilities = \
	 get_fidelity_susceptibility(fidelities, fs_reach)

	delta_c = get_critical_delta(susceptibilities, deltas)

	plt.ioff()
	plt.plot(deltas,  susceptibilities)
	plt.xlabel("$\Delta$")
	plt.ylabel("$\chi_\mathrm{FS}$")
	plt.title("Fidelity susceptibility\n extrapolation"+
			" of a linear model to the $\delta\Delta \\rightarrow 0$ limit.\n"+\
					"$\Delta_c = {d:06f}$".format(d=delta_c))
	plt.show()

	fs_out = sys.argv[2] 
	out = open(fs_out, 'a+')

	for idx, susc in enumerate(susceptibilities):
		a_line = "{d:.9f}\t{fs:.9f}".format(d=deltas[idx],fs=susc)
		print(a_line)
		out.write(a_line+"\n")

	out.close()

	return 0

if __name__ == '__main__':
	main()
