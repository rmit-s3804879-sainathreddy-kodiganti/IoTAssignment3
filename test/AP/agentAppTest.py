import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/AP'))
sys.path.append(os.path.abspath('../../src/Socket'))
sys.path.append(os.path.abspath('../../src/Facial recognition'))
import pathlib
from agentApp import agentApp
from recognise import recognise
from reception import reception
import pexpect

class agentAppTest(unittest.TestCase):
    """This is the agentAppTest Class

    This is used to test the AP modules.
    """
    def test_readConfig(self):
        agent_obj = agentApp()
        agent_obj.read_config()
        self.assertFalse(agent_obj.get_car_id() is None)

    def test_checkCarID(self):
        agent_obj = agentApp()
        agent_obj.read_config()
        self.assertEquals(agent_obj.get_car_id(), "1")
    
    def test_calculateCostIncurred(self):
        agent_obj = agentApp()
        cost = agent_obj.calculate_cost_incurred(2500, "25")
        self.assertTrue(cost>0)

    def test_bluetooth_scan(self):
        agent_obj = agentApp()
        child = pexpect.spawn("bluetoothctl")
        child.send("scan on\n")
        index = child.expect('Device .*', timeout=60)
        self.assertTrue(index>=0)

if __name__ == '__main__':
    unittest.main()
