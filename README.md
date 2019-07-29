# Run Cli Dev
-  Setup local environment
- `python -m cli_app`

#### Cli Commands
- `python -m cli_app list --help`
- `python -m cli_app get --help`
- `python -m cli_app delete --help`
- `python -m cli_app create --help`
- `python -m cli_app update --help`
- `python -m cli_app delete --help`
- `python -m cli_app search --help`

# Run Http Server Dev
-  Setup local environment
- `export FLASK_APP=http_app`
- `python -m flask run`

#### Http APIs
- List
```
curl -X GET \
  http://127.0.0.1:5000?start=0
```
- Create
```
curl -X POST \
  http://127.0.0.1:5000/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Store name",
    "url": "https://store-url",
    "address": "Store address",
    "lat": 53.3242381,
    "lng": -6.3857866
}'
```
- Get
```
curl -X GET \
  http://127.0.0.1:5000/123
```
- Update
```
curl -X PUT \
  http://127.0.0.1:5000/123 \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Store name",
    "url": "https://store-url",
    "address": "Store address",
    "lat": 53.3242381,
    "lng": -6.3857866
}'
```
- Delete
```
curl -X DELETE \
  http://127.0.0.1:5000/123
```
- Search
```
curl -X GET \
  'http://127.0.0.1:5000/search?query=store&user_lat=53.3242381&user_lng=-6.3857866&start=0'
```

# Setup Local Environment
- Install and switch to `python 3.6.8` (`pyenv` recommended)
- Install virtualenv globally `pip install virtualenv`
- Create virtual environment: `virtualenv .venv`
- Activate virtualenv: `source .venv/bin/activate`
- Run `pip install -r requirements.txt` to install dependencies
- Create `.env` file from `.env.example` with proper values
