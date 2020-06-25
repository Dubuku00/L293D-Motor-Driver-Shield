"""
To test DC motors in Motorshield channel 1 and Steper motor in channel 2

"""

import pyb
from pyb import Pin, delay
from PYB_L239D import DriveDC
from PYB_L239D import DriveStepper

#DC motor initialize
LMA = DriveDC("LMA", 'X1')
#M2 = DriveDC("LMB", 'X2')

#Stepper initialize
STP2 = DriveStepper("STP2", 100, 'X3', 'X4')

#SPI initialize
STP2.setSPI('Y', 'Y1')  # SPI init - one time
print('sr called')	

LMA.setSpeed('LMA', 100)	
print('speed called')
LMA.run('FORWARD')
#M2.run('FORWARD')
delay(2000)
LMA.run('RELEASE')

STP2.StepperSpeed("STP2", 200)
STP2.StepperStep( "W", 50, "FORWARD", "DOUBLE")	
print('back to main')	
delay(2000)
STP2.StepperSpeed("STP2", 240)
STP2.StepperStep( "W", 100, "BACKWARD", "COMBO")	
STP2.StepperStep( "R", 100, "RELEASE", "COMBO")	
print('back to main again')	
