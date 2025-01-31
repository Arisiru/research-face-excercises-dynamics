# research-face-excercises-dynamics
We infer the recovery trend in face mobility exercises 


## Dependencies
### Pienv & pyenv

Make sure you have `pyenv` installed. Please follow the [Pyenv repository](https://github.com/pyenv/pyenv) to install it. Use [Pyenv-win reposytory](https://github.com/pyenv-win/pyenv-win) if you're on Windows

Make sure you have `poetry` installed. Please follow the [Poetry documentation](https://python-poetry.org/docs/) to install it.

After installing `poetry` add poetry shell by running `poetry self add poetry-plugin-shell`

Then execute:
- **Copy** and rename `.env_exaple` file to `.env` and alter according to your OS
- to create a virtual envoirnment and install all dependencies use group e.g. `--without xxx` to install correct dependecies 
    - - for linux `poetry install --without mac`
- use group e.g. `--without xxx` to install correct dependecies
    - - for mac `poetry install --without linux`
- to activate the virtual envoirnment run `potery shell`
- to install a dependency please use `poetry add packagename` instead of `pip`


### DVC

For model and experiment data sets' version control please follow [DVC documentation](https://dvc.org/).
If you followed the pipenv section the dvc should be part of your virtual environment.
Please pull data from storage `$ dvc pull`

Access to the data storage can be requested through University or personal messages.

Use dvc commands to commit, push, pull changes to data and models

### Git hooks

Make sure that `pre-commit` is installed
Run `pre-commit install` to setup all the from `.pre-commit-config.yaml`

### Notebook

To run a notebook, please make sure youre get into your virtual environtment `poetry shell`
Install named kernel `python -m ipykernel install --user --name=face-prognosis`
After you run `jupyter lab` from virtual environment and select a kernel named `face-prognosis`

### Mac

Make sure you have wget installed in your system
for Mac run `brew install wget`

If you're on M1 
`brew install hdf5`
`export HDF5_DIR="$(brew --prefix hdf5)"`
`export PIP_NO_BINARY=h5py && pipenv install h5py`