"""
recursely
=========

{description}

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
import ast
import os
from setuptools import setup, find_packages
import sys


def read_tags(filename):
    """Reads values of "magic tags" defined in the given Python file.

    :param filename: Python filename to read the tags from
    :return: Dictionary of tags
    """
    with open(filename) as f:
        ast_tree = ast.parse(f.read(), filename)

    res = {}
    for node in ast.walk(ast_tree):
        if type(node) is not ast.Assign:
            continue

        target = node.targets[0]
        if type(target) is not ast.Name:
            continue

        if not (target.id.startswith('__') and target.id.endswith('__')):
            continue

        name = target.id[2:-2]
        res[name] = ast.literal_eval(node.value)

    return res


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


def read_test_requirements():
    """Reads the list of test requirements
    for ``tests_require`` parameter of ``setup()``.
    """
    requirements = read_requirements('test')
    if sys.version_info <= (2, 7):
        requirements.extend(read_requirements('test-py26'))
    return requirements


tags = read_tags(os.path.join('recursely', '__init__.py'))
__doc__ = __doc__.format(**tags)


setup(
    name="recursely",
    version=tags['version'],
    description=tags['description'],
    long_description=__doc__,
    author=tags['author'],
    author_email="karol.kuczmarski@gmail.com",
    url="http://github.com/Xion/recursely",
    license=tags['license'],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],

    platforms='any',
    packages=find_packages(exclude=['tests']),
    tests_require=read_test_requirements(),
)
