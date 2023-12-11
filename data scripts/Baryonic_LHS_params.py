import numpy as np
import pyDOE as pyDOE

# number of parameters, samples and number of job arrays.
n_params = 8
n_samples = 150000
n_arrays = 20
len_files = int(n_samples/n_arrays)

obh2 = np.linspace(0.01865, 0.02625, n_samples)
omch2 = np.linspace(0.05, 0.255, n_samples)
h = np.linspace(0.64, 0.82, n_samples)
ns = np.linspace(0.84, 1.1, n_samples)
S8 = np.linspace(0.6, 0.9, n_samples)
cmin = np.linspace(2.0, 4.0, n_samples)
eta0 = np.linspace(0.5, 1.0, n_samples)
z = np.linspace(0, 5.0, n_samples)

# LHS grid

AllParams = np.vstack([obh2, omch2, h, ns, S8, cmin, eta0, z])
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
          'c_min': (AllCombinations[:, 5][a_index:b_index]),
          'eta_0': (AllCombinations[:, 6][a_index:b_index]),
          'z': AllCombinations[:, 7][a_index:b_index],
           }

    np.savez('Boost_LHS_parameter_{file}.npz'.format(file=int(ii+1)), **params)
