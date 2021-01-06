import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
db = SQLAlchemy()
database_path = 'postgresql://postgres:77288399@localhost:5432/trivia'
def setup_db(app):
  app.config['SQLALCHEMY_DATABASE_URI'] = database_path 
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app=app 
  db.init_app(app)
  db.create_all()
  

class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    try:
      db.session.add(self)
      db.session.commit()
    except:
      db.session.rollback()
  
  def update(self):
    try:
      db.session.commit()
    except:
      db.session.rollback()

  def delete(self):
    try:
      db.session.delete(self)
      db.session.commit()
    except:
      db.session.rollback()


  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }


class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  name = Column(String)

  def __init__(self, name):
    self.name = name

  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }