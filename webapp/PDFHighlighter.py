import fitz
from shapely.geometry import Polygon
from pathlib import Path
from shapely.ops import unary_union
from pprint import pprint

class PDFHighlighter():
	
	def __init__(	self, 
					doc: Path, 
					page: int):
	 
		self.doc = fitz.open(doc)
		self.PAGE = self.doc[page - 1]

	def highlight(	self, 
					phrase : str,
     				colour : tuple) -> None:

		for rect in self.PAGE.search_for(phrase):	
			polygons = self.rect_2_poly(rect)
   
			rects_merged = unary_union(polygons)
			points = list(rects_merged.exterior.coords)
			self.draw_shape(points, colour)
   

	def save(	self,
				file_path : str) -> None:
 
		self.doc.save(	Path(file_path), 
                		garbage=1, 
                  		deflate=True, 
                    	clean=True)

	def draw_shape(	self, 
					points : list,
               		color: tuple):
		shape = self.PAGE.new_shape()
		
		shape.draw_polyline(points)
		shape.finish(color=(0, 0, 0), fill=color, stroke_opacity=0.15, fill_opacity=0.15)
		shape.commit()
		
   
	def get_text_rects(self):

		rects = self.PAGE.search_for(self.content)
  
		polygons = [self.rect_2_poly(r) for r in rects] 

		rectsMerged = unary_union(polygons) 

		self.points = list(rectsMerged.exterior.coords)
		
	def rect_2_poly(	self, 
						rect: fitz.Rect):

		upperLeft = (rect[0], rect[1])
		upperRight = (rect[2], rect[1])
		lowerRight = (rect[2], rect[3])
		lowerLeft = (rect[0], rect[3])

		return Polygon([upperLeft, upperRight, lowerRight, lowerLeft])

if __name__ == "__main__":  

	# highlighter = PDFHighlighter(Path("test_printed.pdf"), page = 1)
	# highlighter.highlight(	phrase = 'these two branches are related to each',
    #                  		colour=(1,0,0))
 
	# highlighter.highlight(phrase='They make use of the fundamental notions of convergence of infinite sequences and infinite series to a welldefined limit',
    #                     	colour=(0,1,0))
 
	# highlighter.highlight(phrase='the calculus of infinitesimals',
    #                      	colour=(0,0,1))
 
	highlighter = PDFHighlighter(Path(".proxy-statements/AAPL2017.pdf"), page = 6)
	highlighter.highlight('Compensation and Performance Highlights', (0,1,0))
 
	# highlighter = PDFHighlighter(Path("AMAT_ 2017_one_page.pdf"), page = 1)
	# highlighter.highlight('we achieved record performance', (0,1,0))
 
	highlighter.save('highlighted.pdf')