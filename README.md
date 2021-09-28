# app-prog


## Install these before continuing

* uwsgi (server)
* poetry (dependecy manager)
* pyenv (python version manager)
* pyenv-virtualenv (venv manager)

## Prepare environment

```bash
git clone https://github.com/0x0bloodyknight/app-prog
cd app-prog

# Pyenv & virtualenv init
pyenv install 3.8.12
pyenv rehash
pyenv virtualenv 3.8.12 app-prog
pyenv local app-prog

# Poetry install dependencies
poetry install
```

### Run uwsgi server

```bash
cd app-prog
uwsgi --ini wsgi.ini
```