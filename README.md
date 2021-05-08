## Getting Started

Install cookiecutter with `brew install cookiecutter` or `pip install cookiecutter`.

```
cookiecutter gh:rajaumer801/django-boilerplate
```

It will ask you couple of questions required to generate the project. It will generate a folder containing all the files in your current working directory.

Create .env file in main directory.

Install pipenv with `brew install pipenv` or `pip install pipenv`.

1. `cd` into the new `app` folder just created.
2. `run` pipenv sync.
3. Run `python manage.py makemigrations`
4. Run `python manage.py migrate run`
5. Run `python manage.py runserver`