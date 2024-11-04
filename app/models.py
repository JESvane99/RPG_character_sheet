from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50))
    career = db.Column(db.String(50))
    status = db.Column(db.Integer)
    careerpath = db.Column(db.String(50))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    hair = db.Column(db.String(50))
    eyes = db.Column(db.String(50))
    
    text_fields = db.relationship('TextFields', backref='Character.character_id')
    base_mechanics = db.relationship('BaseMechanics', backref='Character.character_id')    

    party = db.relationship('Party', backref='Character.character_id')

    gold = db.Column(db.Integer)
    silver = db.Column(db.Integer)
    brass = db.Column(db.Integer)
    
class BaseMechanics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    experience = db.Column(db.Integer)
    experience_spent = db.Column(db.Integer)
    movement = db.Column(db.Integer)
    fate_points = db.Column(db.Integer)
    fortune_points = db.Column(db.Integer)
    resilience = db.Column(db.Integer)
    resolve = db.Column(db.Integer)
    motivation = db.Column(db.Integer)

class TextFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    psychology = db.Column(db.String(500))
    health_notes = db.Column(db.String(200))
    short_term_ambition = db.Column(db.String(200))
    long_term_ambition = db.Column(db.String(200))
    doom = db.Column(db.String(500))

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    members = db.Column(db.String(500))
    ambitions = db.Column(db.String(200))

class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(50))
    base_value = db.Column(db.Integer)
    advances = db.Column(db.Integer)
    bonus = db.Column(db.Integer)


class BasicSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    base_value = db.Column(db.Integer)
    advances = db.Column(db.Integer)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    base_value = db.Column(db.Integer)
    advances = db.Column(db.Integer)


class Talent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    given_bonus = db.Column(db.Integer)
    bonus_attribute = db.Column(db.String(50))


class Armour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    encumbrance = db.Column(db.Integer)
    armour_points = db.Column(db.Integer)
    location = db.Column(db.String(50))
    qualities = db.Column(db.String(200))


class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    encumbrance = db.Column(db.Integer)
    range = db.Column(db.Integer)
    damage = db.Column(db.String(50))
    qualities = db.Column(db.String(200))


class Magic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    casting_number = db.Column(db.Integer)
    range = db.Column(db.String(50))
    target = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    effect = db.Column(db.String(50))


class Trapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100))
    encumbrance = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(500))


class Note(db.Model):
    id = db.Column(db.Integer)
    # character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(100), primary_key=True)
    note = db.Column(db.String(500))


# Similar structures can be created for Skill, Weapon, Armor, Talent, and Trapping
