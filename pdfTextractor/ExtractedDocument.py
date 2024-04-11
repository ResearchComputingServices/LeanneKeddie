from dataclasses import dataclass, field
from typing import List

from pprint import pprint

import pysbd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class DocumentTextBlock:
    """
    Text_block extracted from pdf using yolov5 bounding box and fitz
    """

    def __init__(self,
                 text : str,
                 conf = 0.,
                 label = 'UNKNOWN'):
          
        self.sentences = self._split_sentences(text)
        self.conf = float(conf)
        self.label = label

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return f'conf: {self.conf} label: {self.label}\n' + self.text
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @property
    def text(self) -> str:
        return ('\n'.join(self.sentences)).strip()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _split_sentences(self,
                         text) -> None:
        seg = pysbd.Segmenter(language='en', clean=False)
        return seg.segment(text)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@dataclass
class DocumentPage:
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, 
                 page_num : int):
        
        self.page_number = page_num
        
        self.document_text_blocks = []
    
     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __iter__(self):
        self.current_block_num = 0
        return self

    def __next__(self):
        if self.current_block_num < len(self.document_text_blocks):
            current_page = self.document_text_blocks[self.current_block_num]
            self.current_block_num += 1
            return current_page
        else:
            raise StopIteration
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @property
    def num_text_blocks(self) -> int:
        """returns the number of elements in the document_text_blocks list

        Returns:
            int: # of elements in self.document_text_blocks
        """
        return len(self.document_text_blocks)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_text_block( self,
                        text : str,
                        conf = 0.,
                        label = 'UNKNOWN') -> None:
        """Add a text block to the document

        Args:
            text_block (DocumentTextBlock): text block to be added
        """

        self.document_text_blocks.append(DocumentTextBlock(text, conf, label))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_text(self) -> str:
        page_text = ''
        
        for text_block in self.document_text_blocks:
            page_text += text_block.text + '\n'    
            
        return page_text
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class ExtractedDocument:
    """
    dataclass representing the data extracted from a pdf by fitz
    """
    document_pages : List = field(default_factory=lambda: [])

    file_path : str = ''
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __iter__(self):
        self.current_page_num = 0
        return self

    def __next__(self):
        if self.current_page_num < len(self.document_pages):
            current_page = self.document_pages[self.current_page_num]
            self.current_page_num += 1
            return current_page
        else:
            raise StopIteration
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @property
    def num_pages(self) -> int:
        """returns the number of elements in the document_pages list

        Returns:
            int: # of elements in self.document_pages
        """
        return len(self.document_pages)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def get_page(self,
                 requested_page_num : int) -> DocumentPage:
       
        for page in self.document_pages:
            if page.page_number == requested_page_num:
                return page 
        return None
   
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    
    def add_page(self,
                 page : DocumentPage):
        
        self.document_pages.append(page)
    