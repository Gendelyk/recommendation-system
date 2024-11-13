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

    def recommend_by_title(self, title, top_n=3):
        try:
            logging.info(f"Start finding for {title}")
            query_embedding = self.model.encode([title])
            distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_n + 1)
            indices = indices[0]
            distances = distances[0]
            results = self.df.iloc[indices].copy()
            results = results[results['title'] != title]
            results = results.head(top_n)
            results['distance'] = distances[:len(results)]
            logging.info(f"Find {len(results)} recs.")
            return results.reset_index(drop=True)
        except Exception as e:
            logging.error(f"Error: {e}")
            return pd.DataFrame()
