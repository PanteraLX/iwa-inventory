# IWA-Inventory

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/PanteraLX/iwa-inventory.git
$ cd iwa-inventory
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

After installation, copy `.env.template`-file as `.env` and provide the desired values. As database engine, `mariadb` ord `sqlite3` can be used out of the box
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.


