#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Researches(Resource):

    def get(self):
        research_list = [r.to_dict() for r in Research.query.all()]

        response = make_response(research_list,200)

        return response
    
class ResearchesID(Resource):
    def get(self, id):
        research_list = Research.query.filter_by(id = id).first()

        if not research_list:
            return {"error": "Research paper not found"}
        
        l = research_list.to_dict()
        l["authors"] = [author.to_dict() for author in research_list.authors]
        response = make_response(jsonify(l), 200)

        return response
    
    def delete(self, id):
        research_list = Research.query.filter_by(id = id).first()

        if not research_list:
            return {"error": "Research paper not found"}
        
        authors_list = ResearchAuthors.query.filter_by(id=id).first()
        db.session.delete(authors_list)
        db.session.commit()
        db.session.delete(research_list)
        db.session.commit()

        response = make_response("", 204)
        return response 
    
class Authors(Resource):
    def get(self):
        author_list = [a.to_dict() for a in Author.query.all()]

        response = make_response(author_list, 200)
        return response
    
class ResearchAuthor(Resource):

    def post(self):
        form_json = request.get_json()

        new_research = ResearchAuthors(
            author_id = form_json["author_id"],
            research_id = form_json["research_id"]
        )

        research = Research.query.get(form_json['research_id'])
        author = Author.query.get(form_json['author_id'])

        if not research or not author:
            return {"errors": ["validation errors"]}
        
        db.session.add(new_research)
        db.session.commit()

        response = make_response(author.to_dict(), 200)

        return response
  
api.add_resource(Researches, '/research')
api.add_resource(ResearchesID, '/research/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(ResearchAuthor, '/research_author')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
