"""
recursely :: Recursive importer for Python submodules
"""
__version__ = "0.0.1"
__author__ = "Karol Kuczmarski"
__license__ = "BSD"


import os
import sys

from .hook import ImportHook
from .utils import SentinelList


def install():
    """Install the recursive import hook in ``sys.meta_path``.

    Because the hook is a catch-all one, we ensure that it's always
    at the very end of ``sys.meta_path``, so that it's tried only if
    no other (more specific) hook has been chosen by Python.
    """
    sys.meta_path = SentinelList(sys.meta_path, sentinel=RecursiveImporter())


class RecursiveImporter(ImportHook):
    """Hook for recursive import of submodules and subpackages
    of a package that is marked as 'recursive'.

    In general, such packages should have ``__recursive__ = True``
    somewhere inside their `__init__.py` files.
    """
    def on_module_imported(self, fullname, module):
        """Invoked just after a module has been imported."""
        recursive = getattr(module, '__recursive__', False)
        if not recursive:
            return

        # recursive import can only start from package's __init__.py file
        module_file = getattr(module, '__file__', None)
        if not module_file:
            return
        if os.path.splitext(os.path.basename(module_file))[0] != '__init__':
            return
        package_dir = os.path.dirname(module_file)

        if recursive is True:
            recursive = 'all'
        recursive = recursive.lower()

        # see what kind of children we should import
        children = []
        if recursive in ('all', 'packages'):
            children.extend(self.list_subpackages(package_dir))
        if recursive in ('all', 'modules'):
            children.extend(m for m in self.list_submodules(package_dir)
                            if m != '__init__')

        if children:
            globals_ = module.__dict__
            locals_ = module.__dict__
            for child in children:
                __import__(child, globals_, locals_)

    @staticmethod
    def list_subpackages(package_dir):
        """Lists all subpackages (directories with `__init__.py`)
        contained within given package.

        :param package_dir: Package directory
        """
        def is_subpackage_dir(name):
            abs_path = os.path.join(package_dir, name)
            init_py = os.path.join(abs_path, '__init__.py')
            return os.path.isdir(abs_path) and os.path.isfile(init_py)

        return [name for name in os.listdir(package_dir)
                if is_subpackage_dir(name)]

    @staticmethod
    def list_submodules(package_dir):
        """Lists all submodules (`*.py` files) contained within given package.
        :param package_dir: Package directory
        """
        def is_submodule_file(name):
            abs_path = os.path.join(package_dir, name)
            return os.path.isfile(abs_path) and name.endswith('.py')

        return [os.path.splitext(name)[0]
                for name in os.listdir(package_dir)
                if is_submodule_file(name)]
