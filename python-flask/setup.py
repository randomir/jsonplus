#!/usr/bin/env python
from setuptools import setup

setup(
    name='Flask-JSONPlus',
    version='0.0.4',
    description="Flask extension for non-basic types' serialization to JSON via jsonplus lib.",
    long_description=open('README.rst').read(),
    author='Radomir Stevanovic',
    author_email='radomir.stevanovic@gmail.com',
    url='https://github.com/randomir/jsonplus/tree/master/python-flask',
    license='MIT',

    py_modules=['flask_jsonplus'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[i.strip() for i in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

