import numpy as np
import sys
import os

#CLASS-IDE
import classy
cosmo = classy.Class()

#ReACT
import pyreact
react = pyreact.ReACT()

#HMCODE
import pyhmcode as hmcode

# Index for job arrays
index = sys.argv[1]

#Creating the range of k-modes
#krange1 = np.logspace(np.log10(1e-5), np.log10(1e-4), num=20, endpoint=False)
krange2 = np.logspace(np.log10(1e-4), np.log10(1e-3), num=40, endpoint=False)
krange3 = np.logspace(np.log10(1e-3), np.log10(1e-2), num=60, endpoint=False)
krange4 = np.logspace(np.log10(1e-2), np.log10(1e-1), num=80, endpoint=False)
krange5 = np.logspace(np.log10(1e-1), np.log10(1), num=100, endpoint=False)
krange6 = np.logspace(np.log10(1), np.log10(10), num=120, endpoint=False)

k = np.concatenate((krange2, krange3, krange4, krange5, krange6))
num_k = len(k)
zeros_k = np.zeros(num_k) #In case CLASS would display errors
np.savetxt('k_modes.txt', k) #Saving

params_lhs = np.load('./params_files/DS_LHS_parameter_{file}.npz'.format(file=int(index)))

#These arrays redefinated are needed in order to avoid the 'Bad magic number' issue with *multiprocessing* due to the paramaters headers cause such error.
omega_b_arr = np.array(params_lhs['omega_b'])
omega_cdm_arr = np.array(params_lhs['omega_cdm'])
h_arr = np.array(params_lhs['h'])
ns_arr = np.array(params_lhs['n_s'])
S8_arr = np.array(params_lhs['S_8'])
mnu_arr = np.array(params_lhs['m_nu'])
w_arr = np.array(params_lhs['w'])
z_arr = np.array(params_lhs['z'])
A_arr = np.array(params_lhs['A']) 

lenght = len(params_lhs['omega_b'])

def rescaling_As(i):
#   Interaction
    if w_arr[i] == -1.0:
        xi_value = 0.0

    else:
        xi_value = A_arr[i]/(1.0+w_arr[i])
        
    cosmo_As = classy.Class()

    cosmo_As.set({'output':'mPk','P_k_max_1/Mpc':50.,'z_max_pk':5.0,
            'h':h_arr[i],'N_ur':2.0308,'N_ncdm':1,'m_ncdm':mnu_arr[i],
            'cs2_fld':1.,
            'w0_fld':w_arr[i],'wa_fld':0.0,'xi_ds':xi_value,'Omega_Lambda':0.,'gauge':'Newtonian',
            'use_ppf':'yes','dark_scattering':'yes',
            'omega_b':omega_b_arr[i],'omega_cdm':omega_cdm_arr[i],
            'A_s':2.1e-9,'n_s':ns_arr[i]})
    
    cosmo_As.compute()
    
    target_S8 = S8_arr[i]
    target_sigma8 = target_S8/np.sqrt(cosmo_As.Omega0_m()/0.3)
    new_As = cosmo_As.pars['A_s']*(target_sigma8/cosmo_As.sigma8())**2
    
    return new_As

def linear_generation(i, As_new):
#   Interaction
    if w_arr[i] == -1.0:
        xi_value = 0.0

    else:
        xi_value = A_arr[i]/(1.0+w_arr[i])

#   Define your cosmology (what is not specified will be set to CLASS default parameters)

    cosmo.set({'output':'mPk','P_k_max_1/Mpc':50.,'z_max_pk':5.0,
            'h':h_arr[i],'N_ur':2.0308,'N_ncdm':1,'m_ncdm':mnu_arr[i],
            'cs2_fld':1.,
            'w0_fld':w_arr[i],'wa_fld':0.0,'xi_ds':xi_value,'Omega_Lambda':0.,'gauge':'Newtonian',
            'use_ppf':'yes','dark_scattering':'yes',
            'omega_b':omega_b_arr[i],'omega_cdm':omega_cdm_arr[i],
            'A_s':As_new,'n_s':ns_arr[i]})

    try:
        cosmo.compute()

        z = np.linspace(0.0, 5.0, 50)

        if z_arr[i] not in z:
            index_remove = np.where(z_arr[i] < z)[0][0] #The nearest redshift to the one will be inserted
            z = np.delete(z, index_remove)
            z = np.sort(np.insert(z, 1, z_arr[i]))

        z_pos = np.where(z == z_arr[i])[0][0]  #Index of z_i in z array.


        #Linear DS
        P_lin = np.array([[cosmo.pk(ki, zi)*h_arr[i]**3.0 for ki in k*h_arr[i]] for zi in z])
        P_cb = np.array([[cosmo.pk_cb(ki, zi)*h_arr[i]**3.0 for ki in k*h_arr[i]] for zi in z])
        sigma_8 = cosmo.sigma8()

        #Linear LCDM
        cosmo_lcdm = classy.Class()

        cosmo_lcdm.set({'output':'mPk','P_k_max_1/Mpc':50,'z_max_pk':5.0,
               'h':h_arr[i],'N_ur':2.0308,'N_ncdm':1,'m_ncdm':mnu_arr[i],
               'gauge':'Newtonian',
               'omega_b':omega_b_arr[i],'omega_cdm':omega_cdm_arr[i],
               'A_s':As_new,'n_s':ns_arr[i]})

        cosmo_lcdm.compute()

        Plcdm_cb = np.array([[cosmo_lcdm.pk_cb(ki, zi)*h_arr[i]**3.0 for ki in k*h_arr[i]] for zi in z])
        sigma_8_lcdm = cosmo_lcdm.sigma8()
        
        print('target:',S8_arr[i], 'computed:', sigma_8*np.sqrt(cosmo.Omega0_m()/0.3))

        return P_lin, P_cb, Plcdm_cb, sigma_8

    #Parameter set rejected by Class
    except classy.CosmoComputationError as failure_message:
        print(str(failure_message)+'\n')
        cosmo.struct_cleanup()
        cosmo.empty()
        return zeros_k, zeros_k, zeros_k, 0.0

    #Something wrong in Class init
    except classy.CosmoSevereError as critical_message:
        print("Something went wrong when calling CLASS" + str(critical_message))
        cosmo.struct_cleanup()
        cosmo.empty()
        return zeros_k, zeros_k, zeros_k, 0.0

    #Parameter set rejected by Class LCDM
    except classy.CosmoComputationError as failure_message:
        print(str(failure_message)+'\n')
        cosmo_lcdm.struct_cleanup()
        cosmo_lcdm.empty()
        return zeros_k, zeros_k, zeros_k, 0.0

    #Something wrong in Class init LCDM
    except classy.CosmoSevereError as critical_message:
        print("Something went wrong when calling CLASS" + str(critical_message))
        cosmo_lcdm.struct_cleanup()
        cosmo_lcdm.empty()
        return zeros_k, zeros_k, zeros_k, 0.0


def reaction(i, As_new, P_lin, P_cb, P_lcdm_cb):

    #Set mass of massive neutrino species
    Omega_nu = mnu_arr[i]/(93.14*h_arr[i]**2.0)

    #DS interaction
    if w_arr[i] == -1.0:
        xi_value = 0.0
    else:
        xi_value = A_arr[i]/(1.0+w_arr[i])

    #Only compute the reaction up to z = 2.5    
    #Previous z-array
    z = np.linspace(0.0, 5.0, 50)

    if z_arr[i] not in z:
        index_remove = np.where(z_arr[i] < z)[0][0] #The nearest redshift to the one will be inserted
        z = np.delete(z, index_remove)
        z = np.sort(np.insert(z, 1, z_arr[i]))

    #Constant interpolation of ReACT to redshift above z = 2.5
    if z_arr[i] > 2.5 or z_arr[i] == 0.0:
        z_pos = np.where(z == z[z<=2.5][-1])[0][0] #Closest position of z_i ≈ 2.5
        z_react = np.asarray([0.0, z[z_pos]])
        P_lin_react = np.asarray([P_lin[0], P_lin[z_pos]])
        P_cb_react = np.asarray([P_cb[0], P_cb[z_pos]])
        Plcdm_cb_react = np.asarray([P_lcdm_cb[0], P_lcdm_cb[z_pos]])

    else:
        z_pos = np.where(z == z_arr[i])[0][0]  #Position of z_i in z array
        z_react = np.asarray([0.0, z[z_pos]]) #Extracting z_i
        P_lin_react = np.asarray([P_lin[0], P_lin[z_pos]])
        P_cb_react = np.asarray([P_cb[0], P_cb[z_pos]])
        Plcdm_cb_react = np.asarray([P_lcdm_cb[0], P_lcdm_cb[z_pos]])

    #Model selection and parameter (1:GR, 2:f(R), 3:DGP, 4:quintessence with interaction, 5:CPL with interaction)
    mymodel = "quintessence with interaction"

    #Loop in spherical collapse
    massloop = 50

    #Calculate corrected xi to account for presence of non-cdm species
    Omega_cdm = omega_cdm_arr[i]/h_arr[i]**2.0
    Omega_b = omega_b_arr[i]/h_arr[i]**2.0
    Omega_m = (Omega_b + Omega_cdm + Omega_nu)
    Rc = Omega_cdm/Omega_m
    unit_conv = 0.0194407
    Corr_xi = xi_value*Rc/(1.+ unit_conv*h_arr[i]*(1.-Omega_m)*(1. + w_arr[i])*xi_value*(1.-Rc)) #ReACT parameters

    R_arr, Plin_react, sigma_8_mod = react.compute_reaction_nu(
                            h_arr[i], ns_arr[i], Omega_m, Omega_b, Omega_nu, As_new,
                            z_react, k, P_lin_react.flatten(), P_cb_react.flatten(),
                            k, Plcdm_cb_react.flatten(),
                            pscale = 0.05,
                            model=mymodel,
                            fR0=0.0, Omega_rc=0.0, w=w_arr[i], wa=0.0, xi = Corr_xi,
                            is_transfer=False, mass_loop=massloop,
                            verbose=False)

    if z_arr[i] == 0.0:
        return R_arr[0], P_lin_react[0]

    else:
        return R_arr[-1], P_lin_react[-1]

def pseudo_generation(i, P_lin, Plcdm, sigma8_val):

    #Set mass of massive neutrino species
    m_nu = 0.0
    omega_nu = m_nu/93.14

    Omega_m = (omega_b_arr[i] + omega_cdm_arr[i] + omega_nu)/h_arr[i]**2.0

    #Setup HMcode internal cosmology
    c_pseudo = hmcode.Cosmology()

    #Set HMcode internal cosmological parameters
    c_pseudo.om_m = Omega_m
    c_pseudo.om_b = omega_b_arr[i]/h_arr[i]**2.0
    c_pseudo.om_v = 1.0 - Omega_m
    c_pseudo.h = h_arr[i]
    c_pseudo.ns = ns_arr[i]
    c_pseudo.sig8 = sigma8_val
    c_pseudo.m_nu = m_nu

    z = np.linspace(0.0, 5.0, 50)

    if z_arr[i] not in z:
        index_remove = np.where(z_arr[i] < z)[0][0] #The nearest redshift to the one will be inserted
        z = np.delete(z, index_remove)
        z = np.sort(np.insert(z, 1, z_arr[i]))
    z_pos = np.where(z == z_arr[i])[0][0]  #Exact index of z_i in z array.

    if z_arr[i] == 0.0:
        z_pos = 0

    if z_arr[i] == 5.0:
        z_pos = -1

    #Removing the k-depence of growth factor
    k_index = np.where(k >= 0.2)[0][0]

    D2_growth = Plcdm[0,k_index]/Plcdm[:,k_index]

    c_pseudo.set_linear_power_spectrum(k, np.array([z_arr[i]]), np.array([D2_growth[z_pos]*P_lin[z_pos]]))
    #Set the halo model in HMcode
    #Options: HMcode2015, HMcode2016, HMcode2020
    hmod = hmcode.Halomodel(hmcode.HMcode2020, verbose=False)
    #Non-linear Power spectrum calculation
    Pk_pseudo = hmcode.calculate_nonlinear_power_spectrum(c_pseudo, hmod, verbose=False)

    return Pk_pseudo[0], z_pos

def nonlinear_spectra_generation(ii):
    
    #Rescaling As
    As_new_i = rescaling_As(ii)

    #Linear spectrum
    Plin, Pcb_lin, Plcdm_cb_lin, sigma8_i = linear_generation(ii, As_new_i)

    #Reaction
    Reaction, Plin_zi = reaction(ii, As_new_i, Plin, Pcb_lin, Plcdm_cb_lin)

    #Pseudo spectrum
    Pseudo, zi_pos = pseudo_generation(ii, Plin, Plcdm_cb_lin, sigma8_i)

    #Non-linear prediction
    P_NL = Pseudo*Reaction

    #The parameters must be ordered
    cosmo_array_As = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], As_new_i))
    f=open('./As_ds_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_As])
    f.close()

    #linear
    cosmo_array_linear = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], Plin[zi_pos]))
    f=open('./linear_ds_files/linear_ds_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_linear])
    f.close()

    #non-linear
    cosmo_array_nonlinear = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], P_NL))
    f=open('./nonlinear_ds_files/nonlinear_ds_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_nonlinear])
    f.close()

    cosmo_array_pseudo = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], Pseudo))
    f=open('./pseudo_ds_files/pseudo_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_pseudo])
    f.close()

    # reaction boost
    cosmo_array_reaction = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], Reaction))
    f=open('./reaction_files/reaction_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_reaction])
    f.close()

    return
