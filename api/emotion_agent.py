from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class EmotionAgent:
    def __init__(self):
        self.pipeline = None

    def train(self, texts, labels):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])
        self.pipeline.fit(texts, labels)

    def predict_emotion(self, text):
        prediction = self.pipeline.predict([text])[0]
        proba = max(self.pipeline.predict_proba([text])[0])
        return prediction, proba