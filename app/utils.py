from models import (
    db,
    Character,
    BaseMechanics,
    TextFields,
    Party,
    Attributes,
    BasicSkill,
    Skill,
    Talent,
    Armour,
    Weapon,
    Magic,
    Trapping,
)


def log_this_find(app, find):
    if find:
        app.logger.info(f"Found {find.name}")
    else:
        app.logger.info(f"Could not find {find.name}")


def upsert(session, app, table, data):
    pass
    # try:
    #     table.get
    #     session.execute(stmt)
    #     session.commit()
    # except Exception as e:
    #     session.rollback()
    #     app.logger.error(e)


def create_character_with_connections(session, name):
    new_character = Character(name=name)
    new_character.species = ""
    new_character.career = ""
    new_character.status = 0
    new_character.careerpath = ""
    new_character.age = 0
    new_character.height = 0
    new_character.hair = ""
    new_character.eyes = ""
    new_character.gold = 0
    new_character.silver = 0
    new_character.brass = 0
    session.add(new_character)
    session.flush()  # Ensure new_character.id is available

    new_base_mechanics = BaseMechanics(
        character_id=new_character.id,
        experience=0,
        experience_spent=0,
        movement=0,
        fate_points=0,
        fortune_points=0,
        resilience=0,
        resolve=0,
        motivation=0,
    )
    new_text_fields = TextFields(
        character_id=new_character.id,
        psychology="",
        health_notes="",
        short_term_ambition="",
        long_term_ambition="",
        doom="",
        campaign_notes="",
    )
    new_party = Party(
        character_id=new_character.id,
        name="",
        members="",
        ambitions="",
    )
    new_attributes = Attributes(
        character_id=new_character.id,
        ws_base=0,
        ws_modifier=0,
        ws_bonus=0,
        bs_base=0,
        bs_modifier=0,
        bs_bonus=0,
        s_base=0,
        s_modifier=0,
        s_bonus=0,
        t_base=0,
        t_modifier=0,
        t_bonus=0,
        i_base=0,
        i_modifier=0,
        i_bonus=0,
        ag_base=0,
        ag_modifier=0,
        ag_bonus=0,
        dex_base=0,
        dex_modifier=0,
        dex_bonus=0,
        int_base=0,
        int_modifier=0,
        int_bonus=0,
        wp_base=0,
        wp_modifier=0,
        wp_bonus=0,
        fel_base=0,
        fel_modifier=0,
        fel_bonus=0,
    )

    session.add(new_base_mechanics)
    session.add(new_text_fields)
    session.add(new_party)
    session.add(new_attributes)

    # Add default basic skills
    basic_skills_data = [
        {"name": "Art", "attribute": "dex", "advances": 0},
        {"name": "Athletics", "attribute": "ag", "advances": 0},
        {"name": "Bribery", "attribute": "fel", "advances": 0},
        {"name": "Charm", "attribute": "fel", "advances": 5},
        {"name": "Charm Animal", "attribute": "wp", "advances": 10},
        {"name": "Climb", "attribute": "s", "advances": 0},
        {"name": "Cool", "attribute": "wp", "advances": 5},
        {"name": "Consume Alcohol", "attribute": "t", "advances": 0},
        {"name": "Dodge", "attribute": "ag", "advances": 0},
        {"name": "Drive", "attribute": "ag", "advances": 0},
        {"name": "Endurance", "attribute": "t", "advances": 0},
        {"name": "Entertain", "attribute": "fel", "advances": 0},
        {"name": "Gamble", "attribute": "int", "advances": 0},
        {"name": "Gossip", "attribute": "fel", "advances": 0},
        {"name": "Haggle", "attribute": "fel", "advances": 0},
        {"name": "Intimidate", "attribute": "s", "advances": 0},
        {"name": "Intuition", "attribute": "i", "advances": 0},
        {"name": "Leadership", "attribute": "fel", "advances": 3},
        {"name": "Melee (Basic)", "attribute": "ws", "advances": 15},
        {"name": "Navigation", "attribute": "int", "advances": 0},
        {"name": "Outdoor Survival", "attribute": "int", "advances": 0},
        {"name": "Perception", "attribute": "i", "advances": 2},
        {"name": "Ride", "attribute": "ag", "advances": 0},
        {"name": "Row", "attribute": "s", "advances": 0},
        {"name": "Stealth", "attribute": "ag", "advances": 0},
    ]

    for skill_data in basic_skills_data:
        skill = BasicSkill(character_id=new_character.id, **skill_data)
        session.add(skill)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return new_character


def check_character_connections(character_id):
    character = db.session.scalars(
        db.select(Character).where(Character.id == character_id)
    ).one_or_none()
    if not character:
        return False

    connections = [
        character.base_mechanics,
        character.text_fields,
        character.party,
        character.attributes,
        character.basic_skills,
        character.skills,
        character.talents,
        character.armours,
        character.weapons,
        character.magics,
        character.trappings,
    ]

    for connection in connections:
        if connection is None:
            return False
    return True


def save_static_data(form, character, app):
    app.logger.info(f"saving static data for {character.name}")
    character.name = form["name"]
    character.species = form["species"]
    character.career = form["career"]
    character.status = form["status"]
    character.careerpath = form["careerpath"]
    character.age = form["age"]
    character.height = form["height"]
    character.hair = form["hair"]
    character.eyes = form["eyes"]
    character.gold = form["gold"]
    character.silver = form["silver"]
    character.brass = form["brass"]
    character.text_fields.psychology = form["psychology"]
    character.text_fields.short_term_ambition = form["short_term_ambition"]
    character.text_fields.long_term_ambition = form["long_term_ambition"]
    character.text_fields.doom = form["doom"]
    character.party.name = form["party_name"]
    character.party.members = form["party_members"]
    character.party.ambitions = form["party_ambitions"]


def save_basic_skills(form, character):
    pass


def save_attributes(form, character):
    pass


def save_trappings(form, character, db):
    for trap in character.trappings:
        trap.name = form.get(f"trappings_name_{trap.id}")
        trap.encumbrance = form.get(f"trappings_enc_{trap.id}")
        trap.quantity = form.get(f"trappings_quantity_{trap.id}")
        trap.description = form.get(f"trappings_description_{trap.id}")
        if not trap.name:
            db.session.delete(trap)

    new_name = form.get("trappings_name_new")
    if new_name:
        new_encumbrance = form.get("trappings_enc_new")
        new_quantity = form.get("trappings_quantity_new")
        new_description = form.get("trappings_description_new")
        new_trapping = Trapping(
            character_id=character.id,
            name=new_name,
            encumbrance=new_encumbrance,
            quantity=new_quantity,
            description=new_description,
        )
        db.session.add(new_trapping)

    db.session.commit()


def save_listed_data(table_to_write, form, character, database, app):
    table_mapping = {
        "basic_skills": BasicSkill,
        "skills": Skill,
        "talents": Talent,
        "armours": Armour,
        "weapons": Weapon,
        "magics": Magic,
        "trappings": Trapping,
    }
    table_to_write = table_to_write.lower()
    if table_to_write not in table_mapping:
        app.logger.error(f"Invalid table name: {table_to_write}")
        return

    app.logger.info(f"saving listed data for {character.name}")
    new_row = {}
    for key, value in form.items():
        if key != table_to_write:
            continue
        row_id = key.split("_")[-1]
        row_key = key.split("_")[1]
        if row_id == "new":
            new_row[row_key] = value
        else:
            row = db.session.scalars(
                db.select(table_mapping[table_to_write])
                .where(table_mapping[table_to_write].id == row_id)
                .where(table_mapping[table_to_write].character_id == character.id)
            ).one_or_none()
            if row:
                current_value = getattr(row, row_key)
                if value != current_value:
                    app.logger.info(
                        f"changing {row_key} from {current_value} to {value}"
                    )
                setattr(row, row_key, value)
            else:
                app.logger.error(f"Could not find row {row_id} in {table_to_write}")
    if new_row:
        new_row = table_mapping[table_to_write](character_id=character.id, **new_row)
        database.session.add(new_row)
        app.logger.info(f"Adding new row to {table_to_write}")
        try:
            database.session.commit()
        except Exception as e:
            database.session.rollback()
            app.logger.error(e)
