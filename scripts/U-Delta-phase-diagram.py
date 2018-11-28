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

    """ Interpolation curve
    xxx = 0.35+0.41*np.arange(100)/100.0
    aaa = 0.320256
    bbb = -0.11199
    ax2.plot(xxx, xxx*aaa+bbb, 'k-' )
    """ 
    #interpolation results
    U += [0.001349, 0.002598, 0.003847, 0.005096, 0.006345, 0.007594, 0.008843, \
0.010092, 0.011341, 0.01259, 0.013839, 0.015088, 0.016337, 0.017586, \
0.018835, 0.020084, 0.021333, 0.022582, 0.023831, 0.02508, 0.026329, \
0.027578, 0.028827, 0.030076, 0.031325, 0.032574, 0.033823, 0.035072, \
0.036321, 0.03757, 0.038819, 0.040068, 0.041317, 0.042566, 0.043815, \
0.045064, 0.046313, 0.047562, 0.048811, 0.05006, 0.051309, 0.052558, \
0.053807, 0.055056, 0.056305, 0.057554, 0.058803, 0.060052, 0.061301, \
0.06255, 0.063799, 0.065048, 0.066297, 0.067546, 0.068795, 0.070044, \
0.071293, 0.072542, 0.073791, 0.07504, 0.076289, 0.077538, 0.078787, \
0.080036, 0.081285, 0.082534, 0.083783, 0.085032, 0.086281, 0.08753, \
0.088779, 0.090028, 0.091277, 0.092526, 0.093775, 0.095024, 0.096273, \
0.097522, 0.098771, 0.10002, 0.101269, 0.102518, 0.103767, 0.105016, \
0.106265, 0.107514, 0.108763, 0.110012, 0.111261, 0.11251, 0.113759, \
0.115008, 0.116257, 0.117506, 0.118755, 0.120004, 0.121253, 0.122502, \
0.123751, 0.125]
    Delta += [0.35388, 0.35776, 0.36164, 0.36552, 0.3694, 0.37328, 0.37716, \
0.38104, 0.38492, 0.3888, 0.39268, 0.39656, 0.40044, 0.40432, 0.4082, \
0.41208, 0.41596, 0.41984, 0.42372, 0.4276, 0.43148, 0.43536, \
0.43924, 0.44312, 0.447, 0.45088, 0.45476, 0.45864, 0.46252, 0.4664, \
0.47028, 0.47416, 0.47804, 0.48192, 0.4858, 0.48968, 0.49356, \
0.49744, 0.50132, 0.5052, 0.50908, 0.51296, 0.51684, 0.52072, 0.5246, \
0.52848, 0.53236, 0.53624, 0.54012, 0.544, 0.54788, 0.55176, 0.55564, \
0.55952, 0.5634, 0.56728, 0.57116, 0.57504, 0.57892, 0.5828, 0.58668, \
0.59056, 0.59444, 0.59832, 0.6022, 0.60608, 0.60996, 0.61384, \
0.61772, 0.6216, 0.62548, 0.62936, 0.63324, 0.63712, 0.641, 0.64488, \
0.64876, 0.65264, 0.65652, 0.6604, 0.66428, 0.66816, 0.67204, \
0.67592, 0.6798, 0.68368, 0.68756, 0.69144, 0.69532, 0.6992, 0.70308, \
0.70696, 0.71084, 0.71472, 0.7186, 0.72248, 0.72636, 0.73024, \
0.73412, 0.738]
    sM +=[0.0990801, 0.099059, 0.0990379, 0.0990168, 0.0989957, 0.0989746, \
0.0989535, 0.0989324, 0.0989113, 0.0988902, 0.0988691, 0.098848, \
0.0988269, 0.0988057, 0.0987846, 0.0987635, 0.0987424, 0.0987213, \
0.0987002, 0.0986791, 0.098658, 0.0986369, 0.0986158, 0.0985947, \
0.0985736, 0.0985525, 0.0985314, 0.0985103, 0.0984892, 0.0984681, \
0.098447, 0.0984258, 0.0984047, 0.0983836, 0.0983625, 0.0983414, \
0.0983203, 0.0982992, 0.0982781, 0.098257, 0.0982359, 0.0982148, \
0.0981937, 0.0981726, 0.0981515, 0.0981304, 0.0981093, 0.0980882, \
0.098067, 0.0980459, 0.0980248, 0.0980037, 0.0979826, 0.0979615, \
0.0979404, 0.0979193, 0.0978982, 0.0978771, 0.097856, 0.0978349, \
0.0978138, 0.0977927, 0.0977716, 0.0977505, 0.0977294, 0.0977083, \
0.0976871, 0.097666, 0.0976449, 0.0976238, 0.0976027, 0.0975816, \
0.0975605, 0.0975394, 0.0975183, 0.0974972, 0.0974761, 0.097455, \
0.0974339, 0.0974128, 0.0973917, 0.0973706, 0.0973495, 0.0973284, \
0.0973072, 0.0972861, 0.097265, 0.0972439, 0.0972228, 0.0972017, \
0.0971806, 0.0971595, 0.0971384, 0.0971173, 0.0970962, 0.0970751, \
0.097054, 0.0970329, 0.0970118, 0.0969907]
    """ """ 
    
    
    fig, ax2 = plt.subplots()
    # ----------
    # Tricontour
    # ----------
    ax2.tricontour(Delta, U, sM, 10, linewidths=0, colors='k')
    cntr2 = ax2.tricontourf(Delta, U, sM, 300, cmap="Oranges")
    
    # The critical points
    Delta_c_left = [0.367, 0.4, 0.454, 0.53, 0.582, 0.624, 0.67, 0.708, 0.766, 0.785]
    U_c_left = [10000.0, 100.0, 40.0, 20.0, 15.00, 12.00, 10.0, 9.0, 8.00, 7.75]
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
    path = '/home/pwojcik/bosons_on_lattice/Utransition/Phase_diagram/'
    plt.savefig(fname = path +'phase_diagram.png', format = 'png',
                dpi=300)
    plt.show()

def main():
    data = get_data()
    
    phase_diagram(data)
    
    return 0

if __name__ == '__main__':
    main()
