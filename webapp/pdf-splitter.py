import os

import fitz
from pprint import pprint

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_pdf(input_pdf, output_folder):
    """
    Splits a PDF file into individual pages, saving each page as a separate PDF file.

    Parameters:
    - input_pdf (str): The path to the input PDF file to be split.
    - output_folder (str): The directory where the output single-page PDF files will be saved.

    Each output file is named using a pattern that includes a page number with leading zeros for consistency,
    e.g., "page_0001.pdf" for the first page.

    No return value.
    """
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
    """
    Recursively searches for and returns a list of all PDF files within a given directory and its subdirectories.

    This function iterates over all items in the specified directory. If an item is a PDF file (determined by the
    file extension), it is added to the list of PDF files. If an item is a directory, the function recursively searches
    that directory for PDF files as well. This process continues until all directories have been searched and all PDF
    files have been identified.

    Parameters:
        directory (str): The path to the directory where the search for PDF files should begin.

    Returns:
        List[str]: A list of paths (as strings) to all the PDF files found within the specified directory and its
        subdirectories. The paths are relative to the initial directory specified.

    Example:
        >>> get_pdf_files('/path/to/directory')
        ['file1.pdf', 'subdir/file2.pdf', ...]

    Note:
        This function does not return the full path to the PDF files, but rather the relative path from the initial
        directory specified.
    """
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
    """
    Creates a directory at the specified path if it does not already exist.

    This function checks if a directory exists at the given path. If the directory does not exist, it creates the
    directory along with any necessary parent directories. If the directory already exists, it simply prints a message
    indicating that the directory already exists.

    Parameters:
        directory (str): The path of the directory to be created.

    Returns:
        None

    Side Effects:
        - If the directory does not exist, it is created on the filesystem.
        - Prints a message to the standard output indicating whether the directory was created or if it already existed.

    Example:
        >>> create_directory('/path/to/new/directory')
        Directory '/path/to/new/directory' created successfully!

        >>> create_directory('/path/to/existing/directory')
        Directory '/path/to/existing/directory' already exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully!")
    else:
        print(f"Directory '{directory}' already exists.")

   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """
    Splits all PDF files found in a specified directory into individual pages.

    This function searches for PDF files within a predefined directory (and its subdirectories) for the year 2019,
    creates a separate directory for each PDF file, and then splits each PDF file into individual pages, saving them
    to the corresponding directory.

    The process involves the following steps:
    1. Define the search directory relative to the current working directory.
    2. Use the `get_pdf_files` function to recursively find all PDF files in the search directory.
    3. For each PDF file found:
       a. Construct the full path to the input PDF file.
       b. Generate an output folder name based on the PDF file name (excluding the '.pdf' extension) and create this
          folder within the search directory.
       c. Call the `split_pdf` function to split the PDF into individual pages, saving each page as a separate PDF
          file within the output folder.
    4. Print a message indicating the successful completion of the PDF splitting process.

    Note:
    - The `create_directory` function is used to ensure the output folder exists before splitting the PDF.
    - The `split_pdf` function must be defined elsewhere and is responsible for the actual splitting of the PDF files.
    """
    SEARCH_DIRT = ".proxy-statements/pdfs/2019"
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
