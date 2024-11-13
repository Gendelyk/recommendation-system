import numpy as np
import logging
import pandas as pd

class Recommender:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.df = embedding_model.df
        self.model = embedding_model.model
        self.embeddings = embedding_model.embeddings
        self.index = embedding_model.index

    def search_articles(self, query, top_n=3):
        try:
            query_embedding = self.model.encode([query])
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_n)
            results = self.df.iloc[indices[0]].copy()
            results['distance'] = distances[0]
            return results.reset_index(drop=True)
        except Exception as e:
            logging.error(f"Помилка під час пошуку: {e}")
            return pd.DataFrame()

    def recommend_similar_articles(self, article_id, top_n=3):
        try:
            # Знаходимо позицію статті в DataFrame
            article_idx = self.df[self.df['id'] == article_id].index
            if len(article_idx) == 0:
                logging.error(f"Статтю з ID {article_id} не знайдено.")
                return pd.DataFrame()
            article_idx = article_idx[0]
            distances, indices = self.index.search(self.embeddings[article_idx].reshape(1, -1), top_n + 1)
            # Виключаємо саму статтю
            indices = indices[0][1:]
            distances = distances[0][1:]
            results = self.df.iloc[indices].copy()
            results['distance'] = distances
            return results.reset_index(drop=True)
        except Exception as e:
            logging.error(f"Помилка під час рекомендації: {e}")
            return pd.DataFrame()

