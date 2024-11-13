from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CategoryEntity(Base):
    __tablename__ = 'category_entity'
    id = Column(Integer, primary_key=True)

class UserEntity(Base):
    __tablename__ = 'user_entity'
    id = Column(Integer, primary_key=True)

class PostEntity(Base):
    __tablename__ = 'post_entity'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    body = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Enum('active', 'inactive', name='post_entity_status_enum'), nullable=False, server_default='active')
