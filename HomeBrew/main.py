import numpy as np

from sentence_transformers import SentenceTransformer

from sklearn import preprocessing as p


from DataSet import DataSet
from utils import *
from Classifier import Classifier

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run(file_path : str):
    
    data_set = DataSet(file_path)

    data_set.perform_embedding(SentenceTransformer('all-MiniLM-L6-v2'))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ds_train, ds_verify = data_set.split_training_testing(0.8)

    umap_embed = ds_train.get_embeddings()
    umap_targets = ds_train.get_label_index_list()

    umap_transformer = create_umap_transformer(embeddings=umap_embed,
                                               targets=umap_targets,
                                               n_components=2)

    ds_train.perform_reduction(umap_transformer)
    ds_verify.perform_reduction(umap_transformer)

    min_max_scaler = p.MinMaxScaler()
    vals = np.concatenate((ds_train.get_reduced_embeddings(),
                           ds_verify.get_reduced_embeddings()))
    
    min_max_scaler.fit(vals)
    ds_train.normalize_data(min_max_scaler)
    ds_verify.normalize_data(min_max_scaler)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    c = Classifier('VirusClassifier')
    c.train_classifier(data_set=ds_train)
    #c.display_training_results()
    c.test_classifier(test_data_set=ds_verify,
                      test_label='BIO')    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    
    label_data_fp = '../training_data/label_sentence_data_balanced.csv'  
    #label_data_fp = '../training_data/virus_labelled_data.csv'  
    
    run(label_data_fp)
    
      
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()