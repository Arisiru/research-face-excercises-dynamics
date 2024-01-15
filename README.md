# research-face-excercises-dynamics
We infer the recovery trend in face mobility exercises 


## Dependencies
### Pienv & pyenv

Make sure you have `pyenv` installed. Please follow the [Pyenv repository](https://github.com/pyenv/pyenv) to install it. Use [Pyenv-win reposytory](https://github.com/pyenv-win/pyenv-win) if you're on Windows

Make sure you have `pipenv` installed. Please follow the [Pienv documentation](https://pipenv-fork.readthedocs.io/en/latest/install.html) to install it.

**Pay attention** if you are on Windows and didn't add `pipenv` to your `PATH` you need always add `python -m` in front of `pipenv`

Then execute:
- **Copy** and rename `.env_exaple` file to `.env` and alter according to your OS
- to create a virtual envoirnment and install all dependencies including development run `pipenv install --dev` (don't forget `python -m pipenv install --dev` in if youre on Winodow and didn't add `pipenv` to your `PATH`)
- to activate the virtual envoirnment run `pipenv shell` or `python -m pipenv install`
- to install a dependency please use `pipenv instal package name` instead of `pip`

Whenever you're having issues with installing all the packages with `pipenv` use `pipenv install --dev --skip-lock`.
You may later from virtual environment try to run `pipenv lock` to lock versions.

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

To run a notebook, please make sure youre get into your virtual environtment `pipenv shell`
Install named kernel `python -m ipykernel install --user --name=face-prognosis`
After you run `jupyter notebook` from virtual environment and select a kernel named `face-prognosis`

### Mac

Make sure you have wget installed in your system
for Mac run `brew install wget`

If you're on M1 
`brew install hdf5`
`export HDF5_DIR="$(brew --prefix hdf5)"`
`export PIP_NO_BINARY=h5py && pipenv install h5py`