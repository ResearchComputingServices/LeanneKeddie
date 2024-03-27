import csv
from pprint import pprint
import difflib

# constants
#label_sentence_data_file_path = '../training_data/label_sentence_data.csv'
label_sentence_data_file_path = '../training_data/label_sentence_data_balanced.csv'
target_label = 'COMP_CON'
fine_tuning_file_path = '../training_data/COMP_CON_fine_tuning.csv'

# check if strings are similar
def not_the_same(a : str, b : str) -> bool:
    seq=difflib.SequenceMatcher(a=a.lower(), b=b.lower())

    return seq.ratio() < 0.9

# read the labelled sentence data from a .csv file
labelled_sentences = []

with open(label_sentence_data_file_path, 'r') as file:
    reader = csv.reader(file)
    labelled_sentences = list(reader)
    
# read the bad encoded sentences from a text file
bad_encoded_sentences = open('../training_data/COMP_CON_bad_encoding.txt').readlines()


# compare the target_label to the label in labelled_sentences and create the fine_tuning data

fine_tuning_output = open(fine_tuning_file_path, 'w+')

for bad_encoding in bad_encoded_sentences:
    
    bad_encoding = bad_encoding.strip()
    
    for item in labelled_sentences:              
        if item[0] == target_label:
            if not_the_same(bad_encoding, item[1]):
                output_string = bad_encoding + '^' + item[1] + '^' +'1.\n'
                fine_tuning_output.write(output_string)
        else:
            output_string = bad_encoding + '^' + item[1] + '^' +'0.\n'
            fine_tuning_output.write(output_string)

fine_tuning_output.close()