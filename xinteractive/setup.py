from setuptools import setup, find_packages

setup(
    name='xarray interactive',
    version='0.0.1',
    url='https://github.com/xarray-interactive.git',
    author='Tom Nicholas',
    author_email='thomas.nicholas@york.ac.uk',
    description='Description of my package',
    packages=find_packages(),
    install_requires=['xarray >= 0.14.0', 'ipywidgets >= 7.5.1',
                      'matplotlib >= 3.0.0'],
)