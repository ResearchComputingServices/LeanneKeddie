from bertopic import BERTopic

from ProcessedDocument import ProcessedDocument

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def action_classify(cl_args_dict : dict) -> None:
    
    topic_model = BERTopic.load(cl_args_dict['load'])
    
    doc = ProcessedDocument(cl_args_dict['docs'])
        
    found_topics = []
    for sentence in doc.sentences:
        topic, _ = topic_model.transform(sentence.sentence_text)
                       
        sentence.assigned_topic = topic[0]
                       
        if 0 not in topic:
            found_topics.append(sentence.sentence_text)

    topic_distr, topic_token_distr = topic_model.approximate_distribution(  doc.get_sentences(),
                                                                            min_similarity=0.05,
                                                                            window=8,
                                                                            calculate_tokens=True)
    
    for i,row in enumerate(topic_distr):
        current_sentence = doc.sentences[i]

        current_sentence.topic_confidences = {j : conf for j,conf in enumerate(row)}    
    
    doc.save_csv('./processed_doc.txt')
