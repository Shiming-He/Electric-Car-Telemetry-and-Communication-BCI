
import time

class Car_data_CA:
    '''object Car_data_CA
    used to store and compute data from the Cycle Analyst'''
    
    def __init__(self, total_time, battery_ah, if_read_speed = False ):
        '''Car_data_CA(total_time, battery_ah) -> Car_data_CA
        create Car_data_CA object
        total_time is the total time for the race'''
        #initalize variables
        
        #battery variables
        self.total_ah = battery_ah
        self.ah_spent = 0
        self.ah_left_in_battery = 0
        self.ah_spent_per_min = 0
        self.previous_ah_value =  0
        self.eraised_ah = 0
        self.past_minute_ah_vals = {}
        
        #time variables
        self.total_time = total_time
        self.start_time = time.time()
        self.end_time = self.start_time +  self.total_time
        
        #speed variables if applicable
        self.if_read_speed = if_read_speed
        if if_read_speed:
            self.speed = 0
        
    def update(self, data_frame):
        '''Car_data_CA.update(data_frame, pres_time) -> None
        updates the data and calculations
        data_frame is a list of a full frame of data from the CA'''
        
        #Check if the frame received is not cut up.
        if len(data_frame) == 5:
            
            #get the Ah value
            recieved_ah_val = abs(float(data_frame[0]))
            #get the speed if applicable
            if self.if_read_speed:
                self.speed = float(data_frame[4])
                
            
            #check if the CA reset. In order to make sure the revious values are not lost
            if self.previous_ah_value >  recieved_ah_val:
                self.eraised_ah = self.ah_spent
                
            #update the battery variables
            self.ah_spent = self.eraised_ah + recieved_ah_val
            self.ah_left_in_battery = self.total_ah - self.ah_spent
            self.past_minute_ah_vals[time.time()] = self.ah_spent
            
            # find the new Ah per minute expenditure
            self.update_ah_per_min()
            
            # used to make sure it can detect a CA rest
            self.previous_ah_value = recieved_ah_val
            
        else:
            time.sleep(1)
            
            
            
    def update_ah_per_min(self):
        '''.get_ah_per_min() -> None
        updates Ah per minute expenditure'''
        #initalize variables
        pres_time = time.time()
        time_stamps = self.past_minute_ah_vals.keys()
        time_between = 0
        last_val = 0
        dif_val = 0
        
        #find the new Ah per minute expenditure
        if len(time_stamps) > 1:
            for key in time_stamps:
                
                if key > pres_time+125:
                    self.past_minute_ah_vals.pop(key)# delete any old keys
                elif key > pres_time+115:
                    self.ah_spent_per_min = (self.ah_spent - self.past_minute_ah_vals[key])/(key-pres_time) # Ah per min
                    self.past_minute_ah_vals.pop(key) # delete the keys that has been used.
            
            
    def get_total_ah(self):
        '''Car_data_CA.get_total_ah() -> float
        returns total Ah'''
        return self.total_ah
    
    def get_ah_per_min(self):
        '''Car_data_CA.get_ah_per_min() -> float
        return present Ah per minute expenditure'''
        return self.ah_spent_per_min
    
    def get_ah_spent(self):
        '''Car_data_CA.get_ah_spent() -> float
        returns Ah spent by the battery up to the present'''
        return self.ah_spent
    
    def get_remaining_time(self):
        '''Car_data_CA.get_remaining_time() -> float
        returns the remaning time in the race in minutes'''
        return (self.end_time-time.time())/60
    
    def get_ah_left_in_battery(self):
        '''Car_data_CA.get_ah_left_in_battery() -> float
        returns how many Ah are left in the battery'''
        return self.ah_left_in_battery
    
    def get_predict_target_ah(self):
        '''Car_data_CA.get_predict_target_ah() -> float
        returns computer perdict target ah'''
        return self.ah_left_in_battery/self.get_remaining_time()
    
    def get_time_remaining_percent(self):
        '''Car_data_CA.get_time_remaining_percent() -> float
        returns remaining time in a percent of the total time'''
        return self.get_remaining_time()*60/self.total_time
    
    def get_total_time(self):
        '''Car_data_CA.get_total_time() -> int
        returns total time of the race'''
        return self.total_time
    
    def update_time(self, sent_time):
        '''Car_data_CA.update_time(sent_time) -> None
        update the time left in the race'''
        self.end_time = time.time() +  sent_time
    
    def get_start_time(self):
        '''Car_data_CA.get_start_time() -> int
        returns the starting time of the race'''
        return self.start_time()    