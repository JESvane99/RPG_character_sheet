from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Character(db.Model):
    """Character model
    contains a full character sheet
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    species: Mapped[str]
    career: Mapped[str]
    status: Mapped[int]
    careerpath: Mapped[str]
    age: Mapped[int]
    height: Mapped[int]
    hair: Mapped[str]
    eyes: Mapped[str]

    gold: Mapped[int]
    silver: Mapped[int]
    brass: Mapped[int]

    base_mechanics: Mapped["BaseMechanics"] = db.relationship(
        cascade="all, delete-orphan", back_populates="character", uselist=False
    )
    text_fields: Mapped["TextFields"] = db.relationship(
        cascade="all, delete-orphan", back_populates="character", uselist=False
    )
    party: Mapped["Party"] = db.relationship(
        cascade="all, delete-orphan", back_populates="character", uselist=False
    )
    attributes: Mapped["Attributes"] = db.relationship(
        cascade="all, delete-orphan", back_populates="character", uselist=False
    )
    basic_skills: Mapped[list["BasicSkill"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    skills: Mapped[list["Skill"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    talents: Mapped[list["Talent"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    armor: Mapped[list["Armor"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )  # Changed from Armour to Armor
    weapons: Mapped[list["Weapon"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    spells_and_prayers: Mapped[list["Magic"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    trappings: Mapped[list["Trapping"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    ammunition: Mapped[list["Ammunition"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )
    ledger: Mapped[list["Ledger"]] = db.relationship(
        cascade="all, delete-orphan", back_populates="character"
    )

    def get_attribute_total(self, attribute_name):
        attribute = int(getattr(self.attributes, f"{attribute_name.lower()}_base", 0))
        modifier = int(
            getattr(self.attributes, f"{attribute_name.lower()}_modifier", 0)
        )
        bonus = int(getattr(self.attributes, f"{attribute_name.lower()}_bonus", 0))
        return attribute + modifier + bonus

    def get_encumbrance(self, belonging: str):
        if belonging not in ["armor", "weapons", "trappings"]:
            raise ValueError(f"Invalid belonging: {belonging}")
        total = 0
        for item in getattr(self, belonging, []):
            total += item.encumbrance
        return total

    def get_attribute_bonus(self, attribute_name):
        total = self.get_attribute_total(attribute_name)
        return total // 10

    @property
    def hardy_wounds_bonus(self):
        for talent in self.talents:
            if talent.name.capitalize() == "Hardy":
                return self.get_attribute_bonus("t")
        return 0

    @property
    def strong_back_enc_bonus(self):
        res = 0
        for talent in self.talents:
            if talent.name.title() == "Strong Back":
                res = talent.times_taken
        return res

    @property
    def corruption_threshold(self):
        return self.get_attribute_bonus("t") + self.get_attribute_bonus("wp")


class BaseMechanics(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        db.ForeignKey("character.id"), nullable=False, unique=True
    )
    character: Mapped["Character"] = db.relationship(back_populates="base_mechanics")
    experience: Mapped[int]
    experience_spent: Mapped[int]
    movement: Mapped[int]
    fate_points: Mapped[int]
    fortune_points: Mapped[int]
    resilience: Mapped[int]
    resolve: Mapped[int]
    motivation: Mapped[int]
    corruption: Mapped[int]
    mutations: Mapped[int]
    mental_mutations: Mapped[int]
    physical_mutations: Mapped[int]


class TextFields(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        db.ForeignKey("character.id"), nullable=False, unique=True
    )
    character: Mapped["Character"] = db.relationship(back_populates="text_fields")
    psychology: Mapped[str]
    health_notes: Mapped[str]
    short_term_ambition: Mapped[str]
    long_term_ambition: Mapped[str]
    doom: Mapped[str]
    campaign_notes: Mapped[str]


class Party(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        db.ForeignKey("character.id"), nullable=False, unique=True
    )
    character: Mapped["Character"] = db.relationship(back_populates="party")
    name: Mapped[str]
    members: Mapped[str]
    ambitions: Mapped[str]
    gold: Mapped[int]
    silver: Mapped[int]
    brass: Mapped[int]


class Attributes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        db.ForeignKey("character.id"), nullable=False, unique=True
    )
    character: Mapped["Character"] = db.relationship(back_populates="attributes")

    ws_base: Mapped[int] = mapped_column(default=0)
    ws_modifier: Mapped[int] = mapped_column(default=0)
    ws_bonus: Mapped[int] = mapped_column(default=0)

    bs_base: Mapped[int] = mapped_column(default=0)
    bs_modifier: Mapped[int] = mapped_column(default=0)
    bs_bonus: Mapped[int] = mapped_column(default=0)

    s_base: Mapped[int] = mapped_column(default=0)
    s_modifier: Mapped[int] = mapped_column(default=0)
    s_bonus: Mapped[int] = mapped_column(default=0)

    t_base: Mapped[int] = mapped_column(default=0)
    t_modifier: Mapped[int] = mapped_column(default=0)
    t_bonus: Mapped[int] = mapped_column(default=0)

    i_base: Mapped[int] = mapped_column(default=0)
    i_modifier: Mapped[int] = mapped_column(default=0)
    i_bonus: Mapped[int] = mapped_column(default=0)

    ag_base: Mapped[int] = mapped_column(default=0)
    ag_modifier: Mapped[int] = mapped_column(default=0)
    ag_bonus: Mapped[int] = mapped_column(default=0)

    dex_base: Mapped[int] = mapped_column(default=0)
    dex_modifier: Mapped[int] = mapped_column(default=0)
    dex_bonus: Mapped[int] = mapped_column(default=0)

    int_base: Mapped[int] = mapped_column(default=0)
    int_modifier: Mapped[int] = mapped_column(default=0)
    int_bonus: Mapped[int] = mapped_column(default=0)

    wp_base: Mapped[int] = mapped_column(default=0)
    wp_modifier: Mapped[int] = mapped_column(default=0)
    wp_bonus: Mapped[int] = mapped_column(default=0)

    fel_base: Mapped[int] = mapped_column(default=0)
    fel_modifier: Mapped[int] = mapped_column(default=0)
    fel_bonus: Mapped[int] = mapped_column(default=0)


class BasicSkill(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="basic_skills")
    name: Mapped[str]
    attribute: Mapped[str]
    advances: Mapped[int] = mapped_column(default=0)

    @property
    def base_value(self):
        return int(self.character.get_attribute_total(self.attribute))

    @property
    def total(self):
        return self.base_value + self.advances


class Skill(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="skills")
    name: Mapped[str]
    attribute: Mapped[str]
    advances: Mapped[int] = mapped_column(default=0)

    @property
    def base_value(self):
        return self.character.get_attribute_total(self.attribute)

    @property
    def total(self):
        return self.base_value + self.advances


class Talent(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="talents")
    name: Mapped[str]
    description: Mapped[str]
    given_bonus: Mapped[int]
    bonus_attribute: Mapped[str]
    times_taken: Mapped[int] = mapped_column(default=1)


class Armor(db.Model):  # Changed from Armour to Armor
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(
        back_populates="armor"
    )  # Changed from armours to armor
    name: Mapped[str]
    encumbrance: Mapped[int]
    armor_points: Mapped[int]  # Changed from armour_points to armor_points
    location: Mapped[str]
    qualities: Mapped[str]


class Weapon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="weapons")
    name: Mapped[str]
    encumbrance: Mapped[int]
    range: Mapped[int]
    damage: Mapped[str]
    qualities: Mapped[str]


class Magic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(
        back_populates="spells_and_prayers"
    )
    name: Mapped[str]
    casting_number: Mapped[int]
    range: Mapped[str]
    target: Mapped[str]
    duration: Mapped[str]
    effect: Mapped[str]


class Trapping(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="trappings")
    name: Mapped[str]
    encumbrance: Mapped[int]
    quantity: Mapped[int]
    description: Mapped[str]


class Ammunition(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"))
    character: Mapped["Character"] = db.relationship(back_populates="ammunition")
    name: Mapped[str]
    quantity: Mapped[int]
    qualities: Mapped[str]


class Ledger(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        db.ForeignKey("character.id"), nullable=False
    )
    character: Mapped["Character"] = db.relationship(back_populates="ledger")
    who: Mapped[str]
    what: Mapped[str]
    gold: Mapped[int]
    silver: Mapped[int]
    brass: Mapped[int]
