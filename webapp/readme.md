# Dictionaries used in the WebApp

## Active Data Set Dictionary

The Active Data Set Dictionary contains the data set currently being
worked on by the user. It is stored in the session_state with the key
ACTIVE_DATA_SET_KEY.

It contains:
1. List of Proxy Statement dicts (key: DATA_SET_PROXY_STATEMENTS)
2. List of Label dicts (key: DATA_SET_LABELS)
3. List of Labelled-Text dicts (key: DATA_SET_LABELLED_TEXT)
4. boolean 'initialized' (key: DATA_SET_INITIALIZED)

### List of Proxy Statement Dicts

List of all the proxy statement pdfs which have been used to create this data set. This data is required for when a user loads a data set, so the
proper passages can be highlighted.

Each dict contains:
1. the base file name of the proxy statement pdf (key: PROXY_STATEMENT_FILENAME)
2. a unique file id (key: PROXY_STATEMENT_FILE_ID)

### List of Label Dict

List of all the labels created by the user for this data set.

Each dict contains:
1. label name (key: LABEL_NAME)
2. hex-code for highlighting colour (key: LABEL_COLOUR)
3. unique label id (key: LABEL_ID)

### List of Labelled-Text Dicts

This is a list of all the passages which have been labelled by the user. 

Each dict contains:
1. The text labelled (key: LABELLED_TEXT_TEXT)
2. The proxy statement PDFs file id (key: LABELLED_TEXT_FILE_ID)
3. The label id (key: LABELLED_TEXT_LABEL_ID)
4. A unique id (key: LABELLED_TEXT_ID)

## Active Results List

This list is populated when a classifier has been used to classify all the sentences contained in the proxy statements. One Result Dictionary is created  and added to the list for each proxy statement. 

Each dictionary contains:
1. the file name


## ExtractedDocument Dictionary

This dictionary contains all the text data which has been extracted from the proxy statement PDFs by the Nipigon DocumentAI package. 

Each extracted document contains:

1. The path to the ExtractedDocument file (key: EXTRACTED_DOCUMENT_FILE_PATH)
2. A list of DocumentPage dictionaries (key: EXTRACTED_DOCUMENT_PAGES)

### DocumentPage Dictionary

Each Document Page dict contains:

1. A page numner (key: page_number)
2. a list of document text block dictionaries (key: EXTRACTED_DOCUMENT_TEXT_BLOCKS)

### TextBlock Dictionary

Each TextBlock contains:

1. A label assigned by Nipigon describing the type of text block (ie. paragrah-text, footer, header, section head, title, etc...) (key: EXTRACTED_DOCUMENT_TEXT_BLOCK_LABEL)
2. A confidence value assigned by Nipigon (key: 'conf')
3. A list of Sentence Dictionaries (key: EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES)

### Sentence Dictionary

Each sentence dictionary contains:

1. The text of the sentence (key: EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES_TEXT)
2. A label (not used) (key : 'label')
3. A confidence (not used) (key : 'conf')

