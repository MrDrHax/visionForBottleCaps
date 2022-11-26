import cv2

class color:
    r: int
    g: int
    b: int

    '''
    Function to define a color used by opencv. 

    Takes in the color values in RGB
    '''
    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b

    '''
    Returns an array ready to use for opencv, with color values being (b,g,r)

    (because opencv takes color values that way)
    '''
    def array(self):
        return (self.b,self.g,self.r) # los colores en opencv estan invertidos

class ImageRec:
    '''
    Class that filters a cam and return positions of caps
    '''
    def __init__(self, minX, maxX, minY, maxY, minCapSize) -> None:
        self.minX = minX
        self.maxX = maxX
        self.maxY = maxY
        self.minY = minY
        
        self.minThresholdSize = minCapSize

        # get the first cam avaible to make the capture 
        self.cap = cv2.VideoCapture(0)

    '''
    Apply the necesary filers to get all the contours of caps on a conveyor belt
    '''
    def applyFilters(self, whiteMin: color, whiteMax: color, transparentMin: color, transparentMax: color, redMin: color, redMax: color) -> None:
        # afrian falta agregar aqui la camara!!!

        # obtain image to proses
        ret, self.img = self.cap.read()

        # crop image to not waste resources
        self.img = self.img[self.minY:self.maxY,self.minX:self.maxY]

        # show original
        cv2.imshow("Cropped original", self.img)

        # Filter images by their min/max RGB values 
        self.redFiltered = cv2.inRange(self.img, redMin.array(), redMax.array())
        self.white = cv2.inRange(self.img, whiteMin.array(), whiteMax.array())
        self.transparent = cv2.inRange(self.img, transparentMin.array(), transparentMax.array())

        cv2.imshow("Filtered red", self.redFiltered)
        cv2.imshow("Filtered white", self.white)
        cv2.imshow("Filtered trans", self.transparent)


        # Get the image contours
        self.redContours, self.redHierarchy = cv2.findContours(self.redFiltered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.whiteContours, self.whiteHierarchy = cv2.findContours(self.white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.transContours, self.transHierarchy = cv2.findContours(self.transparent, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # filter by min size 
        self.redFilteredContours = [i for i in self.redContours if cv2.contourArea(i) > self.minThresholdSize]
        self.whiteFilteredContours = [i for i in self.whiteContours if cv2.contourArea(i) > self.minThresholdSize]
        self.transFilteredContours = [i for i in self.transContours if cv2.contourArea(i) > self.minThresholdSize]

        # Draw and show for debug purposes
        cv2.drawContours(self.img, self.redFilteredContours, -1, (0, 255, 255), 1)
        cv2.drawContours(self.img, self.whiteFilteredContours, -1, (255, 0, 0), 1)
        cv2.drawContours(self.img, self.transFilteredContours, -1, (0, 255, 0), 1)

        cv2.imshow("Contours found", self.img)

    '''
    Test if a red cap is in a position range to activate a servo
    '''
    def isRedInPos(self,startPos,endPos):
        for contour in self.redFilteredContours:
            x,y,w,h = cv2.boundingRect(contour)
            if startPos < x < endPos:
                return True
        return False
    
    '''
    Test if a white cap is in a position range to activate a servo
    '''
    def isWhiteInPos(self,startPos,endPos):
        for contour in self.whiteFilteredContours:
            x,y,w,h = cv2.boundingRect(contour)
            if startPos < x < endPos:
                return True
        return False

    '''
    Test if a transparent cap is in a position range to activate a servo
    '''
    def isTransInPos(self,startPos,endPos):
        for contour in self.transFilteredContours:
            x,y,w,h = cv2.boundingRect(contour)
            if startPos < x < endPos:
                return True
        return False

# This will not run on final production. This is for local testing
if __name__ == "__main__":
    thingy = ImageRec(0,1400, 400, 500, 600)

    redMin = color(200,0,0)
    redMax = color(255,100,100)
    
    whiteMin = color(200,200,200)
    whiteMax = color(255,255,255)
    
    transparentMin = color(100,100,100)
    transparentMax = color(200,200,200)

    while True:
        thingy.applyFilters(whiteMin, whiteMax, transparentMin, transparentMax, redMin, redMax)

        thingy.isRedInPos(500,800)

        if cv2.waitKey(50) == 13 :      # Specifying (Enter) button to break the loop
            break
