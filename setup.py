#!/usr/bin/env python
from setuptools import setup
import jsonplus

setup(
    name=jsonplus.__name__,
    version=jsonplus.__version__,
    description=jsonplus.__doc__,
    long_description=open('README.rst').read(),
    author=jsonplus.__author__,
    author_email=jsonplus.__author_email__,
    url=jsonplus.__url__,
    license=jsonplus.__license__,
    packages=[jsonplus.__name__],
    package_dir={jsonplus.__name__: jsonplus.__name__},
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
