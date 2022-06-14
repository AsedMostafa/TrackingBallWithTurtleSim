import cv2

class ballDetector:
    def __init__(self):
        pass

    def toBinary(self,frame,lower,upper):
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        binary=cv2.inRange(hsv,lower,upper)
        return binary

    def enhanceBinary(self,binary_image,iterations_erode,iterations_dilate):
        ero = cv2.erode(binary_image,None,iterations=iterations_erode)
        dial = cv2.dilate(ero,None,iterations=iterations_dilate)
        return dial

    def getBallCoordinate(self,image_binary,image_color):
        contours, notUsable = cv2.findContours(image_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            center = (320,240)
            r = 5
            return(image_color,center,r)

        else:
            for contour in contours:
                (x,y),r = cv2.minEnclosingCircle(contour)
                r = int(r)
                center = (int(x),int(y))
                cv2.circle(image_color,center,r,(0,255,0),2)
                cv2.circle(image_color,center,3,(255,0,0),3)
                return(image_color,center,r)

