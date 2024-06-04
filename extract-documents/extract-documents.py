import os

from glob import glob

from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROXY_STATEMENTS_PATH = '/home/nicholishiell/Documents/WorkProjects/Profs/LeanneKeddie/docs/Proxy_2017/'

def get_proxy_statement_name(proxy_statement_path : str) -> str:
    return os.path.basename(proxy_statement_path).split('.')[0].replace(' ','_')


def main():

    proxy_statement_pdfs = glob(PROXY_STATEMENTS_PATH+'*.pdf')

    print(f'# of Proxy Statements: {len(proxy_statement_pdfs) }')

    doc_gen = ExtractedDocumentGenerator()

    for pdf_file_path in proxy_statement_pdfs:
        proxy_statement = get_proxy_statement_name(pdf_file_path)

        extracted_doc = doc_gen.extract_from_path(  pdf_file_path=pdf_file_path,
                                                    include_pages=[],
                                                    output_name=None)

        extracted_doc.save_as_json(proxy_statement+'.json')  
        
        print(f'The file {pdf_file_path} has {extracted_doc.num_pages} pages in it')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()