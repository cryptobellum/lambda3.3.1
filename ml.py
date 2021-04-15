from sklearn.linear_model import LogisticRegression
from data_model import User
import numpy as np
import spacy
import pandas as pd

transformer = spacy.load('my_model')


def predict_most_likely_author(text, possible_authors):

    df_dataset = pd.DataFrame()

    for i, author in enumerate(possible_authors):
        author = User.query.filter(User.name == author).one()
        author_features = np.array([transformer(tweet.text).vector for tweet in author.tweets])
        author_target = np.zeros(len(author.tweets)) + i
        author_dataset = pd.DataFrame(author_features)
        author_dataset['target'] = author_target
        df_dataset = pd.concat([df_dataset, author_dataset])

    model = LogisticRegression()
    model.fit(df_dataset[[c for c in df_dataset.columns if not c is 'target']], df_dataset['target'])
    most_likely_author_index = model.predict([transformer(text).vector])[0]

    return possible_authors[int(most_likely_author_index)]