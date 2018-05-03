# Simple Web Application

Share links.

### Links

 - `/home`: recent link
 - `/<site>`: links on this site

### User Priv
 
 * Share links
 * Vote links (_once a link_)

## Tools

 - [Django v2](https://www.djangoproject.com/)
 - [Bulma](https://bulma.io/)
 - [FontAwesome](https://fontawesome.com)

## Setup

```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

```
$ python3 manage.py
```
__Username__ / __password__ : __admin__ / __password0__

## Renew Database

```bash
$ rm db.sqlite3
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
Or
```bash
$ bash resetdb.sh
```