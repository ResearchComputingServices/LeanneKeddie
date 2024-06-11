import time
import csv

import plotly_express as px
from pprint import pprint

from SentenceClassifier.Classifier import SentenceClassifier
from SentenceClassifier.DataSet import DataSet

def main():
        
    # testing_data_path = 'test.csv'    
    testing_data_path = 'test_full_2017.csv'
      
    classifier = SentenceClassifier()
    
    classifier.load(input_path='/home/nicholishiell/Documents/WorkProjects/Profs/LeanneKeddie/webapp/.public-data/classifier/fine-tuned-level-35')
    
    # fig = classifier.generate_interactive_plot()
    # fig.show()   
     
    results = classifier.test_classifier(test_data_path=testing_data_path)
    pprint(results)

if __name__ == '__main__':
    main()
   