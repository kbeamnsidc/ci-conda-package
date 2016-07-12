from setuptools import setup, find_packages

setup(name='ci-conda-package',
      version='0.1.0',
      description='Project to test various CI-as-a-service solutions',
      url='git@bitbucket.org:nsidc/ci-conda-package.git',
      author='Kevin W. Beam (kbeam@nsidc.org)',
      author_email='kbeam@nsidc.org',
      license='GPLv3',
      packages=find_packages(exclude=('tasks',)))
