from .src import openCVModule
import cv2

# first make a new vision instance 
thingy = openCVModule.ImageRec(0,1400, 400, 500, 600)

# define colors min and max for red, white and transparent
redMin = openCVModule.color(200,0,0)
redMax = openCVModule.color(255,100,100)

whiteMin = openCVModule.color(200,200,200)
whiteMax = openCVModule.color(255,255,255)

transparentMin = openCVModule.color(100,100,100)
transparentMax = openCVModule.color(200,200,200)

# run until the enter key is pressed
while True:
    # apply filters
    thingy.applyFilters(whiteMin, whiteMax, transparentMin, transparentMax, redMin, redMax)

    # test if something is in range of a servo
    if thingy.isRedInPos(500,800):
        # do something
        pass

    if cv2.waitKey(50) == 13 :      # Specifying (Enter) button to break the loop
        break
