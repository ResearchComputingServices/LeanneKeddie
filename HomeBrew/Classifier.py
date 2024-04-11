from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay

import numpy as np

import matplotlib.pyplot as plt

from DataSet import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Classifier:
    
    def __init__(self,
                 name : str) -> None:
        self.name = name
        self.logreg = LogisticRegression(verbose=True)
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def train_classifier(self,
                         data_set : DataSet) -> None:
        """trains the classifier on the data provided in data_set

        Args:
            data_set (DataSet): an instance of a DataSet object
        """
    
        self.reduced_embeddings = data_set.get_reduced_embeddings()
        self.targets = data_set.get_label_index_list()
                    
        self.logreg.fit(self.reduced_embeddings, 
                        self.targets)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def display_training_results(self) -> None:

        print(self.logreg.coef_)
        print(self.logreg.intercept_)
        
        print(f'slope = {-1*self.logreg.coef_[0][0]/self.logreg.coef_[0][1]}')
        print(f'y-int = {-1*self.logreg.intercept_[0]/self.logreg.coef_[0][1]}')
        
        _, ax = plt.subplots(figsize=(4, 3))
        
        DecisionBoundaryDisplay.from_estimator(
            self.logreg,
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
        
            probs = self.logreg.predict_proba(formatted_sample)
        
            predicted_class_index = self.logreg.predict(formatted_sample)
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
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~