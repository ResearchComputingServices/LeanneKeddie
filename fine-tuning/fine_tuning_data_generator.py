import os
import json
import random

from pprint import pprint

from SentenceClassifier.Classifier import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TRAINING_DATA_FILE_PATH = 'data/label_sentence_data_cleaned.csv'

MAX_CORRECTIONS = 25

OUTPUT_CORRECTION_SAMPLES_FILE = 'json/fine_tuning_corrections.json'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# correction = {'sentence 1' : sample['sentence'],
#               'sentence 2' : datum.sentence,
#               'similarity' : similarity_val}

def main():
           
    full_data_set = DataSet(file_path=TRAINING_DATA_FILE_PATH)
    
    correction_samples = {'corrections' : []}

    labels = list(full_data_set.labels.keys())

    # loop over all the samples that are not labelled 'Irrelevant'
    for i,sample in enumerate(full_data_set.data_list):
 
        if sample.label == 'Irrelevant':
            continue
        
        print(f'sample {i+1} of {full_data_set.n_samples}')
        
        # add up to MAX_CORRECTIONS instances of corrections for each label type in the dataset
        for label in labels:   
             
            similariyt_score = 0.
            if label == sample.label:
                similariyt_score = 1.
            
            sentences = full_data_set.get_data_with_label(label)
            random.shuffle(sentences)
            
            for counter, sentence in enumerate(sentences):
                correction_samples['corrections'].append({ 'sentence 1' : sample.sentence,
                                                            'sentence 2' : sentence.sentence,
                                                            'similarity' : similariyt_score})
                
                if counter > MAX_CORRECTIONS:
                    break
                
    print(len(correction_samples['corrections']))
    
    with open(OUTPUT_CORRECTION_SAMPLES_FILE, "w") as outfile: 
        json.dump(correction_samples, outfile)
   
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()