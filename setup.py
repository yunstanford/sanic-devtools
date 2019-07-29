#!/usr/bin/env python
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'aiohttp>=3.5.0',
    'cookiecutter',
    'click>=6.6',
    'devtools>=0.5',
    'Pygments>=2.2.0',
    'watchgod>=0.2',
    'sanic',
]

tests_require = []

setup(
    name='pytest-sanic',
    version='0.1.0',
    description='dev tools for Sanic',
    long_description=open(README_PATH).read(),
    author='Yun Xu',
    author_email='yunxu1992@gmail.com',
    url='https://github.com/yunstanford/sanic-devtools/',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "sdev=sanic_devtools.cli:cli",
            "sanic-devtools=sanic_devtools.cli:cli",
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
