"""
recursely
=========

Recursive importer for Python submodules
"""
from setuptools import setup, find_packages

import recursely


setup(
    name="recursely",
    version=recursely.__version__,
    description="Recursive importer for Python submodules",
    long_description=__doc__,
    author=recursely.__author__,
    author_email="karol.kuczmarski@gmail.com",
    url="http://github.com/Xion/recursely",
    license="Simplified BSD",

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],

    platforms='any',
    packages=find_packages(exclude=['tests']),
    tests_require=['nose'],
)
