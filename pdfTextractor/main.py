
from glob import glob
import fitz
import random
from pprint import pprint

from BoundingBox import BoundingBox

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LABEL_DICT = {  '0':  'Caption',
                '1':  'Footnote',
                '2':  'Formula',
                '3':  'List-item',
                '4':  'Page-footer',
                '5':  'Page-header',
                '6':  'Picture',
                '7':  'Section-header',
                '8':  'Table',
                '9':  'Text',
                '10': 'Title'}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    pdf_file_path = './EMN 2020-1.pdf'
    labels_files = sorted(glob('labels/*.txt'))

    fitz_doc = fitz.open(pdf_file_path)
    
    print(f'# of labels file: {len(labels_files)}')
    print(f'# of pages in pdf: {len(fitz_doc)}')
    
    for i, page in enumerate(fitz_doc):
        
        # get the page dimensions
        rect = page.rect 
        print(f'page dimensions (w,h): {rect.x1, rect.y1}')
        page_width = rect.x1
        page_height = rect.y1
        
        # get the labelled bounding boxes
        label_file = open(labels_files[i],'r',encoding='utf-8')
        lines = label_file.readlines()

        print(labels_files[i])
        
        for line in lines:
            (label_key,x0,y0,w,h) = line.split(' ')
            x_c = float(x0)
            y_c = float(y0)
            half_w = float(w)
            half_h = float(h)
            label = LABEL_DICT[label_key]
                            
            bb_x0 = page_width*(x_c-half_w)
            bb_x1 = page_width*(x_c+half_w)
            
            bb_y0 = page_height*(y_c-half_h)
            bb_y1 = page_height*(y_c+half_h)        
               
            bb_rect = fitz.Rect(bb_x0,bb_y0,bb_x1,bb_y1)

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(bb_rect)
            print(label,page.get_textbox(bb_rect))
            
        input('========================================================')        
                    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()
    