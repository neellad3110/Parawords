<h1 align="center">ParaWords</h1>

ParaWords is a [Django Rest-framework](https://www.django-rest-framework.org/) project which takes a passage with multiple paragraphs as input and seperates each paragraphs and words in it. Additionally, a single word can be searched from the entire sets of top 10 paragraphs added by a specific user. Moreover, user creation and authentication using [JWT](https://jwt.io/) token is perform to maintain integrity with paragraphs and words collection. 

**Table of Contents:**

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
- [Installation](#installation)
  - [Python installation](#python-installation)
  - [PostgreSQL installation](#postgresql-installation)
  - [Virtual Environment (`venv`)](#virtual-environment-venv)
  - [Running the project](#running-the-project)
- [Postman Guide](#postman-guide)
    - [ParaWords Postman Collection](#parawords-postman-collection)

## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

```
git clone <project_url>
```

#### Python installation

Head over to the [official Python website](https://www.python.org/downloads/) and download the installer
Also, be sure to have `git` donwloaded and available in your PATH as well.

#### PostgreSQL installation 

[PostgreSQL](https://www.postgresql.org/download/) is available for download as ready-to-use packages or installers for various platforms.

Follow the complete installation guide from [here](https://www.w3schools.com/postgresql/postgresql_install.php)

After installtion, login to your pgAdmin. Expand `Servers` and `PostgreSQL`. Now right click on `Databases` then create a new database.

<img src="https://static.javatpoint.com/postgre/images/postgresql-create-database.png" />

### Virtual Environment (`venv`)

While there are a few ways to achieve a programming environment in Python, we’ll be using the venv module here, which is part of the standard Python 3 library. Let’s install venv by typing:

```
pip install virtualenv
```
Creating and entering a new virtual environment:
```
python -m venv env
source env/bin/activate
```
### Running the project

Before running the project, We need to install required packages for the project from requirements.txt.
```
pip install -r requirements.txt
``` 
Now open project [settings.py](Parawords/settings.py) file and update your database configuation in `DATABASES` part.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': localhost,
        'PORT': 5432,
        'USER': postgres,                               # pgAdmin username
        'PASSWORD': your_password,                      # pgAdmin passoword
        'NAME': your_database_name,                     # Database name
    }
}

```
Let's map your `Model` and create new `Relation` in database by migration.

```
python manage.py makemigrations
pythom manage.py migrate
```
Now create a `Superuser` as Django Admin. Add your username and password

```
python manage.py createsupersuper
```

Finally start the server.
```
python manage.py runserver
```

Once the server has started up, you can visit it at [localhost:8000/](localhost:8000/), or [127.0.0.1:8000/](127.0.0.1:8000/).

For Admin Panel, you can visit it at [localhost:8000/admin](localhost:8000/admin), or [127.0.0.1:8000/](127.0.0.1:8000/admin).

## Postman Guide

To get the latest version of the Postman desktop app, visit the [Download Postman page](https://www.postman.com/downloads/) and select the option for your operating system. Postman is available as a native desktop app for macOS (Intel or Apple silicon), Windows (Intel 32-bit or 64-bit), and Linux (64-bit).

Postman is also available as a web app at [go.postman.co/home](go.postman.co/home). You can use the Postman web app to carry out many of your API development and testing tasks in your web browser. Keep in mind that some features aren't supported when using the Postman web app, so use the Postman desktop app for the full Postman experience.

#### ParaWords Postman Collection

Look at the published ParaWords API end points and documentation [here](https://documenter.getpostman.com/view/32295301/2s9Yyy9JZD) 