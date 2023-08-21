from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Research(db.Model, SerializerMixin):
    __tablename__ = "researches"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    authors = db.relationship("Author", secondary="research_authors", back_populates="researches")
    serialize_rules = ('-authors','-created_at', '-updated_at',)

    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) != 4:
            raise ValueError("Year must be greater tahn four digits")
        return year

class Author(db.Model, SerializerMixin):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    researches = db.relationship("Research", secondary="research_authors", back_populates="authors")
    serialize_rules = ('-researches','-created_at', '-updated_at',)

    @validates("field_of_study")
    def validate_field(self, key, field_of_study):
        fields = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if field_of_study not in fields:
            raise ValueError("Field of study must be in the list of fields")
        return field_of_study
    

class ResearchAuthors(db.Model):
    __tablename__ = "research_authors"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    research_id = db.Column(db.Integer, db.ForeignKey("researches.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


