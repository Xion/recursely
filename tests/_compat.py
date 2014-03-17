"""
Compatibility shims for tests.
"""
try:
    from unittest2 import *
except ImportError:
    from unittest import *
