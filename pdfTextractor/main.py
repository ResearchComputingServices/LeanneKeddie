
from glob import glob
import fitz
import random
from pprint import pprint

from BoundingBoxGenerator import BoundingBoxGenerator as BBGen
from ExtractedDocument import ExtractedDocument, DocumentPage

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

def clean_text(original_text : str) -> str:
    cleaned_text = ''
    
    for char in original_text:
        # replace new line with space
        if ord(char) == 10:
            char = ' '
        
        # only add printable ascii characters
        if ord(char) > 31 and ord(char) < 127:
            cleaned_text += char

    return cleaned_text.strip()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    pdf_file_path = './EMN 2020-1.pdf'
    labels_files = sorted(glob('./data/exp9/labels/*.txt'))
    
    fitz_document = fitz.open(pdf_file_path)
    
    extracted_document = ExtractedDocument()
    extracted_document.file_path=pdf_file_path
    
    for i,fitz_page in enumerate(fitz_document):
        bb_generator = BBGen(fitz_page.rect.x1, 
                             fitz_page.rect.y1, 
                             LABEL_DICT)
        
        bb_list = bb_generator.get_bounding_boxes_from_file(labels_files[i])
            
        extracted_page = DocumentPage(i)
                
        for bb in bb_list:
            
            text = ''
            
            if bb.label == 'Table':
                text = fitz_page.find_table(bb.get_rect())
            else:
                text = clean_text(fitz_page.get_textbox(bb.get_rect()))
            
            extracted_page.add_text_block(text=text,
                                          conf=bb.confidence,
                                          label=bb.label)
           
        extracted_document.add_page(extracted_page)         

        print(extracted_page.get_text())
        input()
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()
    