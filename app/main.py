import logging
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.embeddings import EmbeddingModel
from app.models.recommender import Recommender
from app.database.db_connection import get_db_engine, get_session, init_db
from app.database.models import PostEntity, UserEntity, CategoryEntity

# SETUP logger
logging.basicConfig(level=logging.INFO)

# Init FastAPI
app = FastAPI()

# DB connection
db_engine = get_db_engine()
init_db(db_engine)  # init db
session = get_session(db_engine)

category = session.query(CategoryEntity).filter_by(id=1).first()
if not category:
    category = CategoryEntity(id=1)
    session.add(category)
    session.commit()

author = session.query(UserEntity).filter_by(id=1).first()
if not author:
    author = UserEntity(id=1)
    session.add(author)
    session.commit()

# get data
query = session.query(PostEntity).filter(PostEntity.title != None, PostEntity.status == 'active')
df = pd.read_sql(query.statement, session.bind)

if df.empty:
    logging.error("post_entity` is empty")
    raise Exception("No data")

# Ініціалізація моделі ембеддінгів
embedding_model = EmbeddingModel(df)

# Ініціалізація рекомендаційної системи
recommender = Recommender(embedding_model)

# Модель запиту
class RecommendationRequest(BaseModel):
    user_id: int
    title: str
    quantity: int = 3  # default number of recs

# endpoint
@app.post("/recommend")
async def recommend_articles(request: RecommendationRequest):
    logging.info(f"Request for recs: {request}")
    results = recommender.recommend_by_title(request.title, top_n=request.quantity)
    if results.empty:
        logging.warning("Recommendation is empty")
        raise HTTPException(status_code=404, detail="Unable to find recommendation")
    return results.to_dict(orient='records')

# is works
@app.get("/")
async def read_root():
    return {"message": "All is working well"}

# simple endpoint
@app.post("/search")
def search_posts(query: str, quantity: int = 5):
    results = session.query(PostEntity).filter(PostEntity.title.ilike(f"%{query}%")).limit(quantity).all()
    return {"results": [{"id": post.id, "title": post.title} for post in results]}
