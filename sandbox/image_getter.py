
from glob import glob
import fitz
import random

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

num_pages_to_generate = 25

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_random_page_images():
    full_pdf_file_list = glob('../Proxy2016Blees/*.pdf')
    random.shuffle(full_pdf_file_list)
    pdf_file_list = full_pdf_file_list[:num_pages_to_generate]
    
    for i,pdf_file in enumerate(pdf_file_list):
        
        fitz_doc = fitz.open(pdf_file)
        
        num_pages_in_pdf = len(fitz_doc)
        selected_page = random.randint(0, num_pages_in_pdf)
        
        img = fitz_doc[selected_page].get_pixmap()
        
        img.save(f'test-image-{i}.png')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():

    pdf_file_path = './EMN 2020-1.pdf'

    fitz_doc = fitz.open(pdf_file_path)
    
    for i, page in enumerate(fitz_doc):
        
        img = page.get_pixmap()
        
        img.save(f'./page_images/test-image-{i}.png')
        
        
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()