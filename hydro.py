


class Hydro:
    def __init__(self):
        self.last_checked_time = None
        self.humidity = ""
        self.temp = ""
        self.current_light_status = True
        self.light_status_on = True 
        self.light_on_time = 6
        self.light_off_time = 20
        self.data_write_frequency = 30

    def switch_light_on(self,current_hour):
        if int(current_hour) >= self.light_on_time and int(current_hour) <= self.light_off_time:
            self.light_status_on = True
            return True
        else:
            self.light_status_on = False
            return False
    
    

    def writeClimateData(self,previous_time,current_time):
        current_hour = int(current_time[0])
        current_minute = int(current_time[1])
        previous_hour = int(previous_time[0])
        previous_minute = int(previous_time[1])
        # Convert both times to minutes
        current_total_minutes = current_hour * 60 + current_minute
        previous_total_minutes = previous_hour * 60 + previous_minute
        # Calculate the difference
        difference = current_total_minutes - previous_total_minutes
        if difference < 0:
            difference += 24 * 60
        if difference >= self.data_write_frequency:
            print("differnece is more than frequency so we will be writing data")
            return True
        else:
            print("differnece is less than frequency so we will NOT be writing data")
            return False
    
    def setLastTimeChecked(self,current_hour,current_minute):
        int_of_current_minute = int(current_minute)
        print("current min before: ",int_of_current_minute)
        if int_of_current_minute <= 15 and int_of_current_minute >=0:
            str_of_current_minute  = "00"
        elif int_of_current_minute <= 30 and int_of_current_minute >15:
            str_of_current_minute  = "30"
        elif int_of_current_minute <= 45 and int_of_current_minute >30:
            str_of_current_minute  = "30"
        else:
            str_of_current_minute  = "00"
        print("adjusted current start time: ",str_of_current_minute)
        self.last_checked_time = (current_hour,str_of_current_minute)
    def getLastTimeChecked(self):
        return self.last_checked_time
        
    def setTemp(self,temp):
        self.temp = temp
    def getTemp(self):
        return self.temp

    def setHumidity(self,humidity):
        self.humidity=humidity
    def getHumidity(self):
        return self.humidity
    
    def getLightStatus(self):
        return self.light_status_on
    
    

    