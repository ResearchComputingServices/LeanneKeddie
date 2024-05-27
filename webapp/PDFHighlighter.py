import fitz
from shapely.geometry import Polygon
from pathlib import Path
from shapely.ops import unary_union
from pprint import pprint

class PDFHighlighter():
	
	def __init__(	self, 
					doc_path : Path):
    
		self.file_path = doc_path
		self.doc = fitz.open(doc_path)
		
	def highlight(	self, 
					phrase : str,
     				colour : tuple) -> None:

		for page in self.doc:
			for rect in page.search_for(phrase):	
				polygons = self.rect_2_poly(rect)
	
				rects_merged = unary_union(polygons)
				points = list(rects_merged.exterior.coords)
				self.draw_shape(page, points, colour)
   
	def draw_shape(	self, 
					page : fitz.Page,
					points : list,
               		color: tuple):
		shape = page.new_shape()
		
		shape.draw_polyline(points)
		shape.finish(color=(0, 0, 0), fill=color, stroke_opacity=0.15, fill_opacity=0.15)
		shape.commit()
			
	def rect_2_poly(	self, 
						rect: fitz.Rect):

		upperLeft = (rect[0], rect[1])
		upperRight = (rect[2], rect[1])
		lowerRight = (rect[2], rect[3])
		lowerLeft = (rect[0], rect[3])

		return Polygon([upperLeft, upperRight, lowerRight, lowerLeft])

	def save(	self,
				file_path = None) -> None:
 
		if not file_path:
			file_path = self.file_path

		self.doc.saveIncr()
 
		# self.doc.save(	Path(file_path), 
        #         		garbage=1, 
        #           		deflate=True, 
        #             	clean=True)

if __name__ == "__main__":  

	# highlighter = PDFHighlighter(Path("test.pdf"))
	# highlighter.highlight(	phrase = 'these two branches are related to each',
    #                  		colour=(1,0,0))
 
	# highlighter.highlight(phrase='They make use of the fundamental notions of convergence of infinite sequences and infinite series to a welldefined limit',
    #                     	colour=(0,1,0))
 
	# highlighter.highlight(phrase='the calculus of infinitesimals',
    #                      	colour=(0,0,1))
 
	highlighter = PDFHighlighter(Path('AAPL2017.pdf'))
	highlighter.highlight(	phrase="Any matter intended for the Board, or for any individual member of the Board, should be directed to Apple", 
 							colour=(0,1,0))
 
	# highlighter = PDFHighlighter(Path("AMAT_ 2017_one_page.pdf"))
	# highlighter.highlight('we achieved record performance', (0,1,0))
 
	highlighter.save('highlighted.pdf')