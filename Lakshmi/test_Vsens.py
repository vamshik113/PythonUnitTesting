import Vsens
import unittest

class Test_Vsens(unittest.TestCase):

    def setUp(self):
        self.obj = Vsens.Vsens(Vsens.path,Vsens.expected_time_from_user,Vsens.Accelerometer_packets,Vsens.Temperature_packets,Vsens.Battery_packets)
        self.test_Readfile()
    def test_Readfile(self):
        self.assertNotEqual(len(self.obj.Readfile()),0)
    
    def test_Count_packets(self):
        a_count,t_count,b_count,d_count = self.obj.Count_packets()
        self.assertEqual(a_count,260030)
        self.assertEqual(t_count,882)
        self.assertEqual(b_count,883)
        self.assertEqual(d_count,16)

    def test_Convert_seconds(self):
         self.assertEqual(self.obj.Convert_seconds(1000),1)
    
    def test_input_values(self):
        self.assertRaises(ValueError,self.obj.Actual_time_calculate,-58156,5249.13)
        
    def test_Actual_time_calculate(self):
        self.assertEqual(self.obj.Actual_time_calculate(-5,2),-7,3)


    def test_Calculate_packet_loss(self):
        self.assertAlmostEqual(self.obj.Calculate_packet_loss(5,260030,52906.87),1.7)



if __name__ == '__main__':
    unittest.main()
