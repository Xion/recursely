"""
recursely
=========

Recursive importer for Python submodules

Usage
-----

First, install it early during program's initialization,
such as the top of `\_\_init\_\_.py` in its main package::

    import recursely
    recursely.install()

Then you can add::

    __recursive__ = True

anywhere in the `\_\_.init\_\_.py` file of a package
that you want to import recurs(iv)ely.

That's all to it, really.
"""
import os
from setuptools import setup, find_packages

import recursely


def read_requirements(filename='requirements.txt'):
    """Reads the list of requirements from given file.

    :param filename: Filename to read the requirements from.
                     Uses ``'requirements.txt'`` by default.

    :return: Requirements as list of strings
    """
    # allow for some leeway with the argument
    if not filename.startswith('requirements'):
        filename = 'requirements-' + filename
    if not os.path.splitext(filename)[1]:
        filename += '.txt'  # no extension, add default

    def valid_line(line):
        line = line.strip()
        return line and not any(line.startswith(p) for p in ('#', '-'))

    def extract_requirement(line):
        egg_eq = '#egg='
        if egg_eq in line:
            _, requirement = line.split(egg_eq, 1)
            return requirement
        return line

    with open(filename) as f:
        lines = f.readlines()
        return list(map(extract_requirement, filter(valid_line, lines)))


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
    tests_require=read_requirements('test'),
)
