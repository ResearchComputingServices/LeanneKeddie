from umap import UMAP
from sentence_transformers import SentenceTransformer

import numpy as np

import pandas as pd
import plotly_express as px

from sentence_transformers import SentenceTransformer
from SentenceClassifier.Classifier import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# LLM to compare
PRETRAIN_MODEL = 'all-MiniLM-L6-v2'
FINE_TUNED_MODEL = './fine-tuned-model'

USE_MODEL = PRETRAIN_MODEL

# data location
CLEANED_TRAINING_DATA = 'data/label_sentence_data_cleaned.csv'
BALANCED_TRAINING_DATA = 'data/label_sentence_data_balanced.csv'

TRAINING_DATA_FILE_PATH = CLEANED_TRAINING_DATA

# UMAP
N_COMPONENTS = 2
METRIC_TYPE = 'cosine'
MIN_DIST = 0.

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
    sentence_transformer = SentenceTransformer(USE_MODEL)

    raw_umap_transformer = UMAP(n_components=N_COMPONENTS,
                            metric=METRIC_TYPE,
                            min_dist=MIN_DIST)
    
    full_data_set = DataSet(file_path=TRAINING_DATA_FILE_PATH)
    full_data_set.perform_embedding(sentence_transformer)
    
    raw_umap_transformer.fit(X=full_data_set.get_embeddings())
    
    full_data_set.perform_reduction(raw_umap_transformer)

    fig = generate_interactive_plot(full_data_set)
    fig.show()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()
