from distutils.dir_util import copy_tree

import streamlit as st

from utils import *

from SentenceClassifier.Classifier import SentenceClassifier
from SentenceClassifier.FineTuner import fine_tune_llm, generate_interactive_plot

from create_load_data_set_page import load_file_cb

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 

def save_classifier_cb(classifier_name : str,
                       save_type : str) -> None:
    
    # if the classisifer exsits
    if st.session_state[ACTIVE_CLASSIFIER_KEY]:
        st.session_state[TRAIN_FIGURE_KEY].write_json(get_user_tmp_classifier_path()+'/fig.json')
        
        with open(get_user_tmp_classifier_path()+'/train_results.json', 'w+') as fp:
            json.dump(st.session_state[TRAIN_TEST_RESULTS_KEY] , fp)
        
        src_path = get_user_tmp_classifier_path() 
        
        # get the output path to save the file too
        dst_path = os.path.join(PUBLIC_CLASSIFIER_PATH, classifier_name)
        if save_type == 'private':
            dst_path = os.path.join(USER_DATA_PATH,
                                    st.session_state[USER_CRED_KEY],
                                    PRIVATE_CLASSIFIER_PATH,
                                    classifier_name)
        copy_tree(src_path, dst_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def train_classifier_cb(classifier_name : str,
                        user_selected_model : str,
                        selected_data_set_file : str,
                        training_fraction : float,
                        num_finetune_corr : int) -> None:
    
    # remember to load the data set file into the sessoin state
    load_file_cb(selected_data_set_file)
    
    full_data_set = convert_2_data_set()    
    train_set, test_set = full_data_set.split_training_testing(training_fraction)
    
    fine_tuned_model_path = user_selected_model
    if num_finetune_corr > 0:
        fine_tuned_model_path = fine_tune_llm(  data_set=train_set,
                                                base_output_path=get_user_tmp_classifier_path(),
                                                path_to_pretrained_llm=user_selected_model,
                                                num_corrections=num_finetune_corr)
            
    c = SentenceClassifier(name = classifier_name,
                           pretrained_transformer_path=fine_tuned_model_path,
                           verbose=True)

    c.add_data_set(train_set)

    c.train_classifier()
   
    c.save(output_path=get_user_tmp_classifier_path())
    
    if training_fraction < 0.99:
    
        results = []

        for label in test_set.get_labels():
            result_dict = c._test_classifier(   test_data_set=test_set,
                                                test_label=label)
            results.append(result_dict)
        
        st.session_state[TRAIN_TEST_RESULTS_KEY] = results    
    
    st.session_state[TRAIN_FIGURE_KEY] = c.generate_interactive_plot()
   
    st.session_state[ACTIVE_CLASSIFIER_KEY] = c
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def train_page():
    
    pretrain_model_options = ['all-MiniLM-L6-v2',
                              'nli-distilroberta-base-v2',
                              'paraphrase-MiniLM-L6-v2']
    
    user_selected_model = st.sidebar.radio('Select Pre-Trained Model', 
                                            options=pretrain_model_options )

    selected_file = st.sidebar.selectbox(   label='Data Set Files',
                                            options=get_data_set_files(),
                                            index=None)
    
    training_fraction = st.sidebar.slider(label='Select Training Fraction',
                                            min_value=0.6,
                                            max_value=1.0,
                                            value = 0.7)
    
    num_finetune_corr = st.sidebar.slider(  label='Select Fine Tuning Level',
                                            min_value=0,
                                            max_value=300,
                                            value = 5)
    
    
    classifier_name = st.sidebar.text_input('Classifier Name')
    
    st.sidebar.button('Train',
                      on_click=train_classifier_cb,
                      args=[classifier_name,
                            user_selected_model,
                            selected_file,
                            training_fraction,
                            num_finetune_corr],
                      disabled=((classifier_name == '') or (selected_file == None)))

    with st.sidebar.popover(f'Save Classifer'):

        button_col,type_cal = st.columns([1,1])
        
        save_type = type_cal.radio( 'Save Type',
                                    options = ['private', 'public'],
                                    disabled = (not st.session_state[ACTIVE_CLASSIFIER_KEY]) or (classifier_name == ''))
        
        button_col.button(  'Save',
                            on_click=save_classifier_cb,
                            args=[classifier_name, save_type],
                            disabled = (not st.session_state[ACTIVE_CLASSIFIER_KEY]) or (classifier_name == ''))
        
    
    display_classifier()