
from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator
from SentenceClassifier.Classifier import SentenceClassifier

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    train_data_path = 'training_data/COMP_CON_SOC_ENV/label_sentence_data_cleaned.csv'
    # train_data_path = 'training_data/COMP_CON_SOC_ENV/label_sentence_data.csv'
    
    # test_data_path = 'docs/verification/4000_test_cases_corrected.csv'
    test_data_path = 'docs/verification/3380_test_cases.csv'
    
    classifier_name = 'COMP_SOC'
    # sentence_transformer_path = 'all-MiniLM-L6-v2'
    sentence_transformer_path = 'fine-tuned-COMP-CON-FULL-all-MiniLM-L6-v2'

    pdf_file_path = 'ddocs/Proxy_2017/APPL2017.pdf'
    
    c = SentenceClassifier( name=classifier_name,
                            pretrained_transformer_path=sentence_transformer_path)

    c.set_train_data_path(train_data_path)

    c.train_classifier()

    fig = c.generate_interactive_plot()

    fig.show()

    c.test_classifier(test_data_path = test_data_path,
                      test_label = 'COMP_CON')

    # doc_gen = ExtractedDocumentGenerator()
    # extract_doc = doc_gen.extract_from_path(pdf_file_path, [1,5,10])

    # for page in extract_doc:
    #     for text_box in page:
    #         if text_box.label == 'Text':
    #             for sentence in text_box.sentences:
    #                 label, prob = c.classify(sentence)
    #                 if label != 'Irrelevant':
    #                     print(f'page # {page.page_number} [{sentence}] --> {label} conf {prob}')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()