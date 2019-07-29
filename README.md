## Run Cli Dev
-  Setup local environment
- `python -m cli_app`

## Run Http Server Dev
-  Setup local environment
- `export FLASK_APP=http_app`
- `python -m flask run`

## Setup Local Environment
- Install and switch to `python 3.6.8` (`pyenv` recommended)
- Install virtualenv globally `pip install virtualenv`
- Create virtual environment: `virtualenv .venv`
- Activate virtualenv: `source .venv/bin/activate`
- Run `pip install -r requirements.txt` to install dependencies
- Create `.env` file from `.env.example` with proper values
