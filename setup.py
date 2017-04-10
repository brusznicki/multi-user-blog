# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='Multi User Blog',
    version='0.1.0',
    description='Multi User Blog for Udacity 253',
    long_description=readme,
    author='Chris Brusznic.mdki',
    author_email='chris.brusznicki@gmail.com',
    url='https://github.com/brusznicki/multi-user-blog',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
