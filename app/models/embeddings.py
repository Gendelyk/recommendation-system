import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import logging

class EmbeddingModel:
    def __init__(self, df):
        self.df = df
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = None
        self.index = None
        self.initialize_embeddings()

    def initialize_embeddings(self):
        # Шлях до директорії для збереження ембеддінгів та індексу
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        embeddings_path = os.path.join(data_dir, 'embeddings.pkl')
        index_path = os.path.join(data_dir, 'faiss_index.index')

        text_column = 'title'  # Переконайтеся, що назва стовпця правильна

        # Видаляємо рядки з NaN та скидаємо індекси
        self.df = self.df.dropna(subset=[text_column]).reset_index(drop=True)

        if os.path.exists(embeddings_path) and os.path.exists(index_path):
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            self.index = faiss.read_index(index_path)
            logging.info("Завантажено ембеддінги та індекс з диску.")
        else:
            logging.info("Генерація нових ембеддінгів...")
            sentences = self.df[text_column].astype(str).tolist()
            self.embeddings = self.model.encode(sentences, show_progress_bar=True)
            with open(embeddings_path, 'wb') as f:
                pickle.dump(self.embeddings, f)
            embeddings_np = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(embeddings_np.shape[1])
            self.index.add(embeddings_np)
            faiss.write_index(self.index, index_path)
            logging.info("Ембеддінги та індекс збережено на диск.")