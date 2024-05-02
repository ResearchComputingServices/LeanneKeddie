
from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator
from SentenceClassifier.Classifier import SentenceClassifier

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    # train_data_path = 'training_data/COMP_CON_SOC_ENV/label_sentence_data_cleaned.csv'
    # classifier_name = 'COMP_SOC'
    # sentence_transformer_path = 'all-MiniLM-L6-v2'

    # pdf_file_path = 'docs/Proxy2016Subset/AAPL 2016.pdf'
    
    # c = SentenceClassifier( name=classifier_name,
    #                         training_data_path=train_data_path,
    #                         pretrained_transformer_path=sentence_transformer_path)

    # c.train_classifier()

    doc_gen = ExtractedDocumentGenerator()
    # extract_doc = doc_gen.extract(pdf_file_path, [1,5,10])

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