# DS-emulators

Welcome! This repository houses a non-linear and linear matter spectrum emulator of Dark Scattering (DS) model built upon the framework of the halo model reaction. In addition, a baryonic feedback emulator based on ``HMC0DE2016_FEEDBACK``. 

Comprehensive documentation of ``CosmoPower`` is available [here](https://alessiospuriomancini.github.io/cosmopower).

# Documentation

Since these emulators were trained by ``CosmoPower``, we recommend using them within a [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) virtual environment. 

For example, to create an environment called ``emu_env``, use:

    conda create -n emu_env python=3.7 pip

Then, you may easily activate the environment:

    conda activate emu_env

Once inside the environment, you can install ``CosmoPower``:

- **from PyPI**

        pip install cosmopower

    To test the installation, you can use

        python3 -c 'import cosmopower as cp'
    
    If you do not have a GPU on your machine, you will see a warning message about it which you can safely ignore.

- **from source**

        git clone https://github.com/alessiospuriomancini/cosmopower
        cd cosmopower
        pip install .

    To test the installation, you can use

        pytest

You are now ready to start utilizing the emulators! 


# Getting Started:

To get started with usage of emulators, please ensure that you check the validity range of the input parameters for each emulator. 

## Emulators validity

|   Parameter   |   Range   |
|   ---------   | ------------ |
|   'omega_b'   | [0.01875, 0.02625] | 
|   'omega_cdm' | [0.05, 0.255] |
|      'h'      | [0.64, 0.82] |
|     'n_s'     | [0.84, 1.1]  |
|     'S_8'     | [0.6, 0.9] |
|     'm_nu'     | [0, 0.2] |
|      'w'      | [-1.3, -0.7] |
|      'A'      | [-10, 10] |
|    'c_min'    | [2, 4] |
|    'eta_0'    | [0.5, 1] |
|      'z'      | [0,5] |


Please feel free to look at the `notebooks` directory to find a comprehensive tutorial scripts designed to guide you through the usage of our emulators. Whether you're a beginner or an experienced user, these tutorials cover essential tasks such as emulators setup, manage, and visualization.

## Emulators accuracy

<div align="center">
</div>
<div align="center"><img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_DS_nonlinear_emulator_with_S8.png" width="500" height="400"> 
</div>

<div align="center">
  <figure>
    <img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_linear_emulator_with_S8.png" width="500" height="400">

  </figure>
  
  <figure>
    <img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_bayonic_emulator.png" width="500" height="400">
  </figure>
</div>

# Citation

If you use the emulators from this repository in your research, please consider citing the original [release paper](https://arxiv.org/abs/2106.03846):

    @article{carrion2023,
             TBA
             }

In addition please cite  ``CosmoPower`` [release paper](https://arxiv.org/abs/2106.03846):

    @article{SpurioMancini2022,
         title={CosmoPower: emulating cosmological power spectra for accelerated Bayesian inference from next-generation surveys},
         volume={511},
         ISSN={1365-2966},
         url={http://dx.doi.org/10.1093/mnras/stac064},
         DOI={10.1093/mnras/stac064},
         number={2},
         journal={Monthly Notices of the Royal Astronomical Society},
         publisher={Oxford University Press (OUP)},
         author={Spurio Mancini, Alessio and Piras, Davide and Alsing, Justin and Joachimi, Benjamin and Hobson, Michael P},
         year={2022},
         month={Jan},
         pages={1771–1788}
         }


# License

``CosmoPower`` is released under the GPL-3 license (see [LICENSE](https://github.com/alessiospuriomancini/cosmopower/blob/main/LICENSE)) subject to 
the non-commercial use condition (see [LICENSE_EXT](https://github.com/alessiospuriomancini/cosmopower/blob/main/LICENSE_EXT)).

    CosmoPower
    Copyright (C) 2021 A. Spurio Mancini & contributors

    This program is released under the GPL-3 license (see LICENSE), 
    subject to a non-commercial use condition (see LICENSE_EXT).

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
