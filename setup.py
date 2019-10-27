from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='dk-careglaz',
    version='unspecified',
    packages=find_packages(),
    py_modules=['vseros'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)
