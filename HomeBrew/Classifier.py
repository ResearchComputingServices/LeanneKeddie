from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay
from umap import UMAP
from sentence_transformers import SentenceTransformer

import numpy as np

import matplotlib.pyplot as plt

from DataSet import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Classifier:
    
    def __init__(self,
                 name : str) -> None:
        
        self.name = name
        self.logreg_classifier = LogisticRegression(verbose=True)
        self.sentence_transformer_path = None
        self.umap_transformer = None
        self.data_set = None
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _check_train(self) -> bool:
        """ private method called by train_classifier which checks to make sure
        all required members are set

        Returns:
            bool: True if readu to train
        """
        
        if self.data_set == None:
            return False
        
        if self.sentence_transformer_path == None:
            return False
        
        if not self.data_set.is_embedded:
            return False
        
        if not self.data_set.is_reduced:
            return False
        
        return True       

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _check_data_set(self) -> bool:
        """ Checks if the data set has been set

        Returns:
            bool: Returns true if the data set has been set
        """
        if self.data_set == None:
            return False
        
        return True
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _check_transformer_path(self) -> bool:
        """ Checks if the sentence transformer path has been set

        Returns:
            bool: Returns true if the sentence transformer path has been set
        """
        if self.sentence_transformer_path == None:
            return False
        
        return True
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _check_umap(self) -> bool:
        """ Checks if the UMAP embedding reducer has initialized

        Returns:
            bool: Returns true if UMAP embedding reducer has initialized
        """
        if self.umap_transformer == None:
            return False
        
        return True
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _create_umap_transformer(   self,
                                    embeddings : np.ndarray,
                                    targets = None,
                                    n_components=2,
                                    metric = 'cosine',
                                    min_dist = 0.) -> None:
    
        self.umap_transformer = UMAP(   n_components=n_components,
                                        metric=metric,
                                        min_dist=min_dist)
        
        self.umap_transformer.fit(  X=embeddings, 
                                    y=targets)
            
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _perform_embedding(self) -> None:
        if self._check_transformer_path():
            self.data_set.perform_embedding(SentenceTransformer(self.sentence_transformer_path))
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _perform_reduction(self) -> None:
        if self._check_umap():               
            self.data_set.perform_reduction(self.umap_transformer)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def add_data_set(   self,
                        data_set : DataSet) -> None:
        """add data set used to train the classifier

        Args:
            data_set (DataSet): Object to type DataSet
        """
        
        self.data_set = data_set
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def train_classifier(self,
                         training_fraction = 0.7) -> None:
        """trains the classifier on the data provided in data_set
        """

        if self._check_data_set():
           self._train_classifier(training_fraction)     
            
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _train_classifier(self,
                          training_fraction : float) -> None:
        
        ds_train, ds_verify = self.data_set.split_training_testing(training_fraction)
        
       
        self._create_umap_transformer(  embeddings=ds_train.get_embeddings(),
                                        targets=ds_train.data_set.get_label_index_list())
        
        
        self.logreg_classifier.fit( ds_train.get_reduced_embeddings()
                                    ds_train.get_label_index_list())


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def display_training_results(self) -> None:

        print(self.logreg_classifier.coef_)
        print(self.logreg_classifier.intercept_)
        
        print(f'slope = {-1*self.logreg_classifier.coef_[0][0]/self.logreg_classifier.coef_[0][1]}')
        print(f'y-int = {-1*self.logreg_classifier.intercept_[0]/self.logreg_classifier.coef_[0][1]}')
        
        _, ax = plt.subplots(figsize=(4, 3))
        
        DecisionBoundaryDisplay.from_estimator(
            self.logreg_classifier,
            self.reduced_embeddings,
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
        plt.scatter(self.reduced_embeddings[:, 0],
                    self.reduced_embeddings[:, 1], 
                    c=self.targets, 
                    edgecolors="k", 
                    cmap=plt.cm.Paired)

        plt.xticks(())
        plt.yticks(())

        plt.show()
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def test_classifier(self,
                        test_data_set : DataSet,
                        test_label : str,
                        verbose = False) -> None:
        
        
        if not test_data_set.check_label(test_label):
            print(f'WARNING: label <{test_label}> not in data set.')
            return
        
        total = len(test_data_set.data_list)
        
        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        
        for i, test_sample in enumerate(test_data_set.data_list):
            formatted_sample = np.array(test_sample.reduced_encoding).reshape(1, -1)
        
            probs = self.logreg_classifier.predict_proba(formatted_sample)
        
            predicted_class_index = self.logreg_classifier.predict(formatted_sample)
            predicted_class_label = test_data_set.get_label_from_index(predicted_class_index)
                
            actual_class_label = test_sample.label
            actual_class_index = test_data_set.labels[actual_class_label]
                    
            if actual_class_index == predicted_class_index:
                if actual_class_label == test_label:
                    true_pos += 1
                else:
                    true_neg += 1
            else:
                if actual_class_label == test_label:
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
        
        num_pos = len(test_data_set.get_data_with_label(test_label))        
        num_neg = total - num_pos
                
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