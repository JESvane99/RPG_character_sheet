from flask import Flask, render_template, request, redirect
from models import db, Character, TextFields, Party
from utils import check_character_connections, create_character_with_connections

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CharSheet.db"
app.config["SECRET_KEY"] = "your_secret_key"  # Needed for flashing messages
db.init_app(app)

with app.app_context():
    # db.drop_all()  # Uncomment this line to drop all tables
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["new-name"]
        try:
            create_character_with_connections(db.session, name)
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
        return redirect("/")
    else:
        characters = db.session.scalars(db.select(Character)).all()
        app.logger.info("Characters found: " + str(characters))
    return render_template("index.html", characters=characters)


@app.route("/<int:id>/sheet-p1", methods=["GET", "POST"])
def character_page(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    if not check_character_connections(id):
        app.logger.error("Character connections not found")
        return redirect("/")

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
        character.text_fields.psychology = request.form["psychology"]
        character.text_fields.short_term_ambition = request.form["short_term_ambition"]
        character.text_fields.long_term_ambition = request.form["long_term_ambition"]
        character.text_fields.doom = request.form["doom"]
        character.party.name = request.form["party_name"]
        character.party.members = request.form["party_members"]
        character.party.ambitions = request.form["party_ambitions"]
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
        return redirect(f"/{id}/sheet-p1")
    else:
        app.logger.info("Character found: " + str(character))
        return render_template("character_fluff_page.html", character=character)


if __name__ == "__main__":
    print("----- run app -----")
    app.run(debug=True)

    print("----- stop app -----")
    with app.app_context():
        db.drop_all()  # Uncomment this line to drop all tables
        print("tables dropped")
