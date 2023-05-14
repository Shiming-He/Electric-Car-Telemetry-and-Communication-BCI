# Electric-Car-Telemetry-and-Communication-BCI
This is the new Bluevale Collegiate Institutes Electric Car Telemetry and Communication system. It borrows many important elements of the previous year's system, with a completely new design. It utilizes a Cycle Analyst to provide information about the cars present performance. Also it uses a Raspberry Pi to compute, transmite, and receive information about the performance. Moreover it uses a phone as the display for the driver, and as a hotspot for the Raspberry Pi. Furthermore, a computer is recommended to run the website to observe the information. Lastly, the system uses PubNub to communicate between the Raspberry Pi and the Computer.
# Contributors
Shiming He, and the 2023 Data Management Team
# Special Thank You
A special thanks to the 2022 Data Management Team, especially Austin Wang, and Steven Cao for their work on the original Telemetry System.
# Features
This system features:
- Real-time communication between Raspberry Pi and the Computer
- Allow for commands to speed signals to be sent to the driver remotely
- Real-time computation and basic analyst of the batter performance
- 3 modes for which the speed signals may be sent
- Allow the driver to easily gain situation awareness about the battery
# Installation
Install the Phone to a position on the car that is easy for the driver to see.
Install the Raspberry Pi onto the car in a position that is well protected, and place a power source (Recommending a battery bank) in a secure position nearby, and connect the two together.
Install the Cycle Analyst in a Safe Position.
Create a 5.6k ohms and 8.2k ohms resistor piece as shown in the diagram below. Connect the ground wire to GPIO pin 9 on the Raspberry Pi, and the Rx cable to GPIO pin 10. 
Connect the Cycle Analyst to the Control of your Electric Car
Connect the phone and raspberry pi with an HDMI cable and a Capture Card, as well as adaptors to connect with the phone and raspberry pi.
Install the Computer folder onto your computer. Then open the jsv1.0.0.js file and add your PubNub publish and subscribe channel. 
Install the Raspberry Pi folder onto the Raspberry Pi. Then open the ______.py file and add your PubNub publish and subscribe channel. 
# How to Use the System
Work in Progress
