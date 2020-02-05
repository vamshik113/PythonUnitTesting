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
        new_list = []
        with open(self.path,'r') as f:
            for i in f:
                self.data_list.append(json.loads(i))
        new_list = self.data_list
        return new_list
    
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

        return self.acc_count,self.temp_count,self.battery_count,self.disconnected_count
        
    def Convert_seconds(self,sum_diff):
        self.time_in_sec = sum_diff/1000
        return self.time_in_sec

    def Actual_time_calculate(self,expected_t_user,t_sec):
        if expected_t_user <= 0:
            raise ValueError("Expected time cannot be neagative number")
        self.Actual_test_time = float(expected_t_user) - t_sec
        return self.Actual_test_time
        
    def Calculate_packet_loss(self,expected_packets,actual_count,actual_test_time):
        
        self.Actual_packets_recieved = actual_test_time*float(expected_packets)
        self.packet_loss = round(((self.Actual_packets_recieved - actual_count)/self.Actual_packets_recieved)*100,2)
        return self.packet_loss

    def Function_call(self):
        self.Readfile()
        self.Count_packets()
        self.Convert_seconds(self.sum_of_diff_time)
        self.Actual_time_calculate(self.expected_time_from_user,self.time_in_sec)
        Acc_packet_loss = self.Calculate_packet_loss(self.Accelerometer_packets,self.acc_count,self.Actual_test_time)
        self.Temperature_packets = (float(self.Temperature_packets)*(1/60))
        Temp_packet_loss = self.Calculate_packet_loss(self.Temperature_packets,self.temp_count,self.Actual_test_time)
        self.Battery_packets = (float(self.Battery_packets)*(1/60))
        Battery_packet_loss = self.Calculate_packet_loss(self.Battery_packets,self.battery_count,self.Actual_test_time)
        print('***************OUTPUT*************')
        print('Actual time is : ',self.Actual_test_time,'\n','Disconnected count : ',self.disconnected_count,'\n','Packet loss for accelerometer : ',Acc_packet_loss,'\n','Packet loss for temperature : ',Temp_packet_loss,'\n','Packet loss for battery : ',Battery_packet_loss)


path = input("Enter file path : ")
expected_time_from_user = float(input("Enter the expected time in seconds : "))
Accelerometer_packets = int(input("Enter expected accelerometer packets : "))
Temperature_packets = int(input("Enter expected tempreature packets : "))
Battery_packets  = int(input("Enter expected battery packets : "))
sensor = Vsens(path,expected_time_from_user,Accelerometer_packets,Temperature_packets,Battery_packets)
sensor.Function_call()

'''def User_choice(choice):
    if choice == 1:'''
        


    