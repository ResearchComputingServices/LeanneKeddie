import csv
import re 

from pprint import pprint

from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, OpenAI, PartOfSpeech
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.dimensionality import BaseDimensionalityReduction

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_bertopic_model() -> BERTopic:
    empty_dimensionality_model = BaseDimensionalityReduction()
    clf = LogisticRegression()
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
          
    topic_model= BERTopic(  umap_model=empty_dimensionality_model,
                            hdbscan_model=clf,
                            ctfidf_model=ctfidf_model)
    
    return topic_model

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labelled_sentences(file_path : str) -> dict:
        
    labelled_data_dict = {}
   
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
       
        for item in data:
            label = item[0]
            sentence = re.sub(r'[^a-zA-Z\s]+', "", item[1])
            
            if len(sentence) > 10:
                                         
                if label in labelled_data_dict.keys():
                    labelled_data_dict[label].append(sentence)
                else:
                    labelled_data_dict[label] = [sentence]
    
    return labelled_data_dict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_labelled_data(labeled_data_dict : dict) -> tuple:
    
    labels = []
    sentences = []
        
    keys = sorted(list(labeled_data_dict.keys()))
    
    for i, key in enumerate(keys):
        topic_sentences = labeled_data_dict[key]
        
        sentences.extend(topic_sentences)  
        
        labels.extend([i]*len(topic_sentences))
        
    return sentences, labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def train_model(topic_model : BERTopic, 
                input_data_file_path : str, 
                output_file_path : str)-> None:
    
    labeled_data_dict = get_labelled_sentences(input_data_file_path)    
    sentences, labels = split_labelled_data(labeled_data_dict)
       
    topic_model.fit_transform(sentences, y=labels)
    
    topic_model.save(output_file_path)
    
    for topic in topic_model.get_topics():
        pprint(topic_model.get_topic(topic, full=True))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')  
    
    topic_model.visualize_topics()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# of sentences COMP_CON: 753
# of sentences Irrelevant: 11010
# of sentences SOCENV_INC: 389

def action_train(cl_args_dict : dict) -> None:
          
    topic_model = generate_bertopic_model()

    train_model(topic_model,
                cl_args_dict['data'],
                cl_args_dict['save'])