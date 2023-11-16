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

To get started with usage of emulators


## Emulator validity

| Parameter  | Range |
| ---------  | ----- |
| <img src="https://render.githubusercontent.com/render/math?math=\omega_{\mathrm{b}}"> | <img src="https://render.githubusercontent.com/render/math?math=[0.01875, 0.02625]"> |
| <img src="https://render.githubusercontent.com/render/math?math=\omega_{\mathrm{cdm}}"> | <img src="https://render.githubusercontent.com/render/math?math=[0.05, 0.255]"> |
| <img src="https://render.githubusercontent.com/render/math?math=h"> | <img src="https://render.githubusercontent.com/render/math?math=[0.64, 0.82]"> |
| <img src="https://render.githubusercontent.com/render/math?math=n_s"> | <img src="https://render.githubusercontent.com/render/math?math=[0.84, 1.1]"> |
| <img src="https://render.githubusercontent.com/render/math?math=S_8"> | <img src="https://render.githubusercontent.com/render/math?math=[1.61, 3.91]"> |
| <img src="https://render.githubusercontent.com/render/math?math=w"> | <img src="https://render.githubusercontent.com/render/math?math=[-1.3, -0.7]"> |
| <img src="https://render.githubusercontent.com/render/math?math=A_\mathrm{ds}"> | <img src="https://render.githubusercontent.com/render/math?math=[0, 5]"> |
| <img src="https://render.githubusercontent.com/render/math?math=c_\mathrm{min}"> | <img src="https://render.githubusercontent.com/render/math?math=[2, 4]"> |
| <img src="https://render.githubusercontent.com/render/math?math=\eta_0"> | <img src="https://render.githubusercontent.com/render/math?math=[0.5, 1]"> |
| <img src="https://render.githubusercontent.com/render/math?math=z"> | <img src="https://render.githubusercontent.com/render/math?math=[0, 5]"> |


# Citation

If you use the emulators from this repository in your research, please consider citing the original [release paper](https://arxiv.org/abs/2106.03846):

    @article{carrion2023,
             title={Dark Scattering: accelerated constraints from KiDS-1000 with ReACT and CosmoPower}, 
             author={{Spurio Mancini}, A. and {Piras}, D. and {Alsing}, J. and {Joachimi}, B. and {Hobson}, M.~P.},
             year={2021},
             eprint={2106.03846},
             archivePrefix={arXiv},
             primaryClass={astro-ph.CO}
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
