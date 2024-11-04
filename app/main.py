from flask import Flask, render_template, request, redirect
from models import db, Character, TextFields, Party

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CharSheet.db"
db.init_app(app)


with app.app_context():
    # db.drop_all()  # Uncomment this line to drop all tables
    db.create_all()
    


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["new-name"]
        new_character = Character(name=name)
        try:
            db.session.add(new_character)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
        return redirect("/")
    else:
        characters = db.session.scalars(db.select(Character)).all()
        app.logger.info("Characters found: " + str(characters))
    return render_template("index.html", characters=characters)
    

@app.route("/<int:id>/sheet-p1", methods=["GET", "POST"])
def character(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
        ).one_or_none()
    text_fields = db.session.scalars(
        db.select(TextFields).where(TextFields.character_id == id)
        ).one_or_none()
    party = db.session.scalars(
        db.select(Party).where(Party.character_id == id)
        ).one_or_none()
    if text_fields is None:
        text_fields = TextFields(character_id=id)
        db.session.add(text_fields)
    if party is None:
        party = Party(character_id=id)
        db.session.add(party)
    
    app.logger.info("Character found: ")
    app.logger.info(character)
    app.logger.info("Character name: " + character.name)
    if request.method == "POST":
        app.logger.info("POST request received")
        app.logger.info(request.form)
        character.name = request.form["name"]
        character.species = request.form["species"]
        character.career = request.form["career"]
        character.status = request.form["status"]
        character.careerpath = request.form["careerpath"]
        character.age = request.form["age"]
        character.height = request.form["height"]
        character.hair = request.form["hair"]
        character.eyes = request.form["eyes"]
        character.gold = request.form["gold"]
        character.silver = request.form["silver"]
        character.brass = request.form["brass"]
        text_fields.psychology = request.form["psychology"]
        text_fields.short_term_ambition = request.form["short_term_ambition"]
        text_fields.long_term_ambition = request.form["long_term_ambition"]
        text_fields.doom = request.form["doom"]
        party.name = request.form["party_name"]
        party.members = request.form["party_members"]
        party.ambitions = request.form["party_ambitions"]
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
        return redirect(f"/{id}/sheet-p1")
    else:
        app.logger.info("Character found: " + str(character))
        return render_template("character_fluff_page.html", character=character, party=party, text_fields=text_fields)
   




if __name__ == "__main__":
    app.run(debug=True)
