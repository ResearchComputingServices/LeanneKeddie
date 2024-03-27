from pprint import pprint

import argparse

from TrainModel import action_train
from ClassifyDocuments import action_classify
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extract_command_line_args() -> dict:
    """generates the parser and applies it to the command line args

    Returns:
        dict: a dictionary containing the command line args.
    """
    parser = argparse.ArgumentParser(prog= 'SupervisedTM',
                                     description= 'Perform supervised topic modelling using BERTopic')

    # parser.add_argument('--'+configs.CL_ARG_INPUT_FLAG,
    #                     default=configs.CL_ARG_INPUT_DEFUALT,
    #                     help = configs.CL_ARG_INPUT_HELP)

    # parser.add_argument('--'+,
    #                     default=,
    #                     help=)

    parser.add_argument('--'+'classify',
                        action=argparse.BooleanOptionalAction,
                        help='perform classification on document(s)')

    parser.add_argument('--'+'load',
                        default='./models/feb_15_topic_model.mod',
                        help='load the topic model at this location')

    parser.add_argument('--'+'docs',
                        default='./Proxy2016Blees/A 2016.pdf',
                        help='path to document(s) to be classified')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    parser.add_argument('--'+'train',
                        action=argparse.BooleanOptionalAction,
                        help='perform training on data')

    parser.add_argument('--'+'data',
                        default='./training_data/label_sentence_data.csv',
                        help='file path to training data')
    
    parser.add_argument('--'+'save',
                        default='./models/feb_15_topic_model.mod',
                        help='file path to save trained topic model')
    
    args = parser.parse_args()

    return vars(args)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    
    cl_args_dict = extract_command_line_args()
    
    if cl_args_dict['train']:
        action_train(cl_args_dict)
    
    if cl_args_dict['classify']:
        action_classify(cl_args_dict)
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()