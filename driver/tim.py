import driver
import detector
import socket
import sys
 
HOST = '192.168.1.80'
PORT = 12345
STOP_COUNT = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
try:
    s.bind((HOST, PORT))
except socket.error as err:
    sys.exit()
 
s.listen(10)
# total number of stops

while True:
  # continue to prompt until correct stop number has been entered
  while True:
    conn, addr = s.accept()
    buffer = conn.recv(64)
    stopNumber = int( buffer )
    conn.close()
    
    if stopNumber > 0 and stopNumber < STOP_COUNT:
      break
    else:
      print "Invalid stop number, please try again..."
  
  # wait until cups have been placed
  detector.setup()

  # drive to stop
  driver.drive( stopNumber )

  # wait until cups have been picked up
  detector.dropoff()

  # return home
  driver.drive( STOP_COUNT - stopNumber )

  # message
  print "Arrived back home!!"
  
