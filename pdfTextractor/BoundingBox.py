
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BoundingBox:
    
    def __init__(self,
                 bb_x0 : float,
                 bb_y0 : float,
                 bb_x1 : float,
                 bb_y1 : float,
                 conf : float):
        self.x0 = bb_x0
        self.y0 = bb_y0
        self.x1 = bb_x1
        self.y1 = bb_y1
        
        self.confidence = conf
     
        self._check()
            
    def _check(self) -> None:
        self.x0, self.x1 = self._swap(self.x0, self.x1)
        self.y0, self.y1 = self._swap(self.y0, self.y1)
    
    def _swap(self, a : float, b : float) -> tuple:
        if b < a:
            tmp = a
            a = b
            b = tmp
        return a,b
           
    def overlaps(self, bb) -> bool:
        
        return  (self._range_overlap(self.x0, self.x1, bb.x0, bb.x1) and 
                 self._range_overlap(self.y0, self.y1, bb.y0, bb.y1))
    
    def _range_overlap(self,
                       a_min : float,
                       a_max : float,
                       b_min : float,
                       b_max : float) -> bool:
        return (a_min <= b_max) and (b_min <= a_max)
          
    
    def contains(self, bb) -> bool:
        
        return  (bb.x0 > self.x0 
                and bb.x1 < self.x1
                and bb.y0 > self.y0
                and bb.y1 < self.y1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    bb1 = BoundingBox(1,1,10,2,0.)
    bb2 = BoundingBox(5,0,6,10,0.)
    
    if bb1.contains(bb2):
        print('bb2 inside bb1')
        
    if bb1.overlaps(bb2):
        print('bb1 overlaps')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()