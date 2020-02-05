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
        self.rate_seconds=0
        self.filename = filename
        self.Accelerometer_rate = acc_rate
        self.temp_rate=temp_rate
        self.battery_rate=battery_rate
        self.total_time = time
        
    def read_file(self):
        with open(self.filename) as file:
            for l in file:
                self.List.append(json.loads(l.strip()))
        return self.List

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
        print("acceleromete count=",self.accelerometer_sensor)
        print("temperature count=",self.temperature_sensor)
        print("battery count=",self.battery)
        print("disconnected time in milisec=",self.time_diff)
        return self.total_disconnections,self.accelerometer_sensor, self.temperature_sensor,self.battery
        self.accelerometer_sensor, self.temperature_sensor,self.battery
                    
    def get_time_seconds(self,disconnect_time):
        self.time_seconds = round(disconnect_time  / 1000 ,2)
        #print("disconnected time in sec =",self.time_seconds)
        return self.time_seconds
        
    def get_connected_time(self,total_time,connected_time_sec):
        self.connected_time = round(total_time - connected_time_sec,2)
        #print("connected time=",self.connected_time)
        return self.connected_time
    
    
        
    def calculate_packetloss(self,expected_packet_count,rate,connect_time):
        self.actual_count =float(connect_time* rate) 
        self.packet_loss = round(((self.actual_count - expected_packet_count)/self.actual_count)*100 ,2)
        print("packet loss=",self.packet_loss)
        return self.packet_loss

    def get_packetloss(self):
        self.List=self.read_file()
        self.total_disconnections ,self.accelerometer_sensor, self.temperature_sensor,self.battery=self.total_packets_time()
        #print(self.total_disconnections,self.accelerometer_sensor, self.temperature_sensor,self.battery)
        self.time_seconds=self.get_time_seconds(self.time_diff)
        self.connected_time=self.get_connected_time(self.total_time,self.time_seconds)
        self.acc_packet_loss=self.calculate_packetloss(self.accelerometer_sensor,self.Accelerometer_rate,self.connected_time)
        self.temp_packet_loss=self.calculate_packetloss(self.temperature_sensor,self.temp_rate,self.connected_time)
        self.battery_packet_loss=self.calculate_packetloss(self.battery,self.battery_rate,self.connected_time)
        print("\nTotal disconnections :",round(self.total_disconnections,2),"\nActual Connected time =",self.connected_time,"\nAccelerometer packet loss = ",self.acc_packet_loss,"\nTemperature packet loss = ",self.temp_packet_loss,"\nBattery packet loss = ",self.battery_packet_loss)
        
def input_testing(total_time,Accelerometer_rate,temp_rate,batterydata_rate):
    if(total_time <= 0  ):
        raise ValueError("Total time must be graeter than zero!!!!")
    if(Accelerometer_rate <= 0):
       Exception('lets see if this works')
    if(temp_rate <= 0  ):
        raise ValueError("temperature packet rate cannot be negative or zero")
    if(batterydata_rate <=0):
        raise ValueError("battery packet rate cannot be negative or zero")

        

    
        
    
        
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

input_testing(total_time,Accelerometer_rate,temp_rate,batterydata_rate)
temp_rate = temp_rate / 60
batterydata_rate = batterydata_rate/60  

vSens = vSensCalculator(filename,total_time,Accelerometer_rate,temp_rate,batterydata_rate)
vSens.get_packetloss()