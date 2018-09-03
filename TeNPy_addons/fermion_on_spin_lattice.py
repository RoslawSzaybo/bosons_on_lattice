""" 
    Fermionic Bose-Hubbard chain on spin lattice model.
"""
# Copyright 2018 TeNPy Developers

from tenpy.models.lattice import Chain
from tenpy.networks.site import DoubleSite, SpinHalfSite
from tenpy.models.model import CouplingModel, NearestNeighborModel, MPOModel
from tenpy.tools.params import get_parameter, unused_parameters
from tenpy.tools.misc import any_nonzero

class FermionOnSpinLattice(CouplingModel, MPOModel, NearestNeighborModel):
    r"""Spinless Bose-Hubbard model on a chain with spins on each bond.

    Hamiltonian:
    .. math ::
        H = -t \sum_i (b_i^{\dagger} b_{i+1} + b_{i+1}^{\dagger} b_i)
            + \frac{U}{2} \sum_i n_i (n_i - 1) - \mu \sum_i n_i
            - \alpha \sum_i (b_i^{\dagger} \sigma^{z}_i b_{i+1} + b_{i+1}^{\dagger}\sigma^{z}_i b_i)
            + \frac{\Delta}{2}\sum_i \sigma^z_i + \beta \sum_i \sigma^x_i

    For reference on this model see arXiv:1802.05689v1
    
    I one takes formally U = +\infty so that effectively bosons become fermions. 
    To simulate this fermions I use SpinHalfSite where spin up means that 
    there is a boson on-site and spin down means that there is no boson on-site.
    .. math ::
        H = -t \sum_i (a_i^{\dagger} a_{i+1} + a_{i+1}^{\dagger} a_i)
            - \alpha \sum_i (a_i^{\dagger} \sigma^{z}_i a_{i+1} + a_{i+1}^{\dagger}\sigma^{z}_i a_i)
            + \frac{\Delta}{2}\sum_i \sigma^z_i + \beta \sum_i \sigma^x_i
    
    parameter $\mu$ becomes irrelevat here.
    
    All parameters are collected in a single dictionary `model_param` and read out with
    :func:`~tenpy.tools.params.get_parameter`.

    Parameters
    ----------
    L : int
        Length of the chain
    conserve_fermionic_boson: {'Sz' | 'parity' | None}
        What should be conserved. See :class:`~tenpy.networks.Site.SpinHalfSite`, here 
        conservation of Sz is an analog of the number of particles conservation 
        in the boson_spin model.
    conserve_spin: 'parity' | None
        What should be conserved. See :class:`~tenpy.networks.Site.SpinHalfSite`.
    t, alpha, beta, delta : float | array
        Couplings as defined in the Hamiltonian above.
    bc_MPS : {'finite' | 'infinte'}
        MPS boundary conditions. Coupling boundary conditions are chosen appropriately.
    verbose : int
        Level of verbosity
    """

    def __init__(self, model_param):
        # 0) Read and set parameters.
        L = get_parameter(model_param, 'L', 1, self.__class__)
        bc_MPS = get_parameter(model_param, 'bc_MPS', 'finite', self.__class__)
        t = get_parameter(model_param, 't', 1., self.__class__)
        alpha = get_parameter(model_param, 'alpha', 1.0, self.__class__)
        delta = get_parameter(model_param, 'delta', 1.0, self.__class__)
        beta = get_parameter(model_param, 'beta', 1.0, self.__class__)
        conserve_fermionic_boson = get_parameter(model_param, \
                            'conserve_fermionic_boson', 'Sz', self.__class__)
        conserve_spin = get_parameter(model_param, 'conserve_spin', None, self.__class__)
        unused_parameters(model_param, self.__class__)

        # 1) Sites and lattice.
        boson_site = SpinHalfSite(conserve=conserve_fermionic_boson,)
        bond_spin = SpinHalfSite(conserve=conserve_spin)
        double_site = DoubleSite(site0=boson_site, site1=bond_spin, label0='0', 
                          label1='1', charges='independent')
#        lat = Lattice(Ls=[1], unit_cell=[bond_spin], order='default', bc_MPS=bc_MPS, 
#                      basis=None, positions=None)
        lat = Chain(L=L, site=double_site, bc_MPS='finite')

        # 2) Initialize CouplingModel
        bc_coupling = 'periodic' if bc_MPS == 'infinite' else 'open'
        CouplingModel.__init__(self, lat, bc_coupling)

        # 3) Build the Hamiltonian.
        # 3a) on-site terms
        self.add_onsite(delta/2.0, 0, 'Sigmaz1')
        self.add_onsite(beta, 0, 'Sigmax1')

        # 3b) coupling terms.
        # 3bi) standard Bose-Hubbard coupling terms
        self.add_coupling(-t, 0, 'Sp0', 0, 'Sm0', 1)
        self.add_coupling(-t, 0, 'Sm0', 0, 'Sp0', 1)
        # 3bii) coupling on site bosons to bond spin
        self.add_coupling(-alpha, 0, 'Sp0 Sigmaz1', 0, 'Sm0', 1) 
        self.add_coupling(-alpha, 0, 'Sm0 Sigmaz1', 0, 'Sp0', 1)

        # 4) Initialize MPO
        MPOModel.__init__(self, lat, self.calc_H_MPO())
        # 5) Initialize H bond  # LS: what does this mean?
        NearestNeighborModel.__init__(self, self.lat, self.calc_H_bond())