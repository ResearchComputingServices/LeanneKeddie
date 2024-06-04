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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PRETRAIN_MODEL = 'all-MiniLM-L6-v2'

CONF_THRESHOLD = 0.9

# UMAP
N_COMPONENTS = 2
METRIC_TYPE = 'cosine'
MIN_DIST = 0.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def outlier_detector(training_data_file_path,
                     output_json_file_path):
    
    logreg_classifier = LogisticRegression(verbose=True)
    
    sentence_transformer = SentenceTransformer(PRETRAIN_MODEL)

    raw_umap_transformer = UMAP(n_components=N_COMPONENTS,
                            metric=METRIC_TYPE,
                            min_dist=MIN_DIST)
    
    full_data_set = DataSet(file_path=training_data_file_path)    
    full_data_set.perform_embedding(sentence_transformer)
    
    raw_umap_transformer.fit(X=full_data_set.get_embeddings())
    
    full_data_set.perform_reduction(raw_umap_transformer)
    
    samples = full_data_set.get_reduced_embeddings()
    labels = full_data_set.get_label_index_list()

    logreg_classifier.fit(  X=samples,
                            y=labels)
    
    results_json = {'outliers' : [],
                    'inliers' : {}}
    
    # find all the outliers    
    for datum in full_data_set.data_list:
       
        reduced_sample_embedding = datum.reduced_encoding
        formatted_reduced_sample = np.array(reduced_sample_embedding).reshape(1, -1)

        probs = logreg_classifier.predict_proba(formatted_reduced_sample)

        predicted_class_index = logreg_classifier.predict(formatted_reduced_sample)
        predicted_class_label = full_data_set.get_label_from_index(predicted_class_index)
        prediction_conf = probs[0][predicted_class_index][0]

        if (predicted_class_label != datum.label) or (predicted_class_label == datum.label and prediction_conf < CONF_THRESHOLD):
            results_json['outliers'].append({   'sentence' : datum.sentence,
                                                'actual' : datum.label,
                                                'pred' : predicted_class_label,
                                                'conf' : prediction_conf})
        else:
            if datum.label in results_json['inliers'].keys():
                results_json['inliers'][datum.label].append(datum.sentence)
            else:
                results_json['inliers'][datum.label] = [datum.sentence]

    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # save tp json file  
    #json_data = json.dumps(fine_tuning_corrections)
    with open(output_json_file_path, "w") as outfile: 
        json.dump(results_json, outfile)
        
    return results_json