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
    # that was for L40
    
    #Us = ['100.00', '20.00', '10.000', '9.00', '8.00', '7.550', '7.25', '7.00', '6.00', '5.00']
    #Us = Us[::-1]

    #path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/U'
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/L60_sM/'
    Us = ['10000.00', '100.00', '20.00', '15.00', '12.00', '10.00', '9.00']
    Us +=['8.00', '7.75', '7.50', '7.25', '7.00', '5.00' ]
    
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
    # that was for L40
    
    #Us = ['100.00', '20.00', '10.000', '9.00', '8.00', '7.550', '7.25', '7.00', '6.00', '5.00']
    #Us = Us[::-1]

    #path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/U'
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/L60_sM_plot/'
    Us = ['10000.00', '100.00', '20.00', '15.00', '12.00', '10.00', '9.00']
    Us +=['8.00', '7.75', '7.50', '7.25', '7.00', '5.00' ]
    
    data = []

    for U in Us:
        # I will extract only N+1 samples from each data set
        filename = path + U
        delta, sM = my_read_tsv(filename)
        U = [float(U)] * len(sM)
        
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
    cntr2 = ax2.tricontourf(Delta, U, sM, 300, cmap="RdBu_r")
    
    # Found critical points
    # v unsure ones are: 7.50
    Delta_c_left = [0.368, 0.53, 0.624, 0.67, 0.708, 0.766, 0.785, 0.81]
    U_c_left = [10000.0, 20.0, 12.00, 10.0, 9.0, 8.00, 7.75, 7.5]
    Uinv_c_left = [inv(u) for u in U_c_left]
    
    
    # v unsure ones are: 7.50
    Delta_c_right = [0.906, 0.9, 0.91, 0.910, 0.913, 0.908, 0.890, 0.875, 0.85]
    U_c_right = [10000.0, 100.0, 20.0, 12.00, 10.0, 9.0, 8.0, 7.75, 7.5]
    Uinv_c_right = [inv(u) for u in U_c_right]
    
    # this is v rough
    Delta_c_bottom = [0.85, 0.833, 0.825, 0.8]
    U_c_bottom = [7.4, 7.43, 7.44, 7.6]
    Uinv_c_bottom = [inv(u) for u in U_c_bottom]
    
    fig.colorbar(cntr2, ax=ax2, label="staggered magnetisation (for 60 sites)")
    # Plot critical points
    pointsize=5
    ax2.plot(Delta_c_right, Uinv_c_right, 'ko--', ms=pointsize)
    ax2.plot(Delta_c_left, Uinv_c_left, 'ko--', ms=pointsize)
    ax2.plot(Delta_c_bottom, Uinv_c_bottom, 'ko--', ms=pointsize)
    #ax2.plot([0.7], [inv(10,U0)], 'ko-', ms=3)
    #ax2.plot([0.74], [inv(8.5,U0)], 'ko-', ms=3)
    #ax2.plot([0.7], [inv(15,U0)], 'ko-', ms=3)
    #ax2.plot([0.51], [inv(40)], 'ko-', ms=3)
    #ax2.plot([0.85]*2, [inv(7,U0),inv(8,U0)], 'wo--', ms=5)
    ax2.plot([0.80]*2, [inv(7),inv(8)], 'wo--', ms=5)
    #ax2.plot([0.825]*2, [inv(7),inv(8)], 'wo--', ms=5)
    
    # Here are the locations of the data points
    ax2.plot(Delta, U, 'ko', ms=3)
    
    #
    #decorations
    #
    fontcol='w'
    ax2.axis((Deltamin, Deltamax, ymin, ymax))
    ax2.set_title('$\\alpha = 0.5, \\beta = 0.02, t = 1.0, \\rho = 0.5$')
    ax2.text(Deltamin+0.01, inv(10000), 'U = $10^4$', fontsize = 12, color=fontcol)
    ax2.text(Deltamin+0.01, inv(5.3), 'U = 5', fontsize = 12, color=fontcol)
    ax2.text(0.7, inv(25), 'cBOW$_{1/2}$', fontsize = 16, color=fontcol)
    ax2.text(0.4, inv(7.25), 'SF', fontsize = 16, color=fontcol)
    plt.subplots_adjust(hspace=0.5)
    ax2.set_xlabel("$\Delta$")
    ax2.set_ylabel("$1/U$")
    ax2.set_xlim(0.3,Deltamax-0.02)
    ax2.set_ylim(0.0, inv(5.0))
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'
    plt.savefig(fname = path +'phase_diagram.png', format = 'png',
                dpi=300)
    plt.show()

def main():
    data = get_data()
    
    phase_diagram(data)
    
    return 0

if __name__ == '__main__':
    main()