import serial

def main():
	if __name__ == '__main__':
    		ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=1)
    		ser.flush()

	while True:
        	if ser.in_waiting > 0:
            		line = ser.readline().decode('utf-8').rstrip()
            		print(line)	

if __name__ == "__main__":
	main()
