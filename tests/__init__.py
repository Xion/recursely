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

    def test_only_submodules__import_modules(self):
        """Package with just modules and __recursive__ = 'modules'."""
        import justmodules as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)

    def test_only_subpackages__import_packages(self):
        """Package with just subpackages and __recursive__ = 'packages'."""
        import justpackages as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)

    def test_both__import_modules(self):
        """Package with modules and packages, and __recursive__ = 'modules'."""
        import importmodules as pkg

        # subpackage `a` shouldn't be imported
        with self.assertRaises(AttributeError):
            pkg.a.A
        with self.assertRaises(KeyError):
            sys.modules['%s.a' % pkg.__name__]

        self.assertEquals(pkg.b.B, 2)

    def test_both__import_packages(self):
        """Package with modules and packages, and __recursive__ = 'packages'."""
        import importpackages as pkg

        self.assertEquals(pkg.a.A, 1)

        # submodules `b` shouldn't be imported
        with self.assertRaises(AttributeError):
            pkg.b.B
        with self.assertRaises(KeyError):
            sys.modules['%s.b' % pkg.__name__]

    def test_both__import_all(self):
        """Package with modules and packages, and __recursive__ = 'all'."""
        import importall as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)
