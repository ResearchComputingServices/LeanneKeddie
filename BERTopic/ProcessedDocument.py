import fitz
from nltk.tokenize import sent_tokenize
from dataclasses import dataclass, field
from typing import List
from pprint import pprint

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class ProcessedSentence:
    """
    dataclass containing sentence text and topic confidence
    """
    
    sentence_text : str = ''
    page_number : int = -1
    topic_confidences : dict  = field(default_factory=lambda: {})
    assigned_topic : int = -1

    def __str__(self) -> str:
        out_str = str(self.page_number+1)+'^'+self.sentence_text+'^'+str(self.assigned_topic)
        
        for item in self.topic_confidences.items():
            out_str = out_str + '^' + str(item[1])
        
        return out_str

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class ProcessedDocument:
    """
    dataclass containing text from PDF and analysis results
    """
    
    sentences :  List = field(default_factory=lambda: [])
    file_path : str = ''
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __init__(self, 
                 file_path : str):
        
        self.file_path = file_path
        
        self.sentences = []
        
        self._populate()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def save_csv(   self,
                    file_path : str) -> None:
        
        with open(file_path,'w+') as fp:
            for sentence in self.sentences:
                fp.write(sentence.__str__() + '\n')
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def get_sentences(self) -> list:
        sentences = []
        
        for sentence in self.sentences:
            sentences.append(sentence.sentence_text)
        
        return sentences
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _populate(self):
        
        fitz_doc = self._open_fitz()
        
        if fitz_doc is not None:
            self.process_fitz_doc(fitz_doc)
              
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def process_fitz_doc(   self,
                            fitz_doc):
        
        for page_num , page in enumerate(fitz_doc):
            
            # output plain text in desired reading sequence
            blocks = page.get_text("dict", flags=10, sort=True)["blocks"]
            self._process_blocks(page_num, blocks)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _process_blocks(self,
                        page_num,
                        blocks):
        
        for block in blocks:
            text = self._extract_text(block)
            self._extract_sentences(page_num, text)
   
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _extract_text(self, block) -> str:
        
        text = ''
        
        for line in block['lines']:
            for span in line['spans']:
                text = text + span['text'] + ' '
                
        return text
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _extract_sentences(self,
                           page_num, 
                           text):
    
        for sentence in sent_tokenize(text):
            self.sentences.append(ProcessedSentence(page_number=page_num, 
                                                    sentence_text=sentence))
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _open_fitz(self):
        
        fitz_doc = None
        
        try:
            fitz_doc = fitz.open(self.file_path)
        
        except fitz.fitz.FileDataError:
            print('Can not open file: ', self.file_path)
        
        return fitz_doc
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~