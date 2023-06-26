import board
import digitalio
import time

readvalue = 4000

chip_s = digitalio.DigitalInOut(board.C0)
chip_s.direction = digitalio.Direction.OUTPUT

D_out = digitalio.DigitalInOut(board.C2)
D_out.direction = digitalio.Direction.OUTPUT

Clock = digitalio.DigitalInOut(board.C3)
Clock.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.C1)
button.direction = digitalio.Direction.INPUT

chip_s.value = True
D_out.value = False
Clock.value = False

def read_adc_val(channel):

  adcvalue = 0
  commandbits = 0b11000000

  commandbits|=((channel)<<3)

  chip_s.value = False

  for i in range(7, 2, -1):
    if (commandbits & (1 << i)) == 0: 
        D_out.value = False
        
    else:
        D_out.value = True
    Clock.value = True
    Clock.value = False
        
  Clock.value = True
  Clock.value = False
  Clock.value = True
  Clock.value = False
  
  

  for i in range(11, -1, -1):
    if button.value == True:
       adcvalue+= 1<<i
    else:
       adcvalue+= 0<<i
	
    
    Clock.value = True
    Clock.value = False

  chip_s.value = True
  return adcvalue


while True:

 readvalue = read_adc_val(5)
 time.sleep(5)
 print(readvalue)


