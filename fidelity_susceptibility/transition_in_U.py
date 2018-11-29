#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 23 12:25:12 2018

This code gives the point where fidelity susceptibility predicts phase 
transition. 
"""

import numpy as np
import matplotlib.pyplot as plt

def my_key(d):
    return d[0]

def my_fs_key(d):
    return d[1]

def my_read_tsv(name):
    data = open(file = name, mode = 'r', newline = '\n')
    pairs = []
    while(1):
        line = data.readline()[:-1]
        if not len(line):
            break
        lnsplt = line.split('\t')
        pairs += [[float(lnsplt[0]), float(lnsplt[1])]]
    pairs.sort(key = my_key)
    return pairs
#    return [list(x) for x in zip(*raw_data)] # transposition

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

def show_fs(pairs, pair):
    data = [list(x) for x in zip(*pairs)] # transposition
    
    plt.plot(data[0], data[1], '-')
    plt.scatter(pair[0], pair[1], c='blue')
    plt.title('fidelity susceptibility')
    plt.xlabel('$U$')
    plt.ylabel('$\chi_F$')
    plt.show()
    return 0

def find_limit(Ls, D):
    one_over_L = [1/l for l in Ls]
    
    if len(D) == 1:
        c = D[0]
    else:
        a,c = linear_model(one_over_L, D)
        x = np.arange(0, one_over_L[1], one_over_L[1]/100.0) 
        plt.plot(x, a*x+c, 'k-')
    
    plt.scatter(one_over_L, D, c='blue')
    plt.scatter(0.0, c, c='r')
    plt.xlabel('$\\frac{1}{L}$')
    plt.ylabel('$\Delta_\mathrm{C}$')
    plt.title('$U_c$ = {:.3}'.format(c))
    return 0

def show_fs_together(data, Deltaname, show_peak=True):
    Ls = []
    Dcs = []
    for dd in data:
        xy = [list(x) for x in zip(*dd[0])] # transposition
        plt.plot(xy[0], xy[1], '-', label = str(dd[1]))
        Ls += [dd[1]]
        # peak values
        pair = max(dd[0], key = my_fs_key)
        plt.scatter(pair[0], pair[1], c='blue')
        Dcs += [pair[0]]

    plt.title('fidelity susceptibility scaling for $\Delta = $' + Deltaname)
    plt.xlabel('$U$')
    plt.grid()
    plt.ylabel('$\chi_F$')
    plt.legend()

    plt.show()   
    return 0

def U_c():
    path = '/home/pwojcik/bosons_on_lattice/fidelity_susceptibility/Utransition/'
    #Delta 0.800
    names = []
    names += [[path+'fs_D0.800_L60_ch80.tsv',60]]
    names += [[path+'fs_D0.800_L50_ch80.tsv',50]]
    names += [[path+'fs_D0.800_L40_ch80.tsv',40]]
    #Delta 0.825
    names = []
    names += [[path+'fs_D0.825_L60_ch80.tsv',60]]
    names += [[path+'fs_D0.825_L50_ch80.tsv',50]]
    names += [[path+'fs_D0.825_L40_ch80.tsv',40]]
    #Delta 0.850
    names = []
    names += [[path+'fs_D0.850_L60_ch80.tsv',60]]
    names += [[path+'fs_D0.850_L50_ch80.tsv',50]]
    names += [[path+'fs_D0.850_L40_ch80.tsv',40]]
    #Delta 0.863
    names = []
    names += [[path+'fs_D0.863_L60_ch80.tsv',60]]
    names += [[path+'fs_D0.863_L50_ch80.tsv',50]]
    names += [[path+'fs_D0.863_L40_ch80.tsv',40]]

    Deltaname = names[0][0].split('_')[-3][1:]
    data = []
    Ls = []
    Ucs = []
    for nL in names:
        Ls += [ nL[1] ]        
        fidelity_sus = my_read_tsv(nL[0])
        pair = max(fidelity_sus, key = my_fs_key)
        Ucs += [pair[0]]
        
        data += [[fidelity_sus, nL[1]]]
    
    show_fs_together(data, Deltaname)
    
    find_limit(Ls, Ucs)     
    return 0
    
def main():
    U_c()
    
    return 

if __name__ == '__main__':
	main()
