from vSens1 import vSens1
import unittest



class UnitT(unittest.TestCase):

    def setUp(self):
        
        self.obj = vSens1.vSensCalculator(path,58156,5,1,1)
        self.test_read_file()

    
    def test_read_file(self):
        self.assertNotEqual(len(self.obj.read_file()),0)
    
    def test_get_time_seconds(self):
        ans=self.obj.get_time_seconds(1000)
        self.assertEqual(ans,1)
        ans=self.obj.get_time_seconds(10000)
        self.assertEqual(ans,10)

    def test_get_connected_time(self):
        ans=self.obj.get_connected_time(1000,100)
        self.assertEqual(ans,900)

    def test_calculate_packetloss(self):
        x=1/60
        ans=self.obj.calculate_packetloss(882,x,52906.87)
        self.assertEqual(ans,-0.02)

    def test_calculate_packetloss(self):
        ans=self.obj.calculate_packetloss(260030,5,52906.87)
        self.assertEqual(ans,1.7)

    def test_calculate_packetloss(self):
        x=1/60
        ans=self.obj.calculate_packetloss(883,x,52906.87)
        self.assertEqual(ans,-0.14)

    def test_total_packets_time(self):
        disconnections,acc_count,temp_count,battery_count=self.obj.total_packets_time()
        print(disconnections,acc_count,temp_count,battery_count)
        self.assertEqual(disconnections,16)
        self.assertEqual(temp_count,882)
        self.assertEqual(battery_count,883)
        self.assertEqual(acc_count,260030)

    def test_input(self): #test to check whether input_testing raises exception or not for negative values
        with self.assertRaises(Exception): vSens1.input_testing(58156,-1,1,1)
    
if __name__ == "__main__":
    path=input("enter the lod file path for unit testing :")
    unittest.main()
