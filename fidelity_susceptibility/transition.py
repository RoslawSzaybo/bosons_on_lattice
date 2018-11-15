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
    plt.xlabel('$\Delta$')
    plt.ylabel('$\chi_F$')
    plt.show()
    return 0

def find_max_08(data):
    big = [x for x in data if x[0] > 0.85]
    return max(big, key = my_fs_key)

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
    plt.title('$\Delta_c$ = {:.3}'.format(c))
    return 0

def show_fs_together(data, Uname, show_peak=True):
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

    plt.title('fidelity susceptibility scaling for $U = $' + Uname)
    plt.xlabel('$\Delta$')
    plt.grid()
    plt.ylabel('$\chi_F$')
    plt.legend()

    plt.show()   
    return 0

# scratch
def show_fs_together_prim(data, Uname):
    for dd in data:
        xy = [list(x) for x in zip(*dd[0])] # transposition
        plt.plot(xy[0], xy[1], '-', label = str(dd[1]))

    plt.title('fidelity susceptibility scaling for $U = $' + Uname)
    plt.xlabel('$\Delta$')
    plt.ylabel('$\chi_F$')
    plt.legend()

    plt.show()
    return 0
    
def all_fs():
    path = '/home/pwojcik/bosons_on_lattice/fidelity_susceptibility/Utransition/'
    ## U7.75
    names = []
    names += [[path + 'fs_U7.75_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U7.75_L40_ch80.tsv', 40]]
    ## U20
    names = []    
    names += [[path + 'fs_U20_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U20_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U20_L40_ch60.tsv', 40]]
    ## U100
    names = []
    names += [[path + 'fs_U100_L60_ch80.tsv', 60]]   
    names += [[path + 'fs_U100_L40_ch60.tsv', 40]]
    ## U9
    names = []
    names += [[path + 'fs_U9.00_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U9.00_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U9.00_L40_ch60.tsv', 40]]
    ## U7.75
    names = []
    names += [[path + 'fs_U7.50_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.50_L40_ch80.tsv', 40]]

    Uname = names[0][0].split('_')[-3][1:]
    data = []
    for nL in names:
        fidelity_sus = my_read_tsv(nL[0])
        narrow_D_fs = [x for x in fidelity_sus if x[0] > 0.60]
        data += [[narrow_D_fs, nL[1]]]
    
    show_fs_together_prim(data, Uname)    
    return 0
    
def Delta_c(high=True):
    path = '/home/pwojcik/bosons_on_lattice/fidelity_susceptibility/Utransition/'
    ## U100
    names = []
    names += [[path + 'fs_U100_L60_ch80.tsv', 60]]   
    names += [[path + 'fs_U100_L40_ch60.tsv', 40]]
    ## U9
    names = []
    names += [[path + 'fs_U9.00_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U9.00_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U9.00_L40_ch60.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U7.50_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.50_L40_ch80.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U7.25_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.25_L40_ch80.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U7.25_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.25_L40_ch80.tsv', 40]]
    ## U7.75
    names = []
    names += [[path + 'fs_U7.75_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U7.75_L40_ch80.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U7.00_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.00_L40_ch80.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U7.30_L60L_ch70dwn.tsv', 60]]
    ## 
    names = []
    names += [[path + 'fs_U7.40_L60L_ch70dwn.tsv', 60]]
    ## 
    names = []
    names += [[path + 'fs_U7.60_L60L_ch70dwn.tsv', 60]]
    ## 
    names = []
    names += [[path + 'fs_U7.00_L60_ch80.tsv', 60]]
    names += [[path + 'fs_U7.00_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U7.00_L40_ch60.tsv', 40]]
    ## 
    names = []
    names += [[path + 'fs_U8.00_L60_ch80.tsv', 60]]
    ## U20
    names = []    
    names += [[path + 'fs_U20_L60_ch80.tsv', 60]]
    #names += [[path + 'fs_U20_L50_ch80.tsv', 50]]
    names += [[path + 'fs_U20_L40_ch60.tsv', 40]]

    path = '/home/pwojcik/bosons_on_lattice/fidelity_susceptibility/U10_B02_D9/'
    names = []    
    names += [[path + 'fs_L60_ch80.tsv', 60]]
    names += [[path + 'fs_L50_ch80.tsv', 50]]
    names += [[path + 'fs_L40_ch80.tsv', 40]]
    names += [[path + 'fs_L30_ch80.tsv', 30]]

    Uname = names[0][0].split('_')[-3][1:]
    data = []
    Ls = []
    Dcs = []
    for nL in names:
        Ls += [ nL[1] ]        
        fidelity_sus = my_read_tsv(nL[0])
        if high:
            narrow_D_fs = [x for x in fidelity_sus if x[0]>0.88]
        else:
            narrow_D_fs = [x for x in fidelity_sus if x[0]<0.85 and x[0]>0.3]
            
        pair = max(narrow_D_fs, key = my_fs_key)
        Dcs += [pair[0]]
        
        data += [[narrow_D_fs, nL[1]]]
    
    show_fs_together(data, Uname)
    
    find_limit(Ls, Dcs)     
    return 0
    
def main():
    Delta_c()
    
    return 

if __name__ == '__main__':
	main()
