import logging
import argparse
import fitz

from yolov5.detect import run

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_object_detection():
    weights = './weights/best.pt'   # fine tuned weights
    source = './page_images/'       #
    imgsz = (792,612)
    line_thick = 1
    nosave=False
    save_dir_path = './output/'
    
    run(weights=weights,
        source=source,
        imgsz=imgsz,
        line_thickness=line_thick,
        save_txt=True,
        save_conf=True)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
def extract_command_line_args() -> dict:
    """generates the parser and applies it to the command line args

    Returns:
        dict: a dictionary containing the command line args.
    """
    
    parser = argparse.ArgumentParser(prog='DocLayNet',
                                     description='This program uses a fined-tuned version of Yolov5 to perform document layout analysis')

    # parser.add_argument('--'+CL_ARG_PDF_FLAG,
    #                     default=CL_ARG_PDF_DEFUALT,
    #                     help = CL_ARG_PDF_HELP)

    # parser.add_argument('--'+CL_ARG_OUT_FLAG,
    #                     default=CL_ARG_OUT_DEFUALT,
    #                     help=CL_ARG_OUT_HELP)

    # parser.add_argument('--'+CL_ARG_LABELS_FLAG,
    #                     default=CL_ARG_LABELS_DEFUALT,
    #                    help=CL_ARG_LABELS_HELP)

    args = parser.parse_args()

    return vars(args)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pdf_get_page_images(pdf_file_path : str) -> None:

    fitz_doc = fitz.open(pdf_file_path)
    
    for i, page in enumerate(fitz_doc):
        
        img = page.get_pixmap()
        
        img.save(f'./page_images/page-image-{i}.png')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    args_dict = extract_command_line_args()
    
    logging.basicConfig(filename='pdf_textractor.log', 
                        encoding='utf-8', 
                        level=logging.DEBUG)
    
    run(args_dict)    
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()