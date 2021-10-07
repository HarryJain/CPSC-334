import serial
from pygame import time as pytime
import threading

esp_vals = [2800, 2800, 1000, 1000, 0]

def read_esp():
  global esp_vals
  
  #ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout = 1)
  ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 2)
  ser.flush()

  reps = []
  REP_COUNT = 4

  while True:
    if ser.in_waiting > 0:
      vals = ser.readline().decode('utf-8').rstrip().split(', ')
      vals = [ int(val) for val in vals if val != '' and val.isdigit() ]
      if len(vals) == 5:
        reps.append(vals)
      if len(reps) == REP_COUNT:
        esp_vals = [ int(sum([ reps[j][i] for j in range(REP_COUNT) ]) / REP_COUNT) for i in range(5) ]
        reps = []
        #print(esp_vals)

def main():
  esp_thread = threading.Thread(target = read_esp, name = "esp")
  esp_thread.start()

  clock = pytime.Clock()
  while True:
    clock.tick(60)
    print(esp_vals)

main()