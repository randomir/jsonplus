#!/usr/bin/env python
from setuptools import setup

setup(
    name='jsonplus',
    version='0.4.1',
    description="Custom datatypes (like datetime) serialization to/from JSON.",
    long_description=open('README.rst').read(),
    author='Radomir Stevanovic',
    author_email='radomir.stevanovic@gmail.com',
    url='https://github.com/randomir/jsonplus',
    license='MIT',
    packages=['jsonplus'],
    package_dir={'jsonplus': 'jsonplus'},
    install_requires=[i.strip() for i in open('requirements.txt').readlines()],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='json custom python type serialization deserialization datetime set'
)
