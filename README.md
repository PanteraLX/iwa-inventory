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

After installation, copy `.env.template`-file as `.env` and provide the desired values or credentials. As database engine, `mariadb` or `sqlite3` can be used out of the box
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.

A new super user can be created with:
```
python manage.py createsuperuser
```

## Tailwind build

If you have changed any CSS styles in `app/static/css/input.css`, please compile the file with
## Tailwind build

We use tailwind as a CSS framework. The CSS output files are build with NodeJS. Please install a NodeJs runtime if yout want to change any styles and run

```
npm install
```
in the project directory.

If you have changed any CSS styles in `app/static/css/input.css`, please compile the file with

```
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/app.css
```

Please do not change any styles in app.css directly, since this file will be overwritten by `tailwindcss`