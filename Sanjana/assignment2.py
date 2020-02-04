
import json

class vSensCalculator:
    def __init__(self,filename,time,acc_rate,temp_rate,battery_rate):
        self.List = []
        self.count=0
        self.accelerometer_sensor=0
        self.temperature_sensor=0
        self.battery=0
        self.total_disconnections=0
        self.time_diff=0
        self.actual_count=0
        self.filename = filename
        self.Accelerometer_rate = acc_rate
        self.temp_rate=temp_rate
        self.battery_rate=battery_rate
        self.total_time = time
        
    def read_file(self):
        with open(self.filename) as file:
            for l in file:
                self.List.append(json.loads(l.strip()))

    def total_packets_time(self):
        flag = 0
        index=0
        for element in range(len(self.List)):
            if(self.List[element]["PID"] =="998" ):
                self.total_disconnections += 1
                if(flag != 1):
                    flag=1
                    index=element
            elif(self.List[element]["PID"] =="0"):
                self.accelerometer_sensor += 1
            elif(self.List[element]["PID"] =="1"):
                self.temperature_sensor += 1
            elif(self.List[element]["PID"] =="2"):
                self.battery += 1
            else:
                if(flag==1):
                    self.time_diff = self.time_diff + (self.List[element]["TS"]-self.List[index]["TS"])
                    flag = 0
                    
    def get_time_seconds(self):
        self.time_seconds = self.time_diff / 1000
        
    def get_connected_time(self):
        print(self.total_time,self.time_seconds)
        self.connected_time = self.total_time - self.time_seconds
        
    def calculate_packetloss(self,expected_packet_count,rate):
        self.actual_count = float(self.connected_time * rate)
        self.packet_loss = ((self.actual_count - expected_packet_count)/self.actual_count)*100
        return self.packet_loss

    def get_packetloss(self):
        self.read_file()
        self.total_packets_time()
        self.get_time_seconds()
        self.get_connected_time()
        self.acc_packet_loss=self.calculate_packetloss(self.accelerometer_sensor,self.Accelerometer_rate)
        self.temp_packet_loss=self.calculate_packetloss(self.temperature_sensor,self.temp_rate)
        self.battery_packet_loss=self.calculate_packetloss(self.battery,self.battery_rate)
        print("\nTotal disconnections :",self.total_disconnections,"\nActual Connected time =",self.connected_time,"\nAccelerometer packet loss = ",self.acc_packet_loss,"\nTemperature packet loss = ",self.temp_packet_loss,"\nBattery packet loss = ",self.battery_packet_loss)
        
        
total_disconnections=0
connected_time=0
acc_packet_loss=0
temp_packet_loss=0
battery_packet_loss=0

filename = input("enter log file path : ")
total_time = int(input("Enter the total time :"))
Accelerometer_rate = int(input("Enter rate at which accelerometr sends data per second : "))
temp_rate = float(input("temperature data packet rate per minute : "))
batterydata_rate = float(input("Battery data packet rate per minute : "))

temp_rate = temp_rate / 60
batterydata_rate = batterydata_rate/60  

vSens = vSensCalculator(filename,total_time,Accelerometer_rate,temp_rate,batterydata_rate)
vSens.get_packetloss()

