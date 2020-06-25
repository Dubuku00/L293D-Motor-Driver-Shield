"""
** created by mafaa **

shield pin	  Desc		
D3	PWM2B		IC 1 ENB -PIN9
D4	SER CLK		To PYB SPI
D5	PWM0B		IC 2 ENB -PIN9
D6	PWM0A		IC 2 ENB -PIN1
D7	OE		PYB PIN or GND
D8	SER DATA	To PYB SPI
D9	PWM1A		SERVO1
D10	PWM1B		SERVO2
D11	PWM2A		IC 1 ENB -PIN1
D12	RCLK		PYB PIN

"""

import pyb
from pyb import Timer, Pin, delay, ExtInt
from pyb import SPI

global sr

def callback(line):
    global sr
    Ext.disable()	# avoid multiple bounce / trigger
    sr.shift(0)

global Ext
Ext = ExtInt(pyb.Pin('X?'), ExtInt.IRQ_FALLING, Pin.PULL_NONE, callback)
Ext.disable()

class ShiftRegister:
    # SPI - Pin X8/Y8 to SER (D8) and Pin X6/Y6 to SERCLK (D4)
    # RCLK (Latch) connect to D12
    # oe not declare? - connect D7 to GND
    # SERCLR connected to Vcc (no option to change)  

    def __init__(self, spi, rclk, oe = None):
        self.spi = spi 
        self.rclk = rclk

    # create SPI bus and pin objects
        if (spi=='X') or (spi=='SPI1'):
            spi = pyb.SPI('X', pyb.SPI.MASTER, baudrate=300000, polarity=0, phase=0)
        if (spi=='Y') or (spi=='SPI2'):
            spi = pyb.SPI('Y', pyb.SPI.MASTER, baudrate=300000, polarity=0, phase=0)
        self.rclk = pyb.Pin(rclk, pyb.Pin.OUT_PP)	#Pin to connect RCLK (D12)

        if oe:  				#Pin to connect OE (D7)
            self.oe = pyb.Pin(oe, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)	
            self.oe.low()
        self.spiXY = spi

    def shift(self, buf):
        self.spiXY.send(buf)
        self.rclk.value(1)       # latch data to output
        self.rclk.value(0)

class DriveDC:
    def __init__(self, zM, p, pwm = 1000):

        # Configure timer for PWM signal
        Frq=pwm

        if (p=='X1') or (p=='X6'):
            if p=='X1': p=pyb.Pin('X1', pyb.Pin.OUT_PP)
            if p=='X6': p=pyb.Pin('X6', pyb.Pin.OUT_PP)
            tim = Timer(2, freq=Frq)
            chnl = tim.channel(1, Timer.freq, pin=p)
        elif p=='X2':
            p=pyb.Pin('X2', pyb.Pin.OUT_PP)
            tim = Timer(2, freq=Frq)
            chnl = tim.channel(2, Timer.PWM, pin=p)
        elif (p=='X3') or (p=='Y9'):
            if (p=='X3'): p=pyb.Pin('X3', pyb.Pin.OUT_PP)
            if (p=='Y9'): p=pyb.Pin('Y9', pyb.Pin.OUT_PP)
            tim = Timer(2, freq=Frq)
            chnl = tim.channel(3, Timer.PWM, pin=p)	
        elif (p=='X4') or (p=='Y10'):
            if (p=='X4'): p=pyb.Pin('X4', pyb.Pin.OUT_PP)
            if (p=='Y10'): p=pyb.Pin('Y10', pyb.Pin.OUT_PP)
            tim = Timer(2, freq=Frq)
            chnl = tim.channel(4, Timer.PWM, pin=p)
        elif p=='X7':
            p=pyb.Pin('X7', pyb.Pin.OUT_PP)
            tim = Timer(13, freq=Frq)
            chnl = tim.channel(1, Timer.PWM, pin=p)            
        elif p=='X8':
            p=pyb.Pin('X8', pyb.Pin.OUT_PP)
            tim = Timer(14, freq=Frq)
            chnl = tim.channel(1, Timer.PWM, pin=p)            
        elif p=='X9':
            p=pyb.Pin('X9', pyb.Pin.OUT_PP)
            tim = Timer(4, freq=Frq)
            chnl = tim.channel(1, Timer.PWM, pin=p)            
        elif p=='X10':
            p=pyb.Pin('X10', pyb.Pin.OUT_PP)
            tim = Timer(4, freq=Frq)
            chnl = tim.channel(2, Timer.PWM, pin=p)            
        elif p=='Y1':
            p=pyb.Pin('Y1', pyb.Pin.OUT_PP)
            tim = Timer(8, freq=Frq)
            chnl = tim.channel(1, Timer.PWM, pin=p)
        elif p=='Y2':
            p=pyb.Pin('Y2', pyb.Pin.OUT_PP)
            tim = Timer(8, freq=Frq)
            chnl = tim.channel(2, Timer.PWM, pin=p)
        elif p=='Y3':
            p=pyb.Pin('Y3', pyb.Pin.OUT_PP)
            tim = Timer(4, freq=Frq)
            chnl = tim.channel(3, Timer.PWM, pin= p)            
        elif p=='Y4':
            p=pyb.Pin('Y4', pyb.Pin.OUT_PP)
            tim = Timer(4, freq=Frq)
            chnl = tim.channel(4, Timer.PWM, pin= p)            
        elif p=='Y7':
            p=pyb.Pin('Y7', pyb.Pin.OUT_PP)
            tim = Timer(12, freq=Frq)
            chnl = tim.channel(1, Timer.PWM, pin= p)            
        elif p=='Y8':
            p=pyb.Pin('Y8', pyb.Pin.OUT_PP)
            tim = Timer(12, freq=Frq)
            chnl = tim.channel(2, Timer.PWM, pin= p)            

        if  zM =='LMA':
                self.chLMA = chnl 
        elif  zM =='LMB':
                self.chLMB =chnl 
        elif  zM =='RMA':
                self.chRMA = chnl 
        elif  zM =='RMB':
                self.chRMB = chnl 
        else:
                raise ValueError( 'Invalid motor identifier' )

    def setSPI(self, spi, rclk, oe = None):
        # SPI - Pin X8/Y8 to SER and Pin X6/Y6 to SERCLK
        #oe not declare? - connect D7 to GND
        #SERCLR connected to Vcc (no option to change)  
        # 1 for motor channels 1&2 and 2 for channels 3&4

        if spi[1:2] =='X' or spi[1:2] =='Y':
            spi = spi[1:2]		
        if spi!='X' and spi!='Y' and spi!='SPI1' and spi!='SPI2':
                raise ValueError( 'Invalid SPI identifier' )
        self.spi = spi

        global sr
        try:
            sr
            pass
        except:
            sr = ShiftRegister(self.spi, rclk, oe)	
            sr.shift(0)

    def setSpeed(self, zM, speed):	       # Setting motor speed  
        if speed <= 0 or speed > 100:
                raise ValueError( 'Invalid input speed parameter')

            if  zM =='LMA':
                self.chLMA.pulse_width_percent(speed)
            elif  zM =='LMB':
                self.chLMB.pulse_width_percent(speed)
            elif  zM =='RMA':
                self.chRMA.pulse_width_percent(speed)
            elif  zM =='RMB':
                self.chRMB.pulse_width_percent(speed)
		
    def run(self, cmd):
        #FORWARD - run forward (actual direction of rotation will depend on motor wiring)
        #BACKWARD - run backwards (run in opposite direction from FORWARD)
        #RELEASE - zero volt to the motor without 'break'
        # set direction
        if cmd=='FORWARD':
            sr.shift(39)
        elif cmd=='BACKWARD':
            sr.shift(216)
        elif cmd=='RELEASE':
            sr.shift(0)

    def getSpeed(self, zM):
            if  zM =='LMA':
                return  self.chLMA.pulse_width_percent()
            elif  zM =='LMB':
                return  self.chLMB.pulse_width_percent()
            elif  zM =='RMA':
                return  self.chRMA.pulse_width_percent()
            elif  zM =='RMB':
                return  self.chRMB.pulse_width_percent()

class DriveStepper:
    def __init__(self, zM, step, E1, E2): 
        self.step360 = 1
        self.StepDelay = 5
        self.StepUDelay = 5
        self.StepMode=[0]
        self.P_E1 = None
        self.P_E2 = None
        self.P_E3 = None
        self.P_E4 = None
        self.step360 = step		#no. of steps per 360 deg

        # SPI , Stepper identifier - 1 for motor channels 1&2 and 2 for channels 3&4
              # number of steps for 360 revolution, 
              # Enable Pins - STP1-shield pin D3 & D11  STP2-shield pin D5 & D6

        if  zM =='STP1':
            self.P_E1 = pyb.Pin(E1, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
            self.P_E2 = pyb.Pin(E2, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
            self.P_E1.low()
            self.P_E2.low()
        if  zM =='STP2':
            self.P_E3 = pyb.Pin(E1, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
            self.P_E4 = pyb.Pin(E2, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
            self.P_E3.low()
            self.P_E4.low()

    def setSPI(self, spi, rclk, oe = None):
        # SPI - Pin X8/Y8 to SER and Pin X6/Y6 to SERCLK
        #oe not declare? - connect D7 to GND
        # SERCLR connected to Vcc (no option to change)  
        # channels 1&2 for Stepper 1and 2 for channels 3&4 for Stepper 2

        if spi[1:2] =='X' or spi[1:2] =='Y':
            spi = spi[1:2]		
        if spi!='X' and spi!='Y' and spi!='SPI1' and spi!='SPI2':
                raise ValueError( 'Invalid SPI identifier' )
        self.spi = spi

        global sr
        try:
            sr
            pass
        except:
            sr = ShiftRegister(self.spi, rclk, oe)	
            sr.shift(0)

    def StepperSpeed(self, zM, rpm):	       # Setting motor speed  
            #StepPerSec= (rpm /  60) / (step360)
            if  zM =='STP1':
                self.StepDelay= (1 /((rpm / 60) * self.step360))*1000
            elif  zM =='STP2':
                self.StepDelay= (1 /((rpm / 60) * self.step360))*1000  
            self.StepUDelay = self.StepDelay  
            self.StepDelay = int(self.StepDelay)  

    def StepperStep(self, zM, Rot_cou, cmd, SMod, uX = 4):  
        #zM- Direction, Rot_cou- no of rotation required
        #cmd - set rotation direction
        # SMod - Stepping mode

        global Ext

        if zM=='W':
            if self.P_E1: 
                self.P_E1.high()
                self.P_E2.high()
            if self.P_E3: 
                self.P_E3.high()
                self.P_E4.high()
        elif zM=='L':
            if self.P_E1: 
                self.P_E1.low()
                self.P_E2.low()
            if self.P_E3: 
                self.P_E3.high()
                self.P_E4.high()
        elif zM=='R':
            if self.P_E1: 
                self.P_E1.high()
                self.P_E2.high()
            if self.P_E3: 
                self.P_E3.low()
                self.P_E4.low()
        
        if SMod=='SINGLE':
            self.StepMode = [5, 34, 72, 144] 
        elif SMod=='DOUBLE': 
            self.StepMode = [39, 106, 216, 149] 
        elif SMod=='COMBO':
            self.StepMode = [216, 221, 149, 183, 39, 111, 106, 250] 
        elif SMod=='FINE':
            self.StepMode = [216, 221, 144, 149, 183, 5, 39, 111, 34, 106, 250, 72] 
        #pin = pyb.Pin('Y1', pyb.Pin.IN)
        #Ext.enable()
        if cmd=='FORWARD':
            for i in range(Rot_cou): 
                #if Pin('Y1').value() == 0: break
                for j in self.StepMode: 
                    #if Pin('Y1').value() == 0: break
                    sr.shift(j)
                    pyb.delay(self.StepDelay)
        elif cmd=='BACKWARD':
            #StepMode.reverse
            for i in range(Rot_cou): 
                #if Pin('Y1').value() == 0: break
                for j in reversed(self.StepMode): 
                    #if Pin('Y1').value() == 0: break
                    sr.shift(j)
                    pyb.delay(self.StepDelay)
        elif cmd=='RELEASE':
            sr.shift(0)
        #Ext.disable()	

