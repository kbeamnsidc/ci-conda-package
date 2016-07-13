from invoke import run, task

from tasks import hack


@task
def tag():
    cmd = 'git tag {tag} --force && git push --tags --force'.format(tag=hack.tag())
    run(cmd)


@task
def bump(part='patch'):
    cmd = ('bumpversion {0}'.format(part))
    run(cmd)
