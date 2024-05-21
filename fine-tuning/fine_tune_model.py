from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
from pprint import pprint
import random
import json

PRE_TRAIN_MODEL = 'all-MiniLM-L6-v2'
FINE_TUNED_MODEL = './fine-tuned-COMP-CON-all-MiniLM-L6-v2.mod'
PERCENT_TEST = 0.1
OUTLIER_JSON_FILE_PATH = 'fine_tuning_corrections.json'

# Define the model. Either from scratch of by loading a pre-trained model
model = SentenceTransformer(PRE_TRAIN_MODEL)

# Define your train examples. You need more than just two examples...
train_examples = []

#InputExample(texts=["My first sentence", "My second sentence"], label=0.8),
f = open(OUTLIER_JSON_FILE_PATH)
fine_tuning_data = json.load(f)

print(type(fine_tuning_data))
input()

for sample in fine_tuning_data['corrections']:
    
    input_example = InputExample(texts=[sample['sentence 1'], sample['sentence 1']], label=sample['similarity'])
    train_examples.append(input_example)
          
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
