import fitz
from shapely.geometry import Polygon
from pathlib import Path
from shapely.ops import unary_union
from pprint import pprint

class PDFHighlighter():
	"""
    A class for highlighting phrases within a PDF document.

    This class provides functionality to open a PDF document, search for specific phrases, and highlight them with a
    specified color. It leverages the PyMuPDF (fitz) library for manipulating PDF files.
    """
	def __init__(self, 
					doc_path : Path):
		"""
        Initializes the PDFHighlighter with a path to a PDF document.

        Parameters:
            doc_path (Path): The path to the PDF document to be highlighted.
        """
        
		self.file_path = doc_path
		self.doc = fitz.open(doc_path)
			
	def highlight(self, 
				  phrase: str,
				  colour: tuple) -> None:
		"""
		Searches for and highlights all occurrences of a phrase in the document.

		Parameters:
			phrase (str): The phrase to search for in the document.
			colour (tuple): The color to use for highlighting, specified as an RGB tuple.
		"""

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
		"""	
		Draws a polyline shape on a specified page.

		Parameters:
			page (fitz.Page): The page object where the shape will be drawn.
			points (list): A list of points defining the polyline shape.
			color (tuple): The color to fill the shape, specified as an RGB tuple.
		"""
		shape = page.new_shape()
		
		shape.draw_polyline(points)
		shape.finish(color=(0, 0, 0), fill=color, stroke_opacity=0.15, fill_opacity=0.15)
		shape.commit()
			
	def rect_2_poly(	self, 
						rect: fitz.Rect):
		"""
        Converts a rectangle object to a polygon object.

        Parameters:
            rect (fitz.Rect): The rectangle object to convert.

        Returns:
            Polygon: A polygon object representing the rectangle.
        """
		upperLeft = (rect[0], rect[1])
		upperRight = (rect[2], rect[1])
		lowerRight = (rect[2], rect[3])
		lowerLeft = (rect[0], rect[3])

		return Polygon([upperLeft, upperRight, lowerRight, lowerLeft])

	def save(	self,
				file_path = None) -> None:
 
		"""
        Saves the changes made to the document. If a file path is provided, saves to that path; otherwise, saves
        changes incrementally to the original document.

        Parameters:
            file_path (optional): The path to save the modified document. If not provided, the original document is
            updated.
        """
 
		if not file_path:
			file_path = self.file_path

		self.doc.saveIncr()

# Test code
if __name__ == "__main__":  

	highlighter = PDFHighlighter(Path('AAPL2017.pdf'))
	highlighter.highlight(	phrase="Any matter intended for the Board, or for any individual member of the Board, should be directed to Apple", 
 							colour=(0,1,0))
 
	highlighter.save('highlighted.pdf')