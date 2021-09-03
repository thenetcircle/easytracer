#!/usr/bin/env python3

from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='easytracer',
    version=version,
    description="Easy Distributed Tracing",
    long_description="""Easy Distributed Tracing""",
    classifiers=[],
    keywords='easytracer',
    author='Oscar Eriksson',
    author_email='oscar.eriks@gmail.com',
    url='https://github.com/thenetcircle/EASYTRACER',
    license='LICENSE',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    test_requires=[
    ])
