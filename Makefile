init:
	pip install -r requirements_dev.txt

test:
	python -m unittest discover -s 'tests' -p 'test*.py' -v

# EXAMPLE TASKS FOR FUTURE

# clean-pyc:
#   find . -name '*.pyc' -exec rm --force {} +
#   find . -name '*.pyo' -exec rm --force {} +
#   name '*~' -exec rm --force  {}

# clean-build:
#   rm --force --recursive build/
#   rm --force --recursive dist/
#   rm --force --recursive *.egg-info

# isort:
#   sh -c "isort --skip-glob=.tox --recursive . "

# lint:
#   flake8 --exclude=.tox

# run:
#   python manage.py runserver
