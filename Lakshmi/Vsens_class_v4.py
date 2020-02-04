import json

class Vsens:
    
    def __init__(self,path,expected_time_from_user,Accelerometer_packets,Temperature_packets,Battery_packets):
        self.path = path
        self.data_list = []
        self.Accelerometer_packets = Accelerometer_packets
        self.Temperature_packets = Temperature_packets
        self.Battery_packets = Battery_packets
        self.acc_count = 0
        self.temp_count = 0
        self.battery_count = 0
        self.disconnected_count = 0
        self.PID_998 = []
        self.PID_999 = []
        self.expected_time_from_user = expected_time_from_user
        self.sum_of_diff_time = 0
        self.Actual_test_time = 0
        
    def Readfile(self):
        with open(self.path,'r') as f:
            for i in f:
                self.data_list.append(json.loads(i))
        return self.data_list
    
    def Count_packets(self):
        self.diff_time =0
        self.index = 0
        self.flag = 0
        for i in range(len(self.data_list)):
            
            if self.data_list[i]['PID'] == '0':
                self.acc_count += 1
            elif self.data_list[i]['PID'] == '1':
                self.temp_count += 1
            elif self.data_list[i]['PID'] == '2':
                self.battery_count += 1
            elif self.data_list[i]['PID'] == '998':
                 self.disconnected_count += 1
                 if self.flag == 0:
                    self.index = i
                    self.flag = 1    
            elif self.data_list[i]['PID'] == '999' and self.flag == 1:
                self.PID_999.append(self.data_list[i]) 
                self.diff_time = self.data_list[i]['TS'] - self.data_list[self.index]['TS']
                self.sum_of_diff_time = self.sum_of_diff_time + self.diff_time
                self.flag = 0
      
    def Actual_time_calculate(self):
        self.time_in_sec = self.sum_of_diff_time/1000
        self.Actual_test_time = float(self.expected_time_from_user) - self.time_in_sec
        
    def Calculate_packet_loss(self):
        self.Actual_accelerometer_packets_recieved = self.Actual_test_time*float(self.Accelerometer_packets)
        self.packet_loss_acc = ((self.Actual_accelerometer_packets_recieved - self.acc_count)/self.Actual_accelerometer_packets_recieved)*100
    
        self.Temperature_packets = (float(self.Temperature_packets)*(1/60))
        self.Actual_temp_packets_recieved = self.Actual_test_time*float(self.Temperature_packets)
        self.packet_loss_temp = ((self.Actual_temp_packets_recieved - self.temp_count)/self.Actual_temp_packets_recieved)*100
    
        self.Battery_packets = (float(self.Battery_packets)*(1/60))
        self.Actual_battery_packets_recieved = self.Actual_test_time*float(self.Battery_packets)
        self.packet_loss_battery = ((self.Actual_battery_packets_recieved - self.battery_count)/self.Actual_battery_packets_recieved)*100
    
        print('*************************OUTPUT*******************************')
        print('Actual time is : ',self.Actual_test_time,'\n','Disconnected count : ',self.disconnected_count,'\n','Packet loss for accelerometer : ',self.packet_loss_acc,'\n','Packet loss for temperature : ',self.packet_loss_temp,'\n','Packet loss for battery : ',self.packet_loss_battery)

    def Function_call(self):
        self.Readfile()
        self.Count_packets()
        self.Actual_time_calculate()
        self.Calculate_packet_loss()

path = input("Enter file path : ")
expected_time_from_user,Accelerometer_packets,Temperature_packets,Battery_packets  = input("Enter the expected time in seconds ,expected accelerometer packets per second,expected temperature packets per minute,expected battery packets per minute separeted by comma : ").split(',')
sensor = Vsens(path,expected_time_from_user,Accelerometer_packets,Temperature_packets,Battery_packets)
sensor.Function_call()


    