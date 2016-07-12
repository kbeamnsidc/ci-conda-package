from invoke import run, task


@task
def flake8():
    """
    run flake8 syntax checking
    """

    run('flake8 . --verbose')


@task
def unittest():
    """
    run unittests using nose
    """

    run('nosetests --verbose --exclude-dir=recipe')


@task(flake8, unittest, default=True)
def all():
    """
    run all of the tests
    """
    print('Running all')
