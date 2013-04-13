"""
Tests package.
"""
import os
import sys
import unittest


TESTS_DIR = os.path.dirname(__file__)
IMPORTED_DIR = os.path.join(TESTS_DIR, 'imported')


def test_imported_dir_is_not_package():
    """Make sure `imported` directory was not made into a package.

    The reason it can't be a package is that nose will otherwise "collect" it
    in order to look for tests inside. And collection means importing,
    which we don't want to do before actual tests.
    """
    imported_init_py = os.path.join(IMPORTED_DIR, '__init__.py')
    assert not os.path.exists(imported_init_py)


class TestRecursiveImporter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import recursely
        recursely.install()

        # make it possible to import from tests/imported directory
        sys.path.insert(0, IMPORTED_DIR)

    def test_just_modules(self):
        """Package with just modules and __recursive__ = 'modules'."""
        import justmodules
        self.assertEquals(justmodules.a.A, 1)
        self.assertEquals(justmodules.b.B, 2)

    def test_just_packages(self):
        """Package with just subpackages and __recursive__ = 'packages'."""
        import justpackages
        self.assertEquals(justpackages.a.A, 1)
        self.assertEquals(justpackages.b.B, 2)
