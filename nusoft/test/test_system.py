#!/usr/bin/env python
#
# TestSystem
#
# Tests the System class
#
# Author P G Jones - 2014-02-15 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import unittest
import nusoft.system.standard
import os

class TestSystem(unittest.TestCase):
    
    def setUp(self):
        super(TestSystem, self).setUp()
        self._system = nusoft.system.standard.Standard(os.getcwd())
    def test_remove(self):
        """ Test the system removes files. 

        First create a temporary empty file in the temporary path then remove it.
        """
        test_file = os.path.join(self._system.get_temporary_path(), "nusoft.test")
        with open(test_file, 'a'):
            os.utime(test_file, None)
        self.assertTrue(os.path.exists(test_file))
        self._system.remove(test_file)
        self.assertFalse(os.path.exists(test_file))
    def test_download(self):
        """ Test the system can download files.

        Try to download a small tar.
        """
        test_file = os.path.join(self._system.get_temporary_path(), "nusoft.test")
        self._system.download("http://www.github.com", name=test_file)
        self.assertTrue(os.path.exists(test_file))
        os.remove(test_file)
    def test_untar(self):
        """ Test the system can untar files.

        Download the a small tar and untar.
        """
        
    def test_exists(self):
        """ Test the system believes files exist"""
        self.assertTrue(os.path.exists(__file__) == self._system.exists(__file__))

if __name__ == '__main__':
    unittest.main()
