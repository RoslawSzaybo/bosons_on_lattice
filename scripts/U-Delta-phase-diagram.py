# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import matplotlib.tri as tri
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


def get_data():
    Us = ['100.00', '20.00', '10.000', '9.00', '8.00', '7.550',  
          '7.25', '7.00', '6.00']    
    Us = Us[::-1]

    data = []
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'

    for U in Us:
        # I will extract only N+1 samples from each data set
        N = 8
        filename = path + 'U' + U
        delta, sM = my_read_tsv(filename)
        U = [float(U)] * len(sM)
        
        idces = (np.arange(N)*len(sM))//N
        np.append(idces,len(sM)-1)
        idces = np.unique(idces)
        
        data += [[list(np.array(U)[idces]), 
                  list(np.array(delta)[idces]), 
                  list(np.array(sM)[idces]) ]]
    return data

def inv(U, U0):
    return 1.0/(U-U0)

def phase_diagram(data):
    # source 
    # https://matplotlib.org/gallery/images_contours_and_fields/
    # irregulardatagrid.html#sphx-glr-gallery-images-contours-and-
    # fields-irregulardatagrid-py
    # -------------------------
    # Prepare data
    # ------------------------
    U0 = 2
    Umin, Umax = (6.0, 100.0)
    ymax, ymin = (inv(Umax, U0), inv(Umin, U0))
    Deltamin, Deltamax = (0.65, 0.96)
    U = []
    Delta = []
    sM = []
    
    for i in range(len(data)):
        locU = np.array(data[i][0])
        U += list( 1.0/(locU - U0) )
        Delta += data[i][1]
        sM += data[i][2]
           
    fig, ax2 = plt.subplots()
    # ----------
    # Tricontour
    # ----------
    ax2.tricontour(Delta, U, sM, 10, linewidths=0, colors='k')
    cntr2 = ax2.tricontourf(Delta, U, sM, 200, cmap="RdBu_r")
    
    # Found critical points
    Delta_c_left = [0.53, 0.708, 0.766, 0.785]
    U_c_left = [20.0, 9.0, 8.00, 7.75]
    Uinv_c_left = [inv(u, U0) for u in U_c_left]
    
    Delta_c_right = [0.9, 0.91, 0.913, 0.9, 0.894, 0.875]
    U_c_right = [100.0, 20.0, 10.0, 9.0, 8.0, 7.75]
    Uinv_c_right = [inv(u, U0) for u in U_c_right]
    
    fig.colorbar(cntr2, ax=ax2, label="staggered magnetisation")
    # Plot critical points
    ax2.plot(Delta_c_right, Uinv_c_right, 'ko--', ms=3)
    ax2.plot(Delta_c_left, Uinv_c_left, 'ko--', ms=3)
    #ax2.plot([0.7], [inv(10,U0)], 'ko-', ms=3)
    #ax2.plot([0.7], [inv(12,U0)], 'ko-', ms=3)
    #ax2.plot([0.7], [inv(15,U0)], 'ko-', ms=3)
    #ax2.plot([0.7], [inv(40,U0)], 'ko-', ms=3)
    #ax2.plot([0.85]*2, [inv(7,U0),inv(8,U0)], 'wo--', ms=5)
    #ax2.plot([0.80]*2, [inv(7,U0),inv(8,U0)], 'wo--', ms=5)
    #ax2.plot([0.825]*2, [inv(7,U0),inv(8,U0)], 'wo--', ms=5)
    #ax2.plot(Delta, U, 'ko', ms=3)
    ax2.axis((Deltamin, Deltamax, ymin, ymax))
    ax2.set_title('$\\alpha = 0.5, \\beta = 0.02, t = 1.0, \\rho = 0.5$')
    ax2.text(Deltamin+0.01, inv(20, U0), 'U = 20', fontsize = 12, color='white')
    ax2.text(Deltamin+0.01, inv(6, U0), 'U = 6', fontsize = 12, color='white')
    ax2.text(0.725, inv(25, U0), 'cBOW$_{1/2}$', fontsize = 16, color='white')
    plt.subplots_adjust(hspace=0.5)
    ax2.set_xlabel("$\Delta$")
    ax2.set_ylabel("$1/(U-5.9)$")
    path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'
    plt.savefig(fname = path +'phase_diagram.eps', format = 'eps',
                dpi=300)
    plt.show()

def phase_diagram_B(data):
    # source 
    # https://matplotlib.org/gallery/images_contours_and_fields/
    # irregulardatagrid.html#sphx-glr-gallery-images-contours-and-
    # fields-irregulardatagrid-py
    # -------------------------
    # Prepare data
    # ------------------------
    U0 = 4.9
    Umin, Umax = (6.0, 100.0)
    ymin, ymax = (inv(Umax, U0), inv(Umin, U0))
    Deltamin, Deltamax = (0.7, 1.0)
    U = []
    Delta = []
    sM = []
    
    for i in range(len(data)):
        locU = np.array(data[i][0])
        U += list(1.0/(locU - U0))
        Delta += data[i][1]
        sM += data[i][2]
        
    # -----------------------
    # Interpolation on a grid
    # -----------------------
    # A contour plot of irregularly spaced data coordinates
    # via interpolation on a grid.
    ngridx = 200
    ngridy = 200
    
    # Create grid values first.
    xi = np.linspace(ymin, ymax, ngridx)
    yi = np.linspace(Deltamin, Deltamax, ngridy)
    
    # Perform linear interpolation of the data (x,U)
    # on a grid defined by (xi,yi)
    triang = tri.Triangulation(U, Delta)
    interpolator = tri.LinearTriInterpolator(triang, sM)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    
    fig, ax = plt.subplots()
    
    ax.contour(xi, yi, zi, 0, linewidths=0.5, colors='k')
    cntr1 = ax.contourf(xi, yi, zi, 100, cmap="RdBu_r")
    
    fig.colorbar(cntr1, ax=ax)
    ax.plot(Delta, U, 'ko', ms=3)
    ax.axis((Deltamin, Deltamax, ymin, ymax))
    ax.set_title('grid and contour (%d points, %d grid points)')
    ax.set_xlabel("$\Delta$")
    ax.set_ylabel("U")
    
    plt.show()
    
    #plt.title("Phase diagram")
    #path = '/home/pwojcik/bosons_on_lattice/Utransition/results/sM/'
    #plt.savefig(fname = path +'transition.png', format = 'png',
    #            dpi=300)
    #plt.show()

def main():
    data = get_data()
    
    phase_diagram(data)
    
    return 0

if __name__ == '__main__':
    main()