#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-jsonplus',
    version='0.1.1',
    description="Django extension for non-basic types' serialization to JSON via jsonplus lib.",
    long_description=open('README.rst').read(),
    author='Radomir Stevanovic',
    author_email='radomir.stevanovic@gmail.com',
    url='https://github.com/randomir/jsonplus/tree/master/python-django',
    license='MIT',
    packages=['django_jsonplus'],
    package_dir={'django_jsonplus': 'django_jsonplus'},
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

