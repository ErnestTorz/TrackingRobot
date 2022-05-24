import math
class object:

    def __init__(self,imW,imH,xcenter,ycenter,xmin,xmax,ymin,ymax ):   
        self.imW=imW
        self.imH=imH
        self.xcenter=xcenter
        self.ycenter=ycenter
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
    
    def distance (self,object2:object):
        return math.sqrt(((object2.xcenter-self.xcenter)**2)+((object2.ycenter-self.ycenter)**2))