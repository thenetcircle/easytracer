#!/usr/bin/env python3

from setuptools import setup, find_packages

version = '0.2.0'

setup(
    name='easytracer',
    version=version,
    description="Easy Distributed Tracing",
    long_description="""Easy Distributed Tracing""",
    classifiers=[],
    keywords='easytracer',
    author='Oscar Eriksson',
    author_email='oscar.eriks@gmail.com',
    url='https://github.com/thenetcircle/easytracer',
    license='LICENSE',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'backend']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "arrow"
    ],
    test_requires=[
    ])
