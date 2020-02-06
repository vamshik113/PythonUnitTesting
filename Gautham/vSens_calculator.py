import json
class vSens_Calculator:
    def __init__(self,openfile1,input_time,accelerator_per_sec,temperature_per_sec,battery_per_sec):
        self.count_PID0=0
        self.count_PID998=0
        self.count_PID1=0
        self.count_PID2=0
        self.count_PID999=0
        self.time_difference=0
        self.input_time=input_time
        self.accelerator_per_sec=accelerator_per_sec
        self.temperature_per_sec=temperature_per_sec
        self.battery_per_sec=battery_per_sec
        self.openfile1=openfile1
        self.list_given=[]
        
    def openfile(self,list_given):
    
        with open(self.openfile1) as file:
            for line in file:
                self.list_given.append(json.loads(line.strip()))
        return self.list_given
    def compute_data(self,count_PID0,count_PID1,count_PID2,count_PID998,count_PID999):
        flag=0
        for id in range(len(self.list_given)):
        
            if(self.list_given[id]["PID"]=="0"):
                self.count_PID0+=1
            elif(self.list_given[id]["PID"]=="1"):
                self.count_PID1+=1
            elif(self.list_given[id]["PID"]=="2"):
                self.count_PID2+=1
            elif(self.list_given[id]["PID"]=="998"):
                self.count_PID998+=1
                if(flag == 0):
                    store_index=id
                flag=1
            elif(self.list_given[id]["PID"]=="999" and flag==1):
                self.count_PID999+=1
                self.time_difference=self.time_difference+((self.list_given[id]["TS"]-self.list_given[store_index]["TS"])/1000)
                flag=0
        self.count_PID999+=1
        return self.count_PID0,self.count_PID1,self.count_PID2,self.count_PID998,self.count_PID999
    def packet_loss(self,sensorcount,packets_per_sec,actual_time):
        self.percentage_loss=0
        self.expected_packet=actual_time * packets_per_sec
        self.percentage_loss=((self.expected_packet-sensorcount)/self.expected_packet) * 100
        return self.percentage_loss
    
    def final_compute(self,input_time,time_difference):
        
        self.actual_time=float(input_time)-time_difference
        print("Actual test time:",self.actual_time)
        return self.actual_time
    
    def get_info(self):
        
        self.openfile(self.list_given)
        self.compute_data(self.count_PID0,self.count_PID1,self.count_PID2,self.count_PID998,self.count_PID999)
        self.final_compute(self.input_time,self.time_difference)
        self.accelerometer_packet=self.packet_loss(self.count_PID0,self.accelerator_per_sec,self.actual_time)
        self.temperature_packet=self.packet_loss(self.count_PID1,self.temperature_per_sec,self.actual_time)
        self.battery_packet=self.packet_loss(self.count_PID2,self.battery_per_sec,self.actual_time)
        print("overall disconnections:",self.count_PID998)
        print("Packet loss for accelerometer:",self.accelerometer_packet,"%")
        print("Packet loss for temperature:",self.temperature_packet,"%")
        print("Packet loss for battery:",self.battery_packet,"%")
        
        
open_file=str(input("Enter the filename to open with .txt extension:"))  

Test_time=int(input("Enter the input test time:"))

accelerometer_packets=int(input("Enter the Accelerometer packets data:"))

temperature_packets=int(input("Enter the temperature packets data per min:"))

battery_packets=int(input("Enter the Battery packets data per min:"))

battery_packets=battery_packets/60

temperature_packets=temperature_packets/60

vSens=vSens_Calculator(open_file,Test_time,accelerometer_packets,temperature_packets,battery_packets)

vSens.get_info()