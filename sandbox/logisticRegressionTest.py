from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn import preprocessing as p

import numpy as np

from pprint import pprint
import random

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_data(data_file_path : str):
    
    class_id = 0
    data = []
    target = []
    with open(data_file_path, 'r') as in_file:
        lines = in_file.readlines()

        for line in lines:
            if '-----' in line:
                class_id = class_id + 1
            else:
                datum = []
                for value in line.split(' '):
                    if value != '\n':
                        datum.append(float(value))
                data.append(datum)
                target.append(class_id)

    #random.shuffle(target)

    return np.array(data), np.array(target)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          
def main():
    unnormalized_data, target = load_data('./data/reduced_embedding_5.dat')
     
    min_max_scaler = p.MinMaxScaler() 
    data = min_max_scaler.fit_transform(unnormalized_data)    
    
    data_train, data_test, target_train, target_test = train_test_split(data, target)
    
    poly = PolynomialFeatures(degree = 5, 
                              interaction_only=False, 
                              include_bias=False)
    
    data_poly = poly.fit_transform(data_train)
    print(data_poly.shape)
    # input('Press ENTER to continue...')   
    
    lr = LogisticRegression(verbose=True)
    lr.fit(data_poly,target_train)
    
    score = lr.score(poly.transform(data_test), target_test)
    print(score)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
if __name__ == '__main__':
    main()

# data = load_iris()
# X = data.data
# y = data.target

# print(X.shape)
# print(y)

# X_train, X_test, y_train, y_test = train_test_split(X, y)
