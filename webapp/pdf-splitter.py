import os

import fitz
from pprint import pprint

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_pdf(input_pdf, output_folder):
    # Open the input PDF file
    pdf = fitz.open(input_pdf)

    # Iterate through each page of the PDF
    for page_num in range(len(pdf)):
        # Create a new PDF document for each page
        new_pdf = fitz.open()
        new_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)

        # Save the new PDF as a single-page PDF
        
        num_leading_zeros = 4 - len(str(page_num + 1))        
        output_file = f"{output_folder}/page_{'0'*num_leading_zeros}{page_num + 1}.pdf"
        new_pdf.save(output_file)
        new_pdf.close()

    # Close the input PDF file
    pdf.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_pdf_files(directory):
    pdf_files = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            pdf_files.append(file)
        else:
            if os.path.isdir(f"{directory}/{file}"):
                pdf_files.extend(get_pdf_files(f"{directory}/{file}"))
  
    return pdf_files
  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully!")
    else:
        print(f"Directory '{directory}' already exists.")

   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    SEARCH_DIRT = ".proxy-statements/pdfs/test"
    pdf_files = get_pdf_files(SEARCH_DIRT)

    for pdf_file in pdf_files:
        input_pdf = f"{SEARCH_DIRT}/{pdf_file}"
        output_folder = f"{SEARCH_DIRT}/{pdf_file.split('.')[0]}"
        
        create_directory(output_folder)        
        
        split_pdf(input_pdf, output_folder)

    print("PDFs have been split successfully!")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
   main()
