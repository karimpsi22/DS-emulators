import numpy as np
import sys
import os

#CLASS
import classy
cosmo = classy.Class()

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
zeros_k = np.zeros(num_k) #In case CLASS has errors
np.savetxt('k_modes.txt', k)   #Saving

params_lhs = np.load('./params_files/Boost_LHS_parameter_{file}.npz'.format(file=int(index)))

#These arrays redefinated are needed in order to avoid the 'Bad magic number' issue with *multiprocessing* due to the paramaters headers cause such error.
omega_b_arr = np.array(params_lhs['omega_b'])
omega_cdm_arr = np.array(params_lhs['omega_cdm'])
h_arr = np.array(params_lhs['h'])
ns_arr = np.array(params_lhs['n_s'])
S8_arr = np.array(params_lhs['S_8'])
z_arr = np.array(params_lhs['z'])
cmin_arr = np.array(params_lhs['c_min'])
eta0_arr = np.array(params_lhs['eta_0'])

lenght = len(params_lhs['c_min'])

def rescaling_As(i):

    cosmo_As = classy.Class()

    cosmo_As.set({'output':'mPk','P_k_max_1/Mpc':50.,'z_max_pk':5.0,
            'h':h_arr[i],'N_ncdm' : 0,'N_eff' : 3.046,
            'gauge':'Newtonian',
            'omega_b':omega_b_arr[i],'omega_cdm':omega_cdm_arr[i],
            'A_s':2.1e-9,'n_s':ns_arr[i]})

    cosmo_As.compute()

    target_S8 = S8_arr[i]
    target_sigma8 = target_S8/np.sqrt(cosmo_As.Omega0_m()/0.3)
    new_As = cosmo_As.pars['A_s']*(target_sigma8/cosmo_As.sigma8())**2

    return new_As

def linear_generation(i, As_new):

#   Define your cosmology (what is not specified will be set to CLASS default parameters)

    cosmo.set({'output':'mPk','P_k_max_1/Mpc':50.,'z_max_pk':5.0,
            'N_ncdm' : 0,'N_eff' : 3.046, 'gauge':'Newtonian',
            'h':h_arr[i],'omega_b':omega_b_arr[i],'omega_cdm':omega_cdm_arr[i],
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
        sigma_8 = cosmo.sigma8()

#        print('target:',S8_arr[i], 'computed:', sigma_8*np.sqrt(cosmo.Omega0_m()/0.3))

        return P_lin, sigma_8

    #Parameter set rejected by Class
    except classy.CosmoComputationError as failure_message:
        print(str(failure_message)+'\n')
        cosmo.struct_cleanup()
        cosmo.empty()
        return zeros_k, 0.0

    #Something wrong in Class init
    except classy.CosmoSevereError as critical_message:
        print("Something went wrong when calling CLASS" + str(critical_message))
        cosmo.struct_cleanup()
        cosmo.empty()
        return zeros_k, 0.0

def boost_generation(i, P_lin, sigma8_val):

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
    D2_growth = P_lin[0,k_index]/P_lin[:,k_index]

    c_pseudo.set_linear_power_spectrum(k, np.array([z_arr[i]]), np.array([D2_growth[z_pos]*P_lin[z_pos]]))
    #Set the halo model in HMcode
    #Options: HMcode2015, HMcode2016, HMcode2020
    hmod = hmcode.Halomodel(hmcode.HMcode2020, verbose=False)

    #Baryonic feedback
    hmod_feedback = hmcode.Halomodel(hmcode.HMcode2016, verbose=False)
    hmod_feedback.As = cmin_arr[i]
    hmod_feedback.eta0 = eta0_arr[i]
    #hmod.eta0 = 0.98 - 0.12*As

    #DM-only Non-linear Power spectrum calculation
    Pk_dm_only = hmcode.calculate_nonlinear_power_spectrum(c_pseudo, hmod, verbose=False)[0]

    #Non-linear Power spectrum with baryonic feedback calculation
    Pk_feedback = hmcode.calculate_nonlinear_power_spectrum(c_pseudo, hmod_feedback, verbose=False)[0]

    Boost_feedback = Pk_feedback/Pk_dm_only

    return Boost_feedback, z_pos

def boost_spectra_generation(ii):

    #Rescaling As
    As_new_i = rescaling_As(ii)

    #Linear spectrum
    Plin, sigma8_i = linear_generation(ii, As_new_i)

    #Boost
    Boost, zi_pos = boost_generation(ii, Plin, sigma8_i)

    #linear
    cosmo_array_linear = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], Plin[zi_pos]))
    f=open('./linear_files/linear_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_linear])
    f.close()

    # baryonic boost
    cosmo_array_boost = np.hstack(([params_lhs[jj][ii] for jj in params_lhs], Boost))
    f=open('./boost_feedback_files/boost_feedback_{file}.dat'.format(file=int(index)),'ab')
    np.savetxt(f, [cosmo_array_boost])
    f.close()

    return
