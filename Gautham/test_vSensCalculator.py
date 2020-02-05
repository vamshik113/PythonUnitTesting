# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:08:52 2020

@author: Gautam
"""

import unittest
from vSens_calculator1 import vSens_Calculator
class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.obj=vSens_Calculator("806FB0AFF64C_vSens_PackeIDLog.txt",58156,5,1,1)
        self.test_openfile()
    def test_openfile(self):
        self.assertNotEqual(len(self.obj.openfile()),0)
     
    def test_final_compute(self):
        ans=self.obj.final_compute(100,10)
        self.assertEqual(ans,90)
    
    def test_compute_data(self):
        accelerometer,temperature,battery,disconnections,connections=self.obj.compute_data()
        self.assertEqual(accelerometer,260030)
        self.assertEqual(temperature,882)
        self.assertEqual(battery,883)
        self.assertEqual(disconnections,15)
        self.assertEqual(connections,16)
    
    def test_packet_loss(self):
        rate=1/60
        accelerometer_loss=self.obj.packet_loss(260030,5,52906.87)
        self.assertEqual(accelerometer_loss,1.702746732135178 )
        temperature_loss=self.obj.packet_loss(882,rate,52906.87)
        self.assertEqual(temperature_loss,-0.024817192927876888)
        battery_loss=self.obj.packet_loss(883,rate,52906.87)
        self.assertEqual(battery_loss,-0.13822401514208082) 
    
if __name__ == '__main__':
    unittest.main() 