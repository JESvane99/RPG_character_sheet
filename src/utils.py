from .models import (
    Ammunition,
    db,
    Character,
    BaseMechanics,
    TextFields,
    Party,
    Attributes,
    BasicSkill,
    Skill,
    Talent,
    Armor,  # Changed from Armour to Armor
    Weapon,
    Magic,
    Trapping,
    Ledger,
)


def log_this_find(app, find):
    if find:
        app.logger.info(f"Found {find.name}")
    else:
        app.logger.info(f"Could not find {find.name}")


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
        corruption=0,
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
        gold=0,
        silver=0,
        brass=0,
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
        {"name": "Charm", "attribute": "fel", "advances": 0},
        {"name": "Charm Animal", "attribute": "wp", "advances": 0},
        {"name": "Climb", "attribute": "s", "advances": 0},
        {"name": "Cool", "attribute": "wp", "advances": 0},
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
        {"name": "Leadership", "attribute": "fel", "advances": 0},
        {"name": "Melee (Basic)", "attribute": "ws", "advances": 0},
        {"name": "Navigation", "attribute": "int", "advances": 0},
        {"name": "Outdoor Survival", "attribute": "int", "advances": 0},
        {"name": "Perception", "attribute": "i", "advances": 0},
        {"name": "Ride", "attribute": "ag", "advances": 0},
        {"name": "Row", "attribute": "s", "advances": 0},
        {"name": "Stealth", "attribute": "ag", "advances": 0},
    ]

    for skill_data in basic_skills_data:
        skill = BasicSkill(character_id=new_character.id, **skill_data)
        session.add(skill)
        
    spells_and_prayers = Magic(character_id=new_character.id)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    return new_character

def attribute_case_adjustment(attribute):
    if attribute.lower() in ("ws", "bs", "wp"):
        return attribute.upper()
    return attribute.capitalize()

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
        character.armor,  # Changed from armours to armor
        character.weapons,
        character.spells_and_prayers,
        character.trappings,
    ]

    for connection in connections:
        if connection is None:
            return False
    return True


def save_static_data(form, character, db):
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
    character.base_mechanics.experience = form["experience"]
    character.base_mechanics.experience_spent = form["experience_spent"]
    character.base_mechanics.movement = form["movement"]
    character.base_mechanics.fate_points = form["fate_points"]
    character.base_mechanics.fortune_points = form["fortune_points"]
    character.base_mechanics.resilience = form["resilience"]
    character.base_mechanics.resolve = form["resolve"]
    character.base_mechanics.motivation = form["motivation"]
    character.text_fields.psychology = form["psychology"]
    character.text_fields.short_term_ambition = form["short_term_ambition"]
    character.text_fields.long_term_ambition = form["long_term_ambition"]
    character.text_fields.doom = form["doom"]
    character.text_fields.campaign_notes = form["notes"]
    character.party.name = form["party_name"]
    character.party.members = form["party_members"]
    character.party.ambitions = form["party_ambitions"]
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def save_basic_skills(form, character, db):
    for skill in character.basic_skills:
        skill_advances = form.get(f"{skill.name.lower()}-adv")
        if skill_advances is not None:
            skill.advances = int(skill_advances)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def save_attributes(form, character, db):
    attributes = character.attributes
    attributes.ws_base = int(form.get("ws-init", attributes.ws_base))
    attributes.ws_modifier = int(form.get("ws-adv", attributes.ws_modifier))
    attributes.ws_bonus = int(form.get("ws-bonus", attributes.ws_bonus))

    attributes.bs_base = int(form.get("bs-init", attributes.bs_base))
    attributes.bs_modifier = int(form.get("bs-adv", attributes.bs_modifier))
    attributes.bs_bonus = int(form.get("bs-bonus", attributes.bs_bonus))

    attributes.s_base = int(form.get("s-init", attributes.s_base))
    attributes.s_modifier = int(form.get("s-adv", attributes.s_modifier))
    attributes.s_bonus = int(form.get("s-bonus", attributes.s_bonus))

    attributes.t_base = int(form.get("t-init", attributes.t_base))
    attributes.t_modifier = int(form.get("t-adv", attributes.t_modifier))
    attributes.t_bonus = int(form.get("t-bonus", attributes.t_bonus))

    attributes.i_base = int(form.get("i-init", attributes.i_base))
    attributes.i_modifier = int(form.get("i-adv", attributes.i_modifier))
    attributes.i_bonus = int(form.get("i-bonus", attributes.i_bonus))

    attributes.ag_base = int(form.get("ag-init", attributes.ag_base))
    attributes.ag_modifier = int(form.get("ag-adv", attributes.ag_modifier))
    attributes.ag_bonus = int(form.get("ag-bonus", attributes.ag_bonus))

    attributes.dex_base = int(form.get("dex-init", attributes.dex_base))
    attributes.dex_modifier = int(form.get("dex-adv", attributes.dex_modifier))
    attributes.dex_bonus = int(form.get("dex-bonus", attributes.dex_bonus))

    attributes.int_base = int(form.get("int-init", attributes.int_base))
    attributes.int_modifier = int(form.get("int-adv", attributes.int_modifier))
    attributes.int_bonus = int(form.get("int-bonus", attributes.int_bonus))

    attributes.wp_base = int(form.get("wp-init", attributes.wp_base))
    attributes.wp_modifier = int(form.get("wp-adv", attributes.wp_modifier))
    attributes.wp_bonus = int(form.get("wp-bonus", attributes.wp_bonus))

    attributes.fel_base = int(form.get("fel-init", attributes.fel_base))
    attributes.fel_modifier = int(form.get("fel-adv", attributes.fel_modifier))
    attributes.fel_bonus = int(form.get("fel-bonus", attributes.fel_bonus))

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def save_trappings(form, character, db):
    for trap in character.trappings:
        trap.name = form.get(f"trappings_name_{trap.id}")
        trap.encumbrance = int(form.get(f"trappings_enc_{trap.id}") or 0) 
        trap.quantity = form.get(f"trappings_quantity_{trap.id}")
        trap.description = form.get(f"trappings_description_{trap.id}")
        if not trap.name:
            db.session.delete(trap)

    new_name = form.get("trappings_name_new")
    if new_name:
        new_encumbrance = int(form.get("trappings_enc_new") or 0)
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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def save_skills(form, character, db):
    for skill in character.skills:
        skill.name = form.get(f"skills_name_{skill.id}")
        skill.attribute = attribute_case_adjustment(
            form.get(f"skills_attribute_{skill.id}")
        )
        skill.advances = form.get(f"skills_advances_{skill.id}")
        if not skill.name:
            db.session.delete(skill)

    new_name = form.get("skills_name_new")
    if new_name:
        new_attribute = attribute_case_adjustment(
            form.get("skills_attribute_new").lower()
        )
        new_advances = form.get("skills_advances_new") or 0
        new_skill = Skill(
            character_id=character.id,
            name=new_name,
            attribute=new_attribute,
            advances=new_advances,
        )
        db.session.add(new_skill)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def save_talents(form, character, db):
    for talent in character.talents:
        talent.name = form.get(f"talents_name_{talent.id}")
        talent.description = form.get(f"talents_description_{talent.id}")
        talent.bonus_attribute = attribute_case_adjustment(
            form.get(f"talents_attribute_{talent.id}")
        )
        talent.given_bonus = form.get(f"talents_bonus_value_{talent.id}")
        talent.times_taken = form.get(f"talents_times_taken_{talent.id}")
        if not talent.name:
            db.session.delete(talent)

    new_name = form.get("talents_name_new")
    if new_name:
        new_description = form.get("talents_description_new")
        new_bonus_attribute = attribute_case_adjustment(
            form.get("talents_attribute_new")
        )
        new_bonus = form.get("talents_bonus_value_new")
        new_times_taken = form.get("talents_times_taken_new")
        new_talent = Talent(
            character_id=character.id,
            name=new_name,
            description=new_description,
            given_bonus=new_bonus,
            bonus_attribute=new_bonus_attribute,
            times_taken=new_times_taken,
        )
        db.session.add(new_talent)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def save_armor(form, character, db):
    for armor in character.armor:
        armor.name = form.get(f"armor_name_{armor.id}")
        armor.encumbrance = int(form.get(f"armor_encumbrance_{armor.id}") or 0)
        armor.armor_points = form.get(f"armor_points_{armor.id}")
        armor.location = form.get(f"armor_location_{armor.id}")
        armor.qualities = form.get(f"armor_qualities_{armor.id}")
        if not armor.name:
            db.session.delete(armor)

    new_name = form.get("armor_name_new")
    if new_name:
        new_encumbrance = int(form.get("armor_encumbrance_new") or 0)
        new_armor_points = form.get("armor_points_new")
        new_location = form.get("armor_location_new")
        new_qualities = form.get("armor_qualities_new")
        new_armor = Armor(
            character_id=character.id,
            name=new_name,
            encumbrance=new_encumbrance,
            armor_points=new_armor_points,
            location=new_location,
            qualities=new_qualities,
        )
        db.session.add(new_armor)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def save_weapons(form, character, db):
    for weapon in character.weapons:
        weapon.name = form.get(f"weapon_name_{weapon.id}")
        weapon.encumbrance = int(form.get(f"weapon_encumbrance_{weapon.id}") or 0)
        weapon.range = form.get(f"weapon_range_{weapon.id}")
        weapon.damage = form.get(f"weapon_damage_{weapon.id}")
        weapon.qualities = form.get(f"weapon_qualities_{weapon.id}")
        if not weapon.name:
            db.session.delete(weapon)

    new_name = form.get("weapon_name_new")
    if new_name:
        new_encumbrance = int(form.get("weapon_encumbrance_new") or 0)
        new_range = form.get("weapon_range_new")
        new_damage = form.get("weapon_damage_new")
        new_qualities = form.get("weapon_qualities_new")
        new_weapon = Weapon(
            character_id=character.id,
            name=new_name,
            encumbrance=new_encumbrance,
            range=new_range,
            damage=new_damage,
            qualities=new_qualities,
        )
        db.session.add(new_weapon)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def save_spells_and_prayers(form, character, db):
    for spell in character.spells_and_prayers:
        spell.name = form.get(f"spell_name_{spell.id}")
        spell.casting_number = form.get(f"spell_cn_{spell.id}")
        spell.range = form.get(f"spell_range_{spell.id}")
        spell.target = form.get(f"spell_target_{spell.id}")
        spell.duration = form.get(f"spell_duration_{spell.id}")
        spell.effect = form.get(f"spell_effect_{spell.id}")
        if not spell.name:
            db.session.delete(spell)

    new_name = form.get("spell_name_new")
    if new_name:
        new_casting_number = form.get("spell_cn_new")
        new_range = form.get("spell_range_new")
        new_target = form.get("spell_target_new")
        new_duration = form.get("spell_duration_new")
        new_effect = form.get("spell_effect_new")
        new_spell = Magic(
            character_id=character.id,
            name=new_name,
            casting_number=new_casting_number,
            range=new_range,
            target=new_target,
            duration=new_duration,
            effect=new_effect,
        )
        db.session.add(new_spell)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def save_ammunition(form, character, db):
    for ammo in character.ammunition:
        ammo.name = form.get(f"ammo_name_{ammo.id}")
        ammo.quantity = form.get(f"ammo_quantity_{ammo.id}")
        ammo.qualities = form.get(f"ammo_qualities_{ammo.id}")
        if not ammo.name:
            db.session.delete(ammo)

    new_name = form.get("ammo_name_new")
    if new_name:
        new_quantity = form.get("ammo_quantity_new")
        new_qualities = form.get("ammo_qualities_new")
        new_ammo = Ammunition(
            character_id=character.id,
            name=new_name,
            quantity=new_quantity,
            qualities=new_qualities,
        )
        db.session.add(new_ammo)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    

def save_health_notes(form, character, db):
    character.text_fields.health_notes = form.get("combat_health_notes")
    character.base_mechanics.corruption = form.get("corruption")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def calculate_party_holdings(character, db):
    total_gold = 0
    total_silver = 0
    total_brass = 0
    for entry in character.ledger:
        total_gold += entry.gold
        total_silver += entry.silver
        total_brass += entry.brass
        
    character.party.gold = total_gold
    character.party.silver = total_silver
    character.party.brass = total_brass
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
def save_party_ledger(form, character, db):
    for entry in character.ledger:
        entry.who = form.get(f"who_{entry.id}")
        entry.what = form.get(f"what_{entry.id}")
        entry.gold = int(form.get(f"gold_{entry.id}") or 0)
        entry.silver = int(form.get(f"silver_{entry.id}") or 0)
        entry.brass = int(form.get(f"brass_{entry.id}") or 0)
        if not entry.who or not entry.what:
            db.session.delete(entry)

    new_who = form.get("who_new")
    new_what = form.get("what_new")
    new_gold = int(form.get("gold_new") or 0)
    new_silver = int(form.get("silver_new") or 0)
    new_brass = int(form.get("brass_new") or 0)
    if new_who and new_what:
        new_entry = Ledger(
            character_id=character.id,
            who=new_who,
            what=new_what,
            gold=new_gold,
            silver=new_silver,
            brass=new_brass,
        )
        db.session.add(new_entry)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    
    calculate_party_holdings(character, db)
    
    
def reset_static(character, db):
    character.species = ""
    character.career = ""
    character.status = 0
    character.careerpath = ""
    character.age = 0
    character.height = 0
    character.hair = ""
    character.eyes = ""
    character.gold = 0
    character.silver = 0
    character.brass = 0
    character.base_mechanics.experience = 0
    character.base_mechanics.experience_spent = 0
    character.base_mechanics.movement = 0
    character.base_mechanics.fate_points = 0
    character.base_mechanics.fortune_points = 0
    character.base_mechanics.resilience = 0
    character.base_mechanics.resolve = 0
    character.base_mechanics.motivation = 0
    character.text_fields.psychology = ""
    character.text_fields.short_term_ambition = ""
    character.text_fields.long_term_ambition = ""
    character.text_fields.doom = ""
    character.text_fields.campaign_notes = ""
    character.party.name = ""
    character.party.members = ""
    character.party.ambitions = ""
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True

def reset_trappings(character, db):
    for trap in character.trappings:
        db.session.delete(trap)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_basic_skills(character, db):
    for skill in character.basic_skills:
        skill.advances = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True

def reset_attributes(character, db):
    attrs = [
        "ws",
        "bs",
        "s",
        "t",
        "i",
        "ag",
        "dex",
        "int",
        "wp",
        "fel",
    ]
    
    for attr in attrs:
        setattr(character.attributes, f"{attr}_base", 0)
        setattr(character.attributes, f"{attr}_modifier", 0)
        setattr(character.attributes, f"{attr}_bonus", 0)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True

def reset_special_skills(character, db):
    for skill in character.skills:
        db.session.delete(skill)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True

def reset_talents(character, db):
    for talent in character.talents:
        db.session.delete(talent)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True
    

def reset_ammunition(character, db):
    for ammo in character.ammunition:
        db.session.delete(ammo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_armor(character, db):
    for armor in character.armor:
        db.session.delete(armor)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_weapons(character, db):
    for weapon in character.weapons:
        db.session.delete(weapon)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_spells_and_prayers(character, db):
    for spell in character.spells_and_prayers:
        db.session.delete(spell)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_health_notes(character, db):
    character.text_fields.health_notes = ""
    character.base_mechanics.corruption = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_party_ledger(character, db):
    for entry in character.ledger:
        db.session.delete(entry)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True


def reset_party_holdings(character, db):
    character.party.gold = 0
    character.party.silver = 0
    character.party.brass = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return True