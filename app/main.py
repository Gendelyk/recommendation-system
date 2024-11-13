import logging
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.embeddings import EmbeddingModel
from app.models.recommender import Recommender

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація FastAPI
app = FastAPI()

# Завантаження даних з CSV файлу
data_path = 'app/data/r_dataisbeautiful_posts.csv'
df = pd.read_csv(data_path, low_memory=False)

# Перевірка назв стовпців
print(df.columns)

# Ініціалізація моделі ембеддінгів
embedding_model = EmbeddingModel(df)

# Ініціалізація рекомендаційної системи
recommender = Recommender(embedding_model)

# Моделі запитів
class SearchRequest(BaseModel):
    user_id: int
    query: str

class RecommendationRequest(BaseModel):
    user_id: int
    article_id: int

# Ендпоїнти
@app.post("/search")
async def search_articles(request: SearchRequest):
    results = recommender.search_articles(request.query)
    if results.empty:
        raise HTTPException(status_code=404, detail="Статті не знайдено.")
    return results.to_dict(orient='records')

@app.post("/recommend")
async def recommend_articles(request: RecommendationRequest):
    results = recommender.recommend_similar_articles(request.article_id)
    if results.empty:
        raise HTTPException(status_code=404, detail="Рекомендацій не знайдено.")
    return results.to_dict(orient='records')
