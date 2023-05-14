# Main authour: Shiming He
# Other contributers
# May 2022
# Update 1.0
# Version 1.0

#A speical thanks to Austin Wang and Steven Cao, for their work on the orginal Raspberry Pi Data Management System.
#This file is partially based on the Raspberry Pi Data Management System by Austin Wang and Steven Cao.


import time
import serial

#required for the calculations and display
from pygame_display import Ecar_display_pygame
from data_compute import Car_data_CA

# Required to use APIs of PubNub Python SDK
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException


#initalize variables
ENTRY = "earth"
CHANNEL = "the_guide"
carData = None

# The targe ah per minute for the car
target_ah = 0 

#set the method and signal given to the driver
prediction_Mode = 'semiAuto'
speed_signal = 'Center'

# check if the code has been started on the computer end
start_var = False

#initalize the variable for the computing class for later use
CA_Car_data = None

# find the target speed difference
target_speed_difference = 0

#This is last time that the display was updated
last_update_time = 0


#set up the pygame display window
pygame_display = Ecar_display_pygame.Ecar_pygame_display()



# Set up the config property for PubNub
pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-f418f6ca-711a-402a-b373-fe542788cf3b" # Add the piblish key for your PubNub Channel
pnconfig.subscribe_key = "sub-c-3a2983ca-ce37-11ec-ab76-de5c934881d6" # Add the Subscribe key for your PubNub Channel
pnconfig.uuid = "serverUUID-PUB"

# Initialize a PubNub object to make PubNub API calls.
pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

# listener for PubNub Channel
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('my_channel').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        global start_var
        global target_ah
        global prediction_Mode
        global speed_signal
        global CA_Car_data
        # Handle new message stored in message.message
        # process the message from the computer (Houston)
        message_val = message.message
        if message_val['entry'] == 'Houston':
            
            #make sure that the data is in the correct format
            if type(message.message['update']) == dict:
                
                #start the time and battery info
                if message_val['update'].get('Time'):
                    start_time = time.time()
                    total_time = float(message_val['update']['Time'])*60
                    end_time = start_time + total_time
                    start_var = True
                    
                #set the battery values
                if message_val['update'].get('Battery'):
                    total_ah_battery = float(message_val['update']['Battery'])
                    CA_Car_data = Car_data_CA.Car_data_CA(total_time, total_ah_battery)
                    
                #if update a new remaining time
                elif message_val['update'].get('Time') and type(CA_Car_data) != str:
                    CA_Car_data.update_time(total_time)
                    
                #if receiving a new target value
                if message_val['update'].get('Target'):
                    target_ah = float(message_val['update']['Target'])
                    prediction_Mode = 'semiAuto'
                    
                #if receiving a new perdiction mode value
                if message_val['update'].get('Perdiction Mode'):
                    prediction_Mode = message_val['update']['Perdiction Mode']
                    if prediction_Mode == 'man':
                        speed_signal = 'Center'
                        
                #if receiving a new Speed Signal value
                if message_val['update'].get('Speed Signal'):
                    prediction_Mode = 'man'
                    speed_signal = message_val['update']['Speed Signal']
                

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).execute()


# read serial data in order to receive infomration from the Cycle Analyst
ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1) # change the serial port to the port which is corresponding with the Cycle Analyst
ser.close()
ser.open()

# to make sure that the serial will be closed 
try:
    while True:
        
        # initalize the carData variable
        carData = ''
        
        # read the information from the serial port connected to the Cycle Analyst
        try:
            bytesToRead = ser.in_waiting #get all bytes to stop backlogged data
            carData = ser.read(bytesToRead).decode('ascii')
        except:
            pass
        
        #if no new informatio was read
        if carData == "" or carData == None:
            carData = "blank"
            try:
               the_message = {"entry": ENTRY, "update": 'raw '+ carData}
               envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()
            except:
               continue
            
        if start_var:
            
            #this seperates the frame for the message that was received
            remaining_car_data = carData.splitlines()
            
            # make sure that we are reading a full frame
            if len(remaining_car_data) >2:
                data_segment =remaining_car_data[1]
                
                
                data_segment = data_segment.split()#splits the frame into corresponding values in the format Ah V A Speed Distance                
                
                # publish the raw frame
                try:
                    data_seg = ' '.join(data_segment)
                    the_message = {"entry": ENTRY, "update": 'raw '+ data_seg}
                    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()
                except:
                    print('Fail to Publish raw frame')
                    continue
                
                
                # update the calculations with the new data frame
                CA_Car_data.update(data_segment)
                
                # publish the data that has been processed
                output_data = str(CA_Car_data.get_ah_spent()) + ' ' + str(CA_Car_data.get_ah_left_in_battery()) + ' ' + str(CA_Car_data.get_remaining_time()) + ' ' + str(CA_Car_data.get_ah_per_min()) + ' ' + str(CA_Car_data.get_predict_target_ah())
                try:
                    the_message = {"entry": ENTRY, "update": 'prep '+ output_data}
                    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()
                except:
                    continue
                
            # if there not enough frames
            else:
                #wait for a second in order for more frames to accumulate
                time.sleep(1)
                
                
            #start the screen only when the systems information has been sent from the computer
            if start_var:
                
                #make sure the speed signals only updates every 2 minutes to avoid distracting the driver
                get_time_period_rem_time = (time.time() % 120)
                if (5 >= get_time_period_rem_time or get_time_period_rem_time >= 115) and  not (5 >= last_update_time or last_update_time >= 115): 
                    # it will display the latest signal received in the past 2 minutes
                    
                    # manual mode
                    if prediction_Mode == 'man':
                        if speed_signal == 'Speed Up':
                            target_speed_difference = 5
                        elif speed_signal == 'Center':
                            target_speed_difference = 0
                        else:#speed_signal is Slow Down
                            target_speed_difference = -5
                    else:
                        # automatic mode
                        if prediction_Mode == 'auto':
                            target_ah = CA_Car_data.get_predict_target_ah()
                        # set the speed signal for automatic and semi-automatic modes 
                        target_speed_difference = (target_ah - CA_Car_data.get_ah_per_min())*20
                
                #make sure it doesn't update repeatedly
                last_update_time = get_time_period_rem_time
                
                #update the display window
                pygame_display.update(CA_Car_data.get_ah_left_in_battery()/CA_Car_data.get_total_ah(), CA_Car_data.get_time_remaining_percent(), target_speed_difference, total_time = CA_Car_data.get_total_time()/60)
                        
                #print the status of the published information into the console
                if envelope.status.is_error():
                    print("[PUBLISH: fail]")
                    print("error: %s" % status.error)
                    pass
                else:
                    print("[PUBLISH: sent]")
                    print("timetoken: %s" % envelope.result.timetoken)
                    pass         #delay 0.1s
                
except KeyboardInterrupt:
    ser.close()