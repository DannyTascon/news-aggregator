# api.py
from flask import Blueprint
from flask_restful import Api, Resource
from .models import Article

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class ArticleResource(Resource):
    def get(self, id):
        article = Article.query.get(id)
        if article:
            return {'id': article.id, 'title': article.title, 'link': article.link}, 200
        else:
            return {'error': 'Article not found'}, 404

api.add_resource(ArticleResource, '/articles/<int:id>')

class ArticleListResource(Resource):
    def get(self):
        articles = Article.query.all()
        return [{'id': a.id, 'title': a.title, 'link': a.link} for a in articles], 200

api.add_resource(ArticleListResource, '/articles')

