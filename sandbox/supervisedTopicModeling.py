from sklearn.datasets import fetch_20newsgroups
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.dimensionality import BaseDimensionalityReduction
from sklearn.linear_model import LogisticRegression


# Get labeled data
print('Get Data')
data = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))
docs = data['data']
y = data['target']

print(f'data: {type(data)}')
print(f'docs: {type(docs)}')
print(f'y: {type(y)}')

print(f'# of docs: {len(docs)}')
print(f'len of y: {len(y)}')

# Skip over dimensionality reduction, 
# Replace cluster model with classifier,
# Reduce frequent words 
empty_dimensionality_model = BaseDimensionalityReduction()
clf = LogisticRegression()
ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

# Create a fully supervised BERTopic instance
print('Create instance of BERTopic')
topic_model= BERTopic(  umap_model=empty_dimensionality_model,
                        hdbscan_model=clf,
                        ctfidf_model=ctfidf_model)

# train the model
print('Fit Transform')
topics, probs = topic_model.fit_transform(docs, y=y)

print(topics)
print(probs)

print('Test')
topic, _ = topic_model.transform("this is a document about cars")
result = topic_model.get_topic(topic)

print(type(result))
print(result)
