# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt

def my_read_tsv(filename):
    data_input = open(filename,'r')
    
    delta = []
    sM = []
    while(True):
        line = data_input.readline().split() 
        if not len(line):
            break
        delta += [float(line[0])]
        sM += [float(line[1])]
    
    return (delta, sM)


def get_data():
    Us = ['100.00', '20.00', '10.000', '9.00', '8.00', '7.75', 
          '7.650', '7.550', 
          '7.500', '7.450', '7.400', '7.350', '7.25', '7.00', '6.00']
    Us = Us[::-1]

    data = []
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'

    for U in Us:
        filename = path + 'U' + U
        delta, sM = my_read_tsv(filename)
        U = [float(U)] * len(Us)
        
        data += [[U, delta, sM]]
    return data


def plot_selected(data, idx=0):
    
    if idx == 0:
        idx = len(data)
    
    for i in range(idx):
        delta = data[i][1]
        sM = data[i][2]
        U = data[i][0][0]
        plt.plot(delta, sM, label = "{:.3f}".format(U))
    
    plt.legend()
    plt.title("Staggered magnetisation for $L = 40$, $\\beta = 0.02$"+\
              "\n bond dimension = 60")
    plt.xlabel("$\Delta$")
    plt.ylabel("sM")
    plt.xlim(0.3,1.2)
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'
    plt.savefig(fname = path +'transition.png', format = 'png',
                dpi=300)
    plt.show()

def main():
    data = get_data()
    
    plot_selected(data)
    
    return 0

if __name__ == '__main__':
    main()