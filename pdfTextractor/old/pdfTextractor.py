
from ProcessedDocument import ProcessedDocument

from glob import glob
import fitz
import layoutparser as lp
import cv2
import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INPUT_FILE_PATH = 'EMN 2020-1.pdf'

EXTRACT_TEXT_OUTPUT_PATH_BASE = './extractedText/'

SEPARATORS = ['.',';','l','þ', '¨', '•', 'Ø', '*']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_document_layout_analysis():
    fitz_doc = fitz.open(INPUT_FILE_PATH)
    
    model = lp.models.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config', 
                                            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                            label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})
    
    
    for i, page in enumerate(fitz_doc): 
        
        
        pix = page.get_pixmap(dpi=300)  
        
        # input_file_name = f'./input_images/input_image_page_{i}.jpg'
        # pix.save(input_file_name)
        
        raw_bytes = pix.tobytes()
        input_image = cv2.imdecode(np.frombuffer(bytearray(raw_bytes), dtype=np.uint8), cv2.IMREAD_COLOR)      
        
        input_image = input_image[..., ::-1] 
        
        layout = model.detect(input_image)
        output_image = lp.draw_box(input_image, layout, box_width=3)
        
        output_file_name = f'./output_images/output_image_page_{i}.jpg'
        print(output_file_name)
        output_image.save(output_file_name)  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def generate_output_file_path(input_file_path : str) -> str:
    input_file_name = input_file_path.split('/')[-1]
    
    output_file_name = input_file_name.split('.')[0]+'.txt'
    
    return EXTRACT_TEXT_OUTPUT_PATH_BASE+output_file_name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_extract_text_to_file(input_file_path : str):
    
    fitz_doc = fitz.open(input_file_path)
    
    output_file_path = generate_output_file_path(input_file_path)
    
    output_file = open(output_file_path, 'w+',encoding='UTF-8')
    
    for page_num , page in enumerate(fitz_doc):
        page_text = page.get_textpage().extractText(sort=True)
        output_file.write(page_text+'\n')
        
    output_file.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    # file_list = glob('../Proxy2016Subset/*.pdf')
    file_list = glob('../virusPDFs/*.pdf')
    
    for file in file_list:
        run_extract_text_to_file(file)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()