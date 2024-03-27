import json
import csv
import random
import re

from sentence_transformers import SentenceTransformer
from umap import UMAP
from sklearn import preprocessing as p

import numpy as np

from pprint import pprint

# =========================================================================

class Datum:
    
    def __init__(self, 
                 sentence = '',
                 label_index = -1,
                 confidence = -1.,
                 label_string = '',
                 encoding = [],
                 reduced_encoding = []):
        
        self.sentence = sentence
        self.label_index = label_index
        self.label_string = label_string
        self.confidence = confidence        
        self.encoding = [float(x) for x in encoding]
        self.reduced_encoding = [float(x) for x in reduced_encoding]

    def to_dict(self) -> dict:
        return {'sentence' : self.sentence,
                'label_index' : self.label_index,
                'label_string' : self.label_string,
                'confidence' : str(self.confidence),
                'encoding' : [str(x) for x in self.encoding],
                'reduced_encoding' : [str(x) for x in self.reduced_encoding]}


# =========================================================================

class DataSet:
    
    def __init__(self,
                 file_path = ''):
        
        self.data_list = []
        self.embedding = ''
        self.reduced = ''
        self.topic_labels = {}
    
        if file_path.endswith('.json'):
            self.load_json(file_path)
        elif file_path.endswith('.csv'):
            self.load_csv(file_path)
        else:
            self.file_path = file_path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_label_from_index(self, 
                             index : int) -> str:
        
        for item in self.topic_labels.items():
            if item[1] == index:
                return item[0]
            
        return 'UNKNOWN'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def get_sentences(self) -> list:
        return [d.sentence for d in self.data_list]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def get_embeddings(self) -> np.ndarray:
        return np.array([d.encoding for d in self.data_list])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def get_reduced_embeddings(self) -> np.ndarray:
        return np.array([d.reduced_encoding for d in self.data_list])
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_label_index(self) -> np.ndarray:
        return np.array([d.label_index for d in self.data_list])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_data_with_label_index(self,
                                  label_index : int) -> list:
        
        return [d for d in self.data_list if d.label_index == label_index]
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def split_training_testing(self,
                               training_fraction = 0.9) -> tuple:
    
        random.shuffle(self.data_list) 
        
        ds_training = DataSet()
        ds_testing  = DataSet()
        
        split_index = int(len(self.data_list)*training_fraction)
        
        ds_training.topic_labels = self.topic_labels
        ds_testing.topic_labels = self.topic_labels
        
        ds_training.data_list = self.data_list[:split_index] 
        ds_testing.data_list = self.data_list[split_index:] 
        
        return ds_training, ds_testing

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def save_as_json(self, 
                     file_path : str) -> None:
                    
        with open(file_path, "w+") as final:
            json.dump(self._get_json_dict(), final)
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    
    def load_json(  self, 
                    file_path : str) -> None:
        
        json_dict = json.load(open(file_path,'r'))
        
        self.embedding = json_dict['embedding']
        self.reduced = json_dict['reduced']
        self.file_path = json_dict['file_path']
        self.topic_labels = json_dict['topic_labels']
        
        for datum in json_dict['data']:
            self.data_list.append(Datum(**datum))
              
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        

    def load_csv(self, 
                 file_path : str) -> None:
        
        self.file_path = file_path
   
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            
            for item in data:
                # item[0] label_string, itme[1] sentence, item[2] prob                                                
                if item[0] not in self.topic_labels.keys():
                    self.topic_labels[item[0]] = len( self.topic_labels)
                
                confidence = -1.
                if len(item) > 2:
                    confidence = item[2]
                    
                datum = Datum(  sentence=re.sub(r'[^\x00-\x7F]+',' ', item[1]),
                                label_string=item[0],
                                label_index=self.topic_labels[item[0]],
                                confidence=confidence)         
                
                self.data_list.append(datum)
  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
  
    def _get_json_dict(self) -> dict:
        json_dict = {'file_path' : self.file_path,
                     'embedding' : self. embedding,
                     'reduced' : self.reduced,
                     'topic_labels' : self.topic_labels,
                     'data' : []}
        
        
        for datum in self.data_list:
            json_dict['data'].append(datum.to_dict())
            
        return json_dict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def perform_embedding(  self,
                            sentence_transformer : SentenceTransformer) -> None:
                
        embeddings = sentence_transformer.encode(   sentences=self.get_sentences(), 
                                                    show_progress_bar=True,
                                                    convert_to_numpy=True)
        
        # for sentence in self.get_sentences():           
        #     o = sentence_transformer.tokenizer( sentence, 
        #                                         return_attention_mask=False, 
        #                                         return_token_type_ids=False)
            
        #     num_characters = len(sentence)
        #     num_words = len(sentence.split(' '))
        #     num_tokens = len(o.input_ids)
        #     max_seq_len = sentence_transformer.max_seq_length
        #     if num_tokens > max_seq_len:
        #         print(f'{num_characters} / {num_words} / {num_tokens} / {max_seq_len}')
                
        for i, embedding in enumerate(embeddings):
            self.data_list[i].encoding = list(embedding)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def perform_reduction(self,
                          umap_transformer : UMAP) -> None:
        
        reduced_embeddings = umap_transformer.transform(X=self.get_embeddings())
                
        for i, reduced in enumerate(reduced_embeddings):
            self.data_list[i].reduced_encoding = list(reduced)
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def normalize_data(self,
                       min_max_scaler : p.MinMaxScaler):
        
        normalized_data = min_max_scaler.transform(self.get_reduced_embeddings())  
        
        for i, normalized in enumerate(normalized_data):
            self.data_list[i].reduced_encoding = list(normalized)
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def save_reduced_embedding(self,
                               file_path : str):

        with open(file_path, 'w+') as output_file:
            for item in self.topic_labels.items():
                for datum in self.get_data_with_label_index(item[1]):
                    output_file.write(" ".join([str(i) for i in datum.reduced_encoding])+'\n')

                output_file.write('\n\n')
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clean_data(self,
                   regex_pattern = r'[^a-zA-Z\s]+') -> None:
        
        cleaned_data_list = []
        
        for datum in self.data_list:
            # TODO: This needs to be fixed so that multiple spaces become single spaces not 0 spaces!
            clean_sentence = re.sub(regex_pattern, "", datum.sentence)
                        
            if len(clean_sentence) > 10:
                    cleaned_data_list.append(datum)
                
        
        self.data_list = cleaned_data_list
        
 # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
    
    def save_topic_reduced_embedding(   self,
                                        topic_index : int,
                                        file_path : str):

        with open(file_path, 'w+') as output_file:
            for item in self.topic_labels.items():
                if int(item[1]) == topic_index:
                    for datum in self.get_data_with_label_index(topic_index):
                        output_file.write("^".join([str(i) for i in datum.reduced_encoding]) + '^' + datum.sentence + '\n')    
                
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def set_topic_labels(self,
                         new_topic_labels : dict):
        
        self.topic_labels = new_topic_labels
        
        for datum in self.data_list:
            
            if datum.label_string in new_topic_labels.keys():
                datum.label_index = new_topic_labels[datum.label_string]
            else:
                print('skip')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~