# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np

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


def get_data_altarnative():
    # this function can be ignored
    # this version extracts only N+1 poinst from each data curves
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/L60_sM/'
    Us = ['10000.00', '100.00', '40.00', '20.00', '15.00', '12.00', '10.00']
    Us +=['9.00', '8.00', '7.75', '7.50', '7.25', '7.00', '5.00' ]
    
    data = []

    for U in Us:
        # I will extract only N+1 samples from each data set
        N = 10
        filename = path + U
        delta, sM = my_read_tsv(filename)
        U = [float(U)] * len(sM)
        
        idces = (np.arange(N)*len(sM))//N
        np.append(idces,len(sM)-1)
        idces = np.unique(idces)
        
        data += [[list(np.array(U)[idces]), 
                  list(np.array(delta)[idces]), 
                  list(np.array(sM)[idces]) ]]
    return data

def get_data():
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/L60_sM/'
    Us = ['10000.00', '100.00', '40.00', '20.00', '15.00', '12.00', '10.00']
    Us +=['9.00', '8.00', '7.75', '7.50', '7.25', '7.00', '5.00' ]
    
    data = []

    for U in Us:
        filename = path + U
        delta, sM = my_read_tsv(filename)
        U = [float(U)] * len(sM)
        
        sM = list(np.abs(sM))
        
        data += [[U, delta, sM]]
    return data


def inv(U):
    return 1.0/U

def phase_diagram(data):
    # source 
    # https://matplotlib.org/gallery/images_contours_and_fields/
    # irregulardatagrid.html#sphx-glr-gallery-images-contours-and-
    # fields-irregulardatagrid-py
    
    # -------------------------
    # Prepare data
    # ------------------------
    Umin, Umax = (6.0, 100.0)
    ymax, ymin = (inv(Umin), inv(Umax))
    Deltamin, Deltamax = (0.65, 0.96)
    U = []
    Delta = []
    sM = []
    
    for i in range(len(data)):
        locU = np.array(data[i][0])
        U += list( 1.0/locU )
        Delta += data[i][1]
        sM += data[i][2]
           
    fig, ax2 = plt.subplots()
    # ----------
    # Tricontour
    # ----------
    ax2.tricontour(Delta, U, sM, 10, linewidths=0, colors='k')
    cntr2 = ax2.tricontourf(Delta, U, sM, 300, cmap="Oranges")
    
    # The critical points
    Delta_c_left = [0.367, 0.4, 0.53, 0.624, 0.67, 0.708, 0.766, 0.785]
    U_c_left = [10000.0, 100.0, 20.0, 12.00, 10.0, 9.0, 8.00, 7.75]
    Uinv_c_left = [inv(u) for u in U_c_left]
    #
    Delta_c_right = [0.906, 0.9, 0.907, 0.91, 0.907, 0.910, 0.913, 0.908, 0.890, 0.875]
    U_c_right = [10000.0, 100.0, 40.0, 20.0, 15.0, 12.00, 10.0, 9.0, 8.0, 7.75]
    Uinv_c_right = [inv(u) for u in U_c_right]
    # 
    Delta_c_bottom = [0.85, 0.825, 0.8]
    U_c_bottom = [7.4, 7.44, 7.6]
    Uinv_c_bottom = [inv(u) for u in U_c_bottom]
    #
    Delta_c = Delta_c_left + Delta_c_bottom[::-1] +  Delta_c_right[::-1]
    U_c_inv = Uinv_c_left + Uinv_c_bottom[::-1] + Uinv_c_right[::-1]
    
    fig.colorbar(cntr2, ax=ax2, label="staggered magnetisation (for 60 sites)")
    # Plot critical points
    pointsize=4
    ax2.plot(Delta_c, U_c_inv, 'ko--', ms=pointsize)
    #   
    # Here are the locations of the data points
    #ax2.plot(Delta, U, 'ko', ms=3)
    #
    #
    #decorations
    #
    fontcol='k'
    ax2.axis((Deltamin, Deltamax, ymin, ymax))
    ax2.set_title('$\\alpha = 0.5, \\beta = 0.02, t = 1.0, \\rho = 0.5$')
    ax2.text(Deltamin+0.01, inv(10000), 'U = $10^4$', fontsize = 12, color=fontcol)
    ax2.text(Deltamin+0.01, inv(5.3), 'U = 5', fontsize = 12, color=fontcol)
    ax2.text(0.7, inv(25), 'cBOW$_{1/2}$', fontsize = 16, color=fontcol)
    ax2.text(0.4, inv(7.25), 'SF', fontsize = 16, color=fontcol)
    plt.subplots_adjust(hspace=0.5)
    ax2.set_xlabel("$\Delta$")
    ax2.set_ylabel("$1/U$")
    ax2.set_xlim(0.32,0.95)
    ax2.set_ylim(0.0, inv(5.0))
    # save result
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/'
    plt.savefig(fname = path +'phase_diagram.png', format = 'png',
                dpi=300)
    plt.show()

def main():
    data = get_data()
    
    phase_diagram(data)
    
    return 0

if __name__ == '__main__':
    main()