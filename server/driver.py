import _this_is_mine
import light_detect

# total number of stops
STOP_COUNT = 2

while True:
  # continue to prompt until correct stop number has been entered
  while True:
    stopNumber = input( "Enter stop number : #" )
    
    if stopNumber > 0 and stopNumber < STOP_COUNT:
      break
    else:
      print "Invalid stop number, please try again..."
  
  # wait until cups have been placed
  light_detect.setup()

  # drive to stop
  _this_is_mine.drive( stopNumber )

  # wait until cups have been picked up
  light_detect.dropoff()

  # return home
  _this_is_mine.drive( STOP_COUNT - stopNumber )

  # message
  print "Arrived back home!!"
  
