import csv
import re
import pickle

import matplotlib.pyplot as plt

from pprint import pprint

import numpy as np

from sentence_transformers import SentenceTransformer
from umap import UMAP

from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing as p
from sklearn.inspection import DecisionBoundaryDisplay

from DataSet import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_umap_transformer(embeddings : np.ndarray,
                            targets = None,
                            n_components=2,
                            metric = 'cosine',
                            min_dist = 0.) -> UMAP:
    
    umap_transformer = UMAP(n_components=n_components,
                            metric=metric,
                            min_dist=min_dist)
    
    umap_transformer.fit(X=embeddings, y= targets)
    
    return umap_transformer

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_umap_transformer(umap_transformer : UMAP,
                          file_path : str) -> None:
    
    pickle.dump(umap_transformer, open(file_path, 'wb'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_umap_transformer(file_path : str) -> UMAP:
    return  pickle.load((open(file_path, 'rb')))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_lr_classifier( lr_classifier : LogisticRegression,
                        file_path : str) -> None:
    
    pickle.dump(lr_classifier, open(file_path, 'wb'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_lr_classifier(file_path : str) -> LogisticRegression:
    return  pickle.load((open(file_path, 'rb')))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_train_classifier():
    #load previous prepared data and umap_transformer
    data_set = DataSet('./test_full.json')
   
       
    #train the classifier
    #ds_train, ds_test = data_set.split_training_testing()  
    lr_classifier = train_classifier(data_set)
    save_lr_classifier(lr_classifier, 'lr_classifier.mod')
   
    #test the classifier
    #test_classifier(lr_classifier, ds_test)    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_test_unseen_data():
    umap_transformer = load_umap_transformer('transformer.umap')
     
    data_set = DataSet('../docs/3380_test_cases.csv')
    data_set.clean_data()
    data_set.perform_embedding(SentenceTransformer("all-MiniLM-L6-v2") )
    data_set.perform_reduction(umap_transformer)
    
    min_max_scaler = p.MinMaxScaler() 
    data_set.normalize_data(min_max_scaler)
    data_set.save_as_json('3380_test_cases.json')
    
    data_set.save_reduced_embedding('./test_reduced_embedding.dat')
    
    lr_classifier = load_lr_classifier('lr_classifier.mod')
    test_classifier(lr_classifier, data_set)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def train_classifier(data_set : DataSet):
    
    reduced_embeddings = data_set.get_reduced_embeddings()
    targets = data_set.get_label_index()
                     
    logreg = LogisticRegression(verbose=True)
    logreg.fit(reduced_embeddings, targets)

    print(logreg.coef_)
    print(logreg.intercept_)
    
    print(f'slope = {-1*logreg.coef_[0][0]/logreg.coef_[0][1]}')
    print(f'y-int = {-1*logreg.intercept_[0]/logreg.coef_[0][1]}')
    
    _, ax = plt.subplots(figsize=(4, 3))
    
    DecisionBoundaryDisplay.from_estimator(
        logreg,
        reduced_embeddings,
        cmap=plt.cm.Paired,
        ax=ax,
        response_method="predict",
        plot_method="pcolormesh",
        shading="auto",
        xlabel="Feature 1",
        ylabel="Feature 2",
        eps=0.5,
    )

    # Plot also the training points
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=targets, edgecolors="k", cmap=plt.cm.Paired)

    plt.xticks(())
    plt.yticks(())

    plt.show()
    
    return logreg
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_classifier(lr_classifier : LogisticRegression, 
                    data_set : DataSet,
                    verbose = False):
        
    total = len(data_set.data_list)
    
    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0
       
    for i, test_sample in enumerate(data_set.data_list):
        formatted_sample = np.array(test_sample.reduced_encoding).reshape(1, -1)
    
        probs = lr_classifier.predict_proba(formatted_sample)
    
        predicted_class_index = lr_classifier.predict(formatted_sample)
        predicted_class_label = data_set.get_label_from_index(predicted_class_index)
            
        actual_class_label = test_sample.label_string
        actual_class_index = test_sample.label_index
                
        if actual_class_index == predicted_class_index:
            if actual_class_index == 1:
                true_pos += 1
            else:
                true_neg += 1
        else:
            if actual_class_index > predicted_class_index:
                false_neg += 1
            else:
                false_pos += 1

        if verbose and predicted_class_index != actual_class_index:
            print(f'{i} of {total}')
            print(test_sample.sentence)
            print(f'Actual Class: {actual_class_label} {actual_class_index}')
            print(f'Predicted: {predicted_class_label} {predicted_class_index}')
            print(probs)
            input()      
    
        # if predicted_class_index != actual_class_index and actual_class_index == 0:
        #     print(test_sample.sentence)
    
    num_neg = len(data_set.get_data_with_label_index(0))
    num_pos = len(data_set.get_data_with_label_index(1))
    
    prec = true_pos / (true_pos + false_pos)
    accu = (true_pos + true_neg)/ total
    reca = true_pos / (true_pos + false_neg)
        
    print(f'True +: {true_pos}')
    print(f'True -: {true_neg}')
    print(f'False +: {false_pos}')
    print(f'False -: {false_neg}')
    print(f'Precision: {prec}')    
    print(f'Accuracy: {accu}')
    print(f'Recall: {reca}')
    print(f'F1-Score: {(2*reca*prec/(reca+prec))}')
    print(f'total: {total}')
    print(f'# +: {num_pos}')
    print(f'# -: {num_neg}')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def run_initialize_data_sets(training_file_path : str,
                             verifying_file_path : str,
                             training_output_path = 'train_data_set.json',
                             verifying_output_path = 'verify_data_set.json',
                             encoder_model = "all-MiniLM-L6-v2"):
    
    train_data_set = DataSet(training_file_path)
    train_data_set.clean_data()
    train_data_set.perform_embedding(SentenceTransformer(encoder_model))
             
    verify_data_set = DataSet(verifying_file_path)
    verify_data_set.clean_data()
    verify_data_set.perform_embedding(SentenceTransformer(encoder_model))
    
    umap_embed = train_data_set.get_embeddings()
    umap_targets = train_data_set.get_label_index()
    #umap_embed = verify_data_set.get_embeddings()
    #umap_targets = verify_data_set.get_label_index()
       
    umap_transformer = create_umap_transformer(embeddings=umap_embed,
                                               targets=umap_targets,
                                               n_components=2)
    
    train_data_set.perform_reduction(umap_transformer)  
    verify_data_set.perform_reduction(umap_transformer)
    
    min_max_scaler = p.MinMaxScaler() 
    vals = np.concatenate((train_data_set.get_reduced_embeddings(), verify_data_set.get_reduced_embeddings()))
    min_max_scaler.fit(vals)
    
    train_data_set.normalize_data(min_max_scaler)
    verify_data_set.normalize_data(min_max_scaler)
    
    train_data_set.save_as_json(training_output_path)
    verify_data_set.save_as_json(verifying_output_path)
         
    train_data_set.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'train_topic_1.dat')
    train_data_set.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'train_topic_2.dat')
    train_data_set.save_topic_reduced_embedding(topic_index=2, 
                                          file_path = 'train_topic_3.dat')   
    
    verify_data_set.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'verify_topic_1.dat')
    verify_data_set.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'verify_topic_2.dat')
    verify_data_set.save_topic_reduced_embedding(topic_index=2, 
                                          file_path = 'verify_topic_3.dat')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_ghg_data():
    
    data_set = DataSet('../training_data/ghg_label_sentence_data.csv')
    data_set.clean_data()
    data_set.perform_embedding(SentenceTransformer('all-MiniLM-L6-v2'))

    # topic_labels = {'GHG' : 1,
    #                 'Irrelevant' : 0}
    
    # data_set.set_topic_labels(topic_labels)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ds_train, ds_verify = data_set.split_training_testing(0.8)

    umap_embed = ds_train.get_embeddings()
    umap_targets = ds_train.get_label_index()

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
    
    ds_train.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'train_topic_1.dat')
    ds_train.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'train_topic_2.dat')
   
    ds_verify.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'verify_topic_1.dat')
    ds_verify.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'verify_topic_2.dat')
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    
    lr_class = train_classifier(ds_train)
    test_classifier(lr_class, ds_verify) 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_virus_data():
    
    data_set = DataSet('../training_data/virus_labelled_data.csv')
    data_set.clean_data()
    data_set.perform_embedding(SentenceTransformer('all-MiniLM-L6-v2'))

    topic_labels = {'BIO' : 1,
                    'COMP' : 0,
                    'NON' : 0}
    
    data_set.set_topic_labels(topic_labels)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ds_train, ds_verify = data_set.split_training_testing(0.8)

    umap_embed = ds_train.get_embeddings()
    umap_targets = ds_train.get_label_index()

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
    
    ds_train.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'train_topic_1.dat')
    ds_train.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'train_topic_2.dat')
   
    ds_verify.save_topic_reduced_embedding(topic_index=0, 
                                          file_path = 'verify_topic_1.dat')
    ds_verify.save_topic_reduced_embedding(topic_index=1, 
                                          file_path = 'verify_topic_2.dat')
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    
    lr_class = train_classifier(ds_train)
    test_classifier(lr_class, ds_verify) 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    
    #run_ghg_data()
    
    run_virus_data()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    #run_train_classifier()     

    #run_test_unseen_data
    
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # run_initialize_data_sets(training_file_path = '../training_data/label_sentence_data.csv',
    #                          verifying_file_path = '../docs/3380_test_cases.csv',
    #                          training_output_path = 'training_data_SOCENV_INC.json',
    #                          verifying_output_path = 'verifying_data_SOCENV_INC.json',
    #                          encoder_model='./fine-tuned-SOCENV-INC-all-MiniLM-L6-v2')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # train and verify on training data set
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # data_set = DataSet('training_data_SOCENV_INC_.json')
    # # ds_train, ds_verify = data_set.split_training_testing(0.5)
    
    # ds_train = data_set
    # ds_verify = data_set
    # lr_class = train_classifier(ds_train)
    # test_classifier(lr_class, ds_verify) 
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # train with training data verify with 'real' data
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # train_data_set = DataSet('training_data_COMP_CON.json')
    # verify_data_set = DataSet('verifying_data_COMP_CON.json')
    
    # topic_labels = {'COMP_CON' : 1,
    #                 'Irrelevant' : 0,
    #                 'SOCENV_INC' : 0}
    
    # train_data_set.set_topic_labels(topic_labels)
    # verify_data_set.set_topic_labels(topic_labels)
      
    # lr_class = train_classifier(train_data_set)
   
    # save_lr_classifier(lr_class, './lr_classifier.mod')
    # test_classifier(lr_class, verify_data_set)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()