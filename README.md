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

You are now ready to start running the emulators! 


# Getting Started:

To kick off the use of emulators, please ensure that you check the validity range of the input parameters for each emulator. 

## Emulators validity

|  Input parameter   |   Range   |    Definition   |
|   ---------   | ------------ | ------------ |
|   'omega_b'   | [0.01875, 0.02625] | Physical baryon density parameter |
|   'omega_cdm' | [0.05, 0.255] | Physical dark matter density parameter |
|      'h'      | [0.64, 0.82] | Reduced Hubble constant |
|     'n_s'     | [0.84, 1.1]  | Scalar spectral index |
|     'S_8'     | [0.6, 0.9] | Amplitude of matter fluctuations |
|     'm_nu'     | [0, 0.2] | Neutrino mass |
|      'w'      | [-1.3, -0.7] | Dark energy equation of state |
|      'A'      | [-30, 30] | DS interaction term |
|    'c_min'    | [2, 4] | Baryonic parameter |
|    'eta_0'    | [0.5, 1] | Baryonic parameter |
|      'z'      | [0,5] | Redshift |


Please feel free to look at the `notebooks` directory to find a comprehensive tutorial scripts designed to guide you through the usage of our emulators. Whether you're a beginner or an experienced user, these tutorials cover essential tasks such as emulators setup, manage, and visualization.

## Emulators accuracy

We provide visual representations of the accuracy of the emulators. The figures show the accuracy of each emulator:

1. **DS non-linear matter power spectrum emulator**
<div align="center">
</div>
<div align="center"><img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_DS_nonlinear_emulator.png" width="500" height="400"> 
</div>

2. **DS linear matter power spectrum emulator**
<div align="center">
</div>
<div align="center"><img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_linear_emulator.png" width="500" height="400"> 
</div>

3. **Baryonic feedback emulator**
<div align="center">
</div>
<div align="center"><img src="https://github.com/karimpsi22/DS-emulators/blob/main/accuracy_bayonic_emulator.png" width="500" height="400"> 
</div>


# Citation

If you use the emulators from this repository in your research, please consider citing the original [release paper](https://arxiv.org/abs/2402.18562):

    @article{Carrion:2024itc,
    author = "Carrion, Karim and Carrilho, Pedro and Spurio Mancini, Alessio and Pourtsidou, Alkistis and Hidalgo, Juan Carlos",
    title = "{Dark Scattering: accelerated constraints from KiDS-1000 with $\tt{ReACT}$ and $\tt{CosmoPower}$}",
    eprint = "2402.18562",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    month = "2",
    year = "2024"
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
