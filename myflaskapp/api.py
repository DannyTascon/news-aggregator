# api.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from .models import Article
from . import db
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class ArticleListResource(Resource):
    def get(self):
        articles = Article.query.all()
        return jsonify([e.serialize() for e in articles])
    
    def post(self):
        data = request.get_json()
        new_article = Article(
            title=data.get('title'),
            link=data.get('link'),
            description=data.get('description'),
            category=data.get('category')
        )
        db.session.add(new_article)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "An article with the same title or link already exists."}, 400
        return {"message": "New article added."}, 201

class ArticleResource(Resource):
    def get(self, id):
        article = Article.query.get_or_404(id)
        return jsonify(article.serialize())
    
    def put(self, id):
        article = Article.query.get_or_404(id)
        data = request.get_json()
        article.title = data.get('title', article.title)
        article.link = data.get('link', article.link)
        article.description = data.get('description', article.description)
        article.category = data.get('category', article.category)
        db.session.commit()
        return {"message": "Article updated."}, 200
    
    def delete(self, id):
        article = Article.query.get_or_404(id)
        db.session.delete(article)
        db.session.commit()
        return {"message": "Article deleted."}, 204

api.add_resource(ArticleListResource, '/api/articles')
api.add_resource(ArticleResource, '/api/articles/<int:id>')


