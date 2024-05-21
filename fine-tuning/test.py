import os
import json

from pprint import pprint

from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay
from umap import UMAP
from sentence_transformers import SentenceTransformer

import numpy as np

import pandas as pd
import plotly_express as px

from SentenceClassifier.Classifier import DataSet

from correction_samples_generator import generate_correction_samples as gcs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BASE_DATA_PATH = '/home/nickshiell/Documents/Work/ActiveProjects/data/Leanne'
BASE_TRAINING_DATA_PATH = os.path.join(BASE_DATA_PATH,'training_data/COMP_CON_SOC_ENV')
TRAINING_DATA_FILE_PATH = os.path.join(BASE_TRAINING_DATA_PATH, 'label_sentence_data_balanced.csv')

OUTPUT_CORRECTION_SAMPLES_FILE = 'fine_tuning_corrections.json'
OUTLIER_JSON_FILE_PATH = 'correction_samples.json'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def generate_interactive_plot(training_data_set : DataSet) -> None:
        
        df = pd.DataFrame()
        df.insert(0, "Reduced Feature 1", training_data_set.get_reduced_embeddings()[:, 0], True)
        df.insert(1, "Reduced Feature 2", training_data_set.get_reduced_embeddings()[:, 1], True)
        df.insert(2, "sentence", training_data_set.get_sentences(), True)
        df.insert(3, "label", training_data_set.get_label_list(), True)
        
        fig = px.scatter(df,
                         x="Reduced Feature 1", 
                         y="Reduced Feature 2", 
                         hover_name=df["sentence"].str.wrap(30).apply(lambda x: x.replace('\n', '<br>')),
                         color="label",
                         hover_data={'label': False, 
                                     'Reduced Feature 1': False,
                                     'Reduced Feature 2': False})
        
        return fig    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    
    #generate_correction_samples
    #_ = gcs(training_data_file_path=TRAINING_DATA_FILE_PATH)
    
    f = open(OUTLIER_JSON_FILE_PATH)
    outlier_data = json.load(f)
        
    full_data_set = DataSet(file_path=TRAINING_DATA_FILE_PATH)
    
    correction_samples = {'corrections' : []}
        
    for sample in outlier_data['samples']:
                
        predicted_sentences = full_data_set.get_data_with_label(sample['pred'])
        
        similarity_val = 0.
        if sample['actual'] == sample['pred']:
            similarity_val = 1.
        
        for datum in predicted_sentences:
            correction = {'sentence 1' : sample['sentence'],
                          'sentence 2' : datum.sentence,
                          'similarity' : similarity_val}
    
            correction_samples['corrections'].append(correction)

    with open(OUTPUT_CORRECTION_SAMPLES_FILE, "w") as outfile: 
        json.dump(correction_samples, outfile)
   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()