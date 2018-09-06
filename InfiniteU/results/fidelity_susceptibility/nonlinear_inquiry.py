#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Sep 6 14:54:12 2018

This program allows to look closely on a selected fidelity susceptibility computations.
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


def fidelity_susceptibility_interface(fidelities, delta, fs_reach):
	deltas = [dd[2] for dd in fidelities]
	if not delta in deltas:
		print("There is no entry for delta = {}".format(delta) +\
				" in given fidelities.")
		print("Choose one of the following:")
		print(deltas)
		sys.exit(-1)

	idx = deltas.index(delta)
	ff = fidelities[idx]

	if len(ff[0]) != fs_reach:
		print("Sorry, len(ff[0]) != fs_reach!")
		print("Pick different delta or get refined fidelities.")
		sys.exit(-1)
	return ff

def get_fidelity_fractions_and_ddeltas(ff):
	""" 
		limit of fractions at $\delta\Delta \rightarrow 0$ is
		the fidelity susceptibility. A fraction is the only 
		fraction on the right hand side of eq. (6) in
		PRL, 76, 022101, (2007)
	"""
	overlaps = np.array(ff[0])
	overlaps_abs = np.abs(overlaps)
	logs = -2.0*np.log(overlaps_abs)

	ddeltas = np.array(ff[1])
	denominators = ddeltas*ddeltas
	fractions = logs/denominators

	return (fractions, ddeltas)

def plot_fractions_as_ddeltas(fractions, distances, a, c, linear_behaviour,
		delta):

	# initiall rescalling
	rescaled = [1000*dd for dd in distances]
	distances = rescaled

	x_span = distances[-1] - distances[0]	
	xmin = -0.05*x_span
	xmax = distances[-1] + 0.05*x_span
	x = np.linspace(xmin, xmax, 1000)


	fig = plt.figure(figsize=(4,3))
	plt.plot(x, a*x/1000+c, color = 'k', linestyle = '--', 
			label = 'linear fit')
	plt.plot(distances, fractions, 'k*', 
			label = "$\\frac{-2 \ln F_i}{\delta\Delta_i^2}$")
	plt.plot(0.0, c, 'r*', markeredgecolor = 'k', markersize = 12,
			label = "$\chi_{F}(\Delta)$" +  " = {:.0f}".format(c))
	plt.ylabel("$-2\ln F\ /\ \delta \Delta^2$")
	plt.xlabel("$1000\cdot\delta \Delta$")
	plt.xlim(xmin, xmax)
	if not linear_behaviour:
		plt.title("$\Delta = {d:.6f}$\n".format(d=delta) + \
				"not linear behaviour")
		print("{}".format(delta))
	else:
		plt.title("$\Delta = {d:.6f}$".format(d=delta))
	plt.legend()
	plt.subplots_adjust(left=0.20,bottom=0.15,top=0.85)
	"""
	plt.savefig(filename, dpi=300, bbox_inches ='tight',
			format = 'eps')
	"""
	plt.show()
	plt.clf()

def show_fidelity_susceptibility_at_delta(fidelities, delta, fs_reach):
	"""
	arguments:
	fidelistes	list of triples [a,b,c] a is a list of overlaps of ground states
										b is a list of $\delta\Delta$'s
										c is the value of delta for which the ovelaps are computed
	delta 		value at which one wants to look at the delta
	fs_reach	an integer which gives a number of points where I look for a linear behaviour
	"""

	ff = fidelity_susceptibility_interface(fidelities, delta, fs_reach)
	fractions, distances = get_fidelity_fractions_and_ddeltas(ff)
	a,c = linear_model(distances, fractions)
	linear_behaviour = is_linear(fractions, distances)
	plot_fractions_as_ddeltas(fractions, distances, a, c, 
			linear_behaviour, delta)

	return 0


def main():
	fs_reach = 5
	if len(sys.argv) != 3:
		print("Give filename as the command line argument.")
		print("python "+sys.argv[0]+" fidelities.pkl delta")
		sys.exit(-1)

	fidelity_filename = sys.argv[1]
	with open(fidelity_filename,'rb') as g:
		fidelities = pickle.load(g)

	delta = float(sys.argv[2])
	show_fidelity_susceptibility_at_delta(fidelities, delta, fs_reach)

	return 0

if __name__ == '__main__':
	main()

