from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
from pprint import pprint
import random

PRE_TRAIN_MODEL = 'all-MiniLM-L6-v2'
TRAIN_DATA_FILE_PATH = 'training_data/COMP_CON_SOC_ENV/COMP_CON_fine_tuning.csv'
FINE_TUNED_MODEL = './fine-tuned-COMP-CON-all-MiniLM-L6-v2.mod'
PERCENT_TEST = 0.1

# Define the model. Either from scratch of by loading a pre-trained model
model = SentenceTransformer(PRE_TRAIN_MODEL)

# Define your train examples. You need more than just two examples...
train_examples = []

#InputExample(texts=["My first sentence", "My second sentence"], label=0.8),
with open(TRAIN_DATA_FILE_PATH, 'r') as training_data_file:
    for line in training_data_file.readlines():
        line_split = line.split('^')

        if len(line_split)==3:
            input_example = InputExample(texts=[line_split[0], line_split[1]], label=float(line_split[2].strip()))
            train_examples.append(input_example)
            
training_data_file.close()  
 
random.shuffle(train_examples)

TEST_INDEX = int(len(train_examples)*PERCENT_TEST)
print(TEST_INDEX)
print(len(train_examples))

sentences1 = []
sentences2 = []
scores = []

for item in train_examples[:TEST_INDEX]:
    sentences1.append(item.texts[0])
    sentences2.append(item.texts[1])
    scores.append(item.label)

evaluator = evaluation.EmbeddingSimilarityEvaluator(sentences1, sentences2, scores)

# Define your train dataset, the dataloader and the train loss
train_dataloader = DataLoader(train_examples[TEST_INDEX:], shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

# Tune the model
model.fit(train_objectives=[(train_dataloader, train_loss)], 
          epochs=1, 
          warmup_steps=100,
          save_best_model=True,
          output_path=FINE_TUNED_MODEL,
          show_progress_bar=True,
          evaluator=evaluator,
          evaluation_steps=500)
