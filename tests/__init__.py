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

    def test_only_submodules(self):
        """Package with just one level of submodules."""
        import justmodules as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)

    def test_only_subpackages(self):
        """Package with just one level of subpackages."""
        import justpackages as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)

    def test_both__one_level(self):
        """Package with modules and packages up to one level of recursion."""
        import both1level as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)

    def test_both__two_levels(self):
        """Package with modules and packages up to two levels of recursion."""
        import both2levels as pkg
        self.assertEquals(pkg.a.A, 1)
        self.assertEquals(pkg.b.B, 2)
        self.assertEquals(pkg.a.c.C, 3)
        self.assertEquals(pkg.a.d.D, 4)
