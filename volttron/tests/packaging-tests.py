import unittest
import os
import shutil
import sys
import uuid

from collections import namedtuple
from wheel.install import WheelFile

from volttron.platform.packaging import (create_package,
                                         extract_package)
                                 
from volttron.platform.packaging import AgentPackageError

# Temporary path for working during running of package/unpackage tests.
TMP_AGENT_DIR = '/tmp/agent-dir'

AGENT_TESTCASE1_NAME = 'test-agent-package'

class TestPackaging(unittest.TestCase):

    def get_agent_fixture(self, agent_name):
        return os.path.join(self.fixtureDir, agent_name)
    
    def setUp(self):
        '''
        Recreates the temporary agent directory before each run
        '''
        if os.path.exists(TMP_AGENT_DIR):
            shutil.rmtree(TMP_AGENT_DIR)
        os.makedirs(TMP_AGENT_DIR)
        
        self.fixtureDir = os.path.join(os.path.dirname(__file__), "fixtures")
    
#     def test_can_sign_wheel(self):
#         wheel_package = create_package(get_agent_fixture(AGENT_TESTCASE1_NAME))
#         
        
    def test_can_extract_package(self):
        agent_name = AGENT_TESTCASE1_NAME
        wheelhouse = '/tmp/extract_package/'
        package_name = create_package(self.get_agent_fixture(agent_name),"/tmp/create_tmp_package/")
         
        installed_at = extract_package(package_name, wheelhouse)
         
        try:
            whl = WheelFile(package_name)
            self.assertTrue(whl.datadir_name in installed_at)
        finally:
            shutil.rmtree(installed_at)
            shutil.rmtree(wheelhouse)

    def test_can_create_an_initial_package(self):
        '''
        Tests that a proper wheel package is created from the create_package method of
        the AgentPackage class.
        '''
        agent_name = AGENT_TESTCASE1_NAME
         
        package_name = create_package(self.get_agent_fixture(agent_name),"/tmp/create_package")
         
        self.assertIsNotNone(package_name, "Invalid package name {}".format(package_name))
        # Wheel is in the correct location.
        print(package_name)
        self.assertTrue(os.path.exists(package_name))
         
        self.assertTrue('listeneragent' in package_name)
         
        try:
            # TODO Verify zip structure.
            whl = WheelFile(package_name)
            whl.zipfile.close()
        finally:
            os.remove(package_name)
    
    def test_raises_error_if_agent_dir_not_exists(self):
        '''
        This test passes under the following conditions:
            1. An AgentPackageError is thrown if the passed agent directory 
               doesen't exists.
        '''
        # 
        fake_agent = '/tmp/Fake'
        if os.path.exists(fake_agent):
            shutil.rmtree(fake_agent, True)
            
        self.assertRaises(AgentPackageError, lambda: create_package(fake_agent))
        

