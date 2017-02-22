class sideOfPieces:
    def __init__(self,right,left):
        self.cornerRight=right
        self.cornerLeft=left
        self.originalPoints=[]
        self.x_axis_Points=[]
        self.isStraight = False
        self.isConvex = False
        self.isConcave = False
    