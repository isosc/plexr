from unittest import TestCase

import os
import subprocess

class TestPlxrCLI(TestCase):

    def test_plxr_help(self):
        cp = subprocess.run(['plxr','-h'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)
 
    def test_plxr_insert(self):
        cp = subprocess.run(['plxr','insert', 'test_plxr_cli.bp', "{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__))), 'A'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)

    def test_plxr_insert_multiple(self):
        cp = subprocess.run(['plxr','insert', 'test_plxr_cli.bp', "{}/images/simple-3x3-1.png".format(os.path.dirname(os.path.abspath(__file__))), 'A'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)
        cp = subprocess.run(['plxr','insert', 'test_plxr_cli.bp', "{}/images/simple-3x3-2.png".format(os.path.dirname(os.path.abspath(__file__))), 'B'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)
        cp = subprocess.run(['plxr','insert', 'test_plxr_cli.bp', "{}/images/simple-3x3-3.png".format(os.path.dirname(os.path.abspath(__file__))), 'C'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)
        cp = subprocess.run(['plxr','insert', 'test_plxr_cli.bp', "{}/images/simple-3x3-4.png".format(os.path.dirname(os.path.abspath(__file__))), 'D'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)

    def test_plxr_extract(self):
        # Borrow the inserts from the insert test
        self.test_plxr_insert()

        # Now try extracting
        cp = subprocess.run(['plxr','extract', 'test_plxr_cli.bp', 'A'])
        exit_status = cp.returncode
        self.assertEqual (exit_status, 0)

        

