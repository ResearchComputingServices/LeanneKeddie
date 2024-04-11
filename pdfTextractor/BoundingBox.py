from fitz import Rect

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BoundingBox:
    """This function represents a bounding box for a document object detected by Yolov5
    """
    
    def __init__(self,
                 bb_x0 : float,
                 bb_y0 : float,
                 bb_x1 : float,
                 bb_y1 : float,
                 label : str,
                 conf : float):
    
        self.x0 = int(bb_x0)
        self.y0 = int(bb_y0)
        self.x1 = int(bb_x1)
        self.y1 = int(bb_y1)
     
        self.label = label
        
        self.confidence = float(conf)
     
        self._check()
    
    def __str__(self):
        return f'({self.x0}, {self.y0}) - ({self.x1}, {self.y1}) conf: {self.confidence} label: {self.label}'
    
    def __lt__(self, other):
        
        is_less_than_other = False
        
        if self.y0 < other.y0:
            is_less_than_other = True
        elif self.y0 == other.y0 and self.x0 < other.x0:
            is_less_than_other = True    
        
        return is_less_than_other
    
    def _check(self) -> None:
        """ensure that the point (x0,y0) is closer to the top left corner than the point (x1,y1)
        """
        self.x0, self.x1 = self._swap(self.x0, self.x1)
        self.y0, self.y1 = self._swap(self.y0, self.y1)
    
    def _swap(self, a : float, b : float) -> tuple:
        """Returns the arguments in ascending order. Helper function used by self._check

        Args:
            a (float): value 1
            b (float): value 2

        Returns:
            tuple: lower value, higher value
        """
        if b < a:
            tmp = a
            a = b
            b = tmp
        return a,b
    
    def get_definition(self) -> tuple:
        """returns values which define the extents of the bounding box

        Returns:
            tuple: self.x0, self.y0,self.x1,self.y1
        """
        return self.x0, self.y0,self.x1,self.y1
    
    def get_rect(self) -> Rect:
        return Rect(self.x0, self.y0,self.x1,self.y1)
          
    def overlaps(self, bb) -> bool:
        """Returns true if the bounding box bb overlaps the calling bounding box

        Args:
            bb (_type_): _description_

        Returns:
            bool: _description_
        """
        
        return  (self._range_overlap(self.x0, self.x1, bb.x0, bb.x1) and 
                 self._range_overlap(self.y0, self.y1, bb.y0, bb.y1))
    
    def _range_overlap(self,
                       a_min : float,
                       a_max : float,
                       b_min : float,
                       b_max : float) -> bool:
        """This function checks if the ranges defined by [a_min, a_max]
        and [b_min, b_max] overlap. Helper function for self.overlaps

        Args:
            a_min (float): lower value of range 1
            a_max (float): upper value of range 1
            b_min (float): lower value of range 2
            b_max (float): upper value of range 2

        Returns:
            bool: returns true if the ranges overlap
        """
        return (a_min <= b_max) and (b_min <= a_max)
          
    
    def contains(self, bb) -> bool:
        """checks if bb is completely contained with in the calling bounding box.

        Args:
            bb (BoudningBox): test bounding box

        Returns:
            bool: returns true if passed bounding box is contained
        """
        
        return  (bb.x0 >= self.x0 and bb.x0 <= self.x1 and
                 bb.x1 >= self.x0 and bb.x1 <= self.x1 and
                 bb.y0 >= self.y0 and bb.y0 <= self.y1 and
                 bb.y1 >= self.y0 and bb.y1 <= self.y1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    bb1 = BoundingBox(1,1,10,2,'test',0.)
    bb2 = BoundingBox(5,0,6,10,'test',0.)
    bb3 = BoundingBox(5,1,6,2,'test',0)
    
    if bb1.contains(bb2):
        print('bb1 contains bb2')
    else:
        print('bb2 NOT inside bb1')
    
    if bb1.overlaps(bb2):
        print('bb1 overlaps bb2')
    else:
        print('bb1 does not overlap bb2')

    if bb1.contains(bb3):
        print('bb1 contains bb3')
    else:
        print('bb1 does Not contain bb3')
        
    if bb1.overlaps(bb3):
        print('bb1 overlaps bb3')
    else:
        print('bb1 does not overlap bb3')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()