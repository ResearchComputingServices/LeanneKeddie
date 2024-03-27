import re
import pysbd
from glob import glob

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

INPUT_DICTIONARY = {'BIO' : './text/biological_viruses.txt',
                    'COMP' : './text/computer_virus_paragraphs.txt',
                    'NON' : './text/random_paragraphs.txt'}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    
    sample_list = []
    
    for item in INPUT_DICTIONARY.items():
        key = item[0]
        txt_file_path = item[1]
        
    
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            text = txt_file.read()
            text = re.sub(r"[\[].*?[\]]", "", text)
            
            sentences = pysbd.Segmenter(language="en").segment(text)
            print(f'# of sentences: {len(sentences)}')
            for sentence in sentences:
                sample_list.append([key,'"'+sentence.strip()+'"'])

    with open('virus_labelled_data.csv','w+',encoding='utf-8') as output_file:
        for sample in sample_list:
            output_file.write(sample[0]+','+sample[1]+'\n')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()