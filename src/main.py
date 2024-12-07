from flask import Flask, render_template, request, redirect

from .models import db, Character
from .utils import (
    check_character_connections,
    create_character_with_connections,
    reset_ammunition,
    reset_armor,
    reset_health_notes,
    reset_party_holdings,
    reset_party_ledger,
    reset_spells_and_prayers,
    reset_static,
    reset_trappings,
    reset_basic_skills,
    reset_attributes,
    reset_special_skills,
    reset_talents,
    reset_weapons,
    save_ammunition,
    save_attributes,
    save_basic_skills,
    save_health_notes,
    save_party_ledger,
    save_skills,
    save_static_data,
    save_talents,
    save_trappings,
    save_armor,
    save_weapons,
    save_spells_and_prayers,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CharSheet.db"
app.config["SECRET_KEY"] = "your_secret_key"  # Needed for flashing messages
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["new-name"]
        if not name:
            return redirect("/")
        elif not name.replace(" ", "").isalnum():
            return redirect("/")
        try:
            create_character_with_connections(db.session, name)
        except Exception as e:
            db.session.rollback()
            e.add_note("Error creating character")
            raise e
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
        app.logger.info("POST request received. saving data:")
        app.logger.info(request.form)
        app.logger.info("saving static data:")
        save_static_data(request.form, character, db)
        app.logger.info("saving trappings:")
        save_trappings(request.form, character, db) # no catch of errors in this method may result in site reloading with complete loss of data
        return redirect(f"/{id}/sheet-p1")
    else:
        return render_template("character_fluff_page.html", character=character)


@app.route("/<int:id>/sheet-p2", methods=["GET", "POST"])
def skills_and_talents(id):
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
        app.logger.info("saving basic skills:")
        save_basic_skills(request.form, character, db)
        app.logger.info("saving attributes:")
        save_attributes(request.form, character, db)
        app.logger.info("saving skills:")
        save_skills(request.form, character, db)
        app.logger.info("saving talents:")
        save_talents(request.form, character, db)
        return redirect(f"/{id}/sheet-p2")
    else:
        return render_template(
            "character_skills_talents_page.html", character=character
        )


@app.route("/<int:id>/sheet-p3", methods=["GET", "POST"])
def action_and_equipment(id):
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
        try:
            save_armor(request.form, character, db)
            save_weapons(request.form, character, db)
            save_spells_and_prayers(request.form, character, db)
            save_ammunition(request.form, character, db)
            save_health_notes(request.form, character, db)
        except Exception as e:
            app.logger.error(e)
        return redirect(f"/{id}/sheet-p3")
    else:
        return render_template("character_battle_page.html", character=character)


@app.route("/<int:id>/party-ledger", methods=["GET", "POST"])
def party_ledger(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    if request.method == "POST":
        app.logger.info("POST request received")
        app.logger.info(request.form)
        try:
            save_party_ledger(request.form, character, db)
        except Exception as e:
            app.logger.error(e)
        return redirect(f"/{id}/party-ledger")
    else:
        return render_template("party_ledger_page.html", character=character)


@app.route("/<int:id>/reset-p1")
def reset_description(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    app.logger.info("Resetting description...")
    if not reset_static(character, db):
        app.logger.error("Error resetting static data!!!")
    app.logger.info("Resetting trappings...")
    if not reset_trappings(character, db):
        app.logger.error("Error resetting trappings!!!")
    return redirect(f"/{id}/sheet-p1")


@app.route("/<int:id>/reset-p2")
def reset_skills_and_talents(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)
    
    app.logger.info("Resetting basic skills...")
    if not reset_basic_skills(character, db):
        app.logger.error("Error resetting basic skills!!!")
    app.logger.info("Resetting attributes...")
    if not reset_attributes(character, db):
        app.logger.error("Error resetting attributes!!!")
    app.logger.info("Resetting special skills...")
    if not reset_special_skills(character, db):
        app.logger.error("Error resetting special skills!!!")
    app.logger.info("Resetting talents...")
    if not reset_talents(character, db):
        app.logger.error("Error resetting talents!!!")
    return redirect(f"/{id}/sheet-p2")


@app.route("/<int:id>/reset-p3")
def reset_action(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    app.logger.info("Resetting ammunition...")
    if not reset_ammunition(character, db):
        app.logger.error("Error resetting ammunition!!!")
    app.logger.info("Resetting armor...")
    if not reset_armor(character, db):
        app.logger.error("Error resetting armor!!!")
    app.logger.info("Resetting weapons...")
    if not reset_weapons(character, db):
        app.logger.error("Error resetting weapons!!!")
    app.logger.info("Resetting spells and prayers...")
    if not reset_spells_and_prayers(character, db):
        app.logger.error("Error resetting spells and prayers!!!")
    app.logger.info("Resetting health notes...")
    if not reset_health_notes(character, db):
        app.logger.error("Error resetting health notes!!!")
    return redirect(f"/{id}/sheet-p3")


@app.route("/<int:id>/reset-ledger")
def reset_ledger(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    app.logger.info("Resetting party ledger...")
    if not reset_party_ledger(character, db):
        app.logger.error("Error resetting party ledger!!!")
    app.logger.info("Resetting party holding...")
    if not reset_party_holdings(character, db):
        app.logger.error("Error resetting party holding!!!")
    return redirect(f"/{id}/party-ledger")


@app.route("/<int:id>/delete")
def delete(id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == id)
    ).one_or_none()

    if character is None:
        app.logger.error("Character not found")
        return redirect("/")

    app.logger.info("Character found: " + character.name)

    try:
        db.session.delete(character)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
    return redirect("/")



