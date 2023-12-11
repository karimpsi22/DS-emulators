import numpy as np
import pyDOE as pyDOE

# number of parameters, samples and number of job arrays.

n_params = 9
n_samples = 200000
n_arrays = 100
len_files = int(n_samples/n_arrays)

obh2 =      np.linspace(0.01865, 0.02625, n_samples)
omch2 =     np.linspace(0.1, 0.255, n_samples)
h =         np.linspace(0.64, 0.82, n_samples)
ns =        np.linspace(0.84, 1.1, n_samples)
S8 =      np.linspace(0.6, 0.9, n_samples)
z =         np.linspace(0, 5, n_samples)
#pyhmcode does not accept values below m_nu = 0.00202020202020202
mnu =       np.linspace(0.0, 0.2, n_samples)
#ReACT ranges -1.3<w0<-0.7 in order to spherical collapse library can solve the virial theorem.
w =         np.linspace(-0.7, -1.3, n_samples)
A_abs =     np.linspace(0, 10, n_samples) #A_abs = abs(A_ds) = abs(\xi*(1+w))
z =         np.linspace(0, 5.0, n_samples)

# LHS grid
AllParams = np.vstack([obh2, omch2, h, ns, S8, mnu, w, A_abs, z])
lhd = pyDOE.lhs(n_params, samples=n_samples, criterion=None)
idx = (lhd * n_samples).astype(int)

AllCombinations = np.zeros((n_samples, n_params))
for i in range(n_params):
    AllCombinations[:, i] = AllParams[i][idx[:, i]]

# saving in each file of len_files
for ii in range(n_arrays):
    a_index = len_files*(ii)
    b_index = (len_files*(ii + 1))

    params = {'omega_b': AllCombinations[:, 0][a_index:b_index],
          'omega_cdm': AllCombinations[:, 1][a_index:b_index],
          'h': AllCombinations[:, 2][a_index:b_index],
          'n_s': AllCombinations[:, 3][a_index:b_index],
          'S_8': AllCombinations[:, 4][a_index:b_index],
          'm_nu': AllCombinations[:, 5][a_index:b_index],
          'w': AllCombinations[:, 6][a_index:b_index],
          'A': (AllCombinations[:, 7][a_index:b_index])*np.sign(1.0+AllCombinations[:, 6][a_index:b_index]),
          'z': AllCombinations[:, 8][a_index:b_index],
           }

    np.savez('LHS_parameter_{file}.npz'.format(file=int(ii+1)), **params)
