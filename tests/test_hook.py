"""
Tests for the .hook module.
"""
from recursely._compat import IS_PY3
from recursely.hook import ImportHook
from tests._compat import TestCase, skipUnless


class TestImportHook(TestCase):

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_abc(self):
        from importlib import abc
        self.assertTrue(issubclass(ImportHook, abc.Finder))
        self.assertTrue(issubclass(ImportHook, abc.Loader))
        self.assertTrue(issubclass(ImportHook, abc.InspectLoader))
