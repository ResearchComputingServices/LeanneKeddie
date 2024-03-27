import pysbd
from glob import glob

txt_file_list = glob('../pdfTextractor/extractedText/*.txt')

print(f'# of files found: {len(txt_file_list)}')

for txt_file in txt_file_list:
    print(f'filename: {txt_file}')
    with open(txt_file, 'r', encoding='utf-8') as input_file:
        text = input_file.read().replace('\n', ' ').replace('~','')
        
        sentences = pysbd.Segmenter(language="en", doc_type='pdf', clean=True).segment(text)
        print(f'# of sentences: {len(sentences)}')
        for sentence in sentences:
            print(sentence)
            input()