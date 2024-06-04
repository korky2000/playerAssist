import json
import os
import sys
import textwrap
import random


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def load_wild_magic_table():
    with open(resource_path("wild_magic_table.json"), "r") as file:
        return json.load(file)

wild_magic_table = load_wild_magic_table()

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)




class Character:
    def __init__(self, name, race, sub_race, char_class, level, sub_class, ability_modifiers, proficiencies, god, proficiency_bonus, saving_throws, notes, weapons, race_abilities, class_abilities, spells):
        self.name = name
        self.race = race
        self.sub_race = sub_race
        self.char_class = char_class
        self.level = level
        self.sub_class = sub_class
        self.ability_modifiers = ability_modifiers
        self.proficiencies = [proficiency.lower() for proficiency in proficiencies]
        self.god = god
        self.proficiency_bonus = proficiency_bonus
        self.saving_throws = [saving_throw.lower() for saving_throw in saving_throws]
        self.notes = notes
        self.weapons = weapons
        self.race_abilities = race_abilities
        self.class_abilities = class_abilities
        self.spells = spells

    def get_stat(self, stat):
        skill_to_ability = {
            "athletics": "strength",
            "acrobatics": "dexterity",
            "sleight of hand": "dexterity",
            "stealth": "dexterity",
            "arcana": "intelligence",
            "history": "intelligence",
            "investigation": "intelligence",
            "nature": "intelligence",
            "religion": "intelligence",
            "animal handling": "wisdom",
            "insight": "wisdom",
            "medicine": "wisdom",
            "perception": "wisdom",
            "survival": "wisdom",
            "deception": "charisma",
            "intimidation": "charisma",
            "performance": "charisma",
            "persuasion": "charisma",
            "social interaction": "charisma"
        }

        stat = stat.lower()

        if stat in self.ability_modifiers:
            total_modifier = self.ability_modifiers[stat]
            if stat in self.saving_throws:
                total_modifier += self.proficiency_bonus
            return total_modifier

        ability = skill_to_ability.get(stat, None)
        if not ability:
            return None

        ability_modifier = self.ability_modifiers.get(ability, 0)
        total_modifier = ability_modifier

        if stat in self.proficiencies:
            total_modifier += self.proficiency_bonus

        return total_modifier

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "sub_race": self.sub_race,
            "char_class": self.char_class,
            "level": self.level,
            "sub_class": self.sub_class,
            "ability_modifiers": self.ability_modifiers,
            "proficiencies": self.proficiencies,
            "god": self.god,
            "proficiency_bonus": self.proficiency_bonus,
            "saving_throws": self.saving_throws,
            "notes": self.notes,
            "weapons": self.weapons,
            "race_abilities": self.race_abilities,
            "class_abilities": self.class_abilities,
            "spells": self.spells
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["race"],
            data.get("sub_race", ""),
            data["char_class"],
            data["level"],
            data["sub_class"],
            data["ability_modifiers"],
            data["proficiencies"],
            data.get("god", ""),
            data["proficiency_bonus"],
            data.get("saving_throws", []),
            data.get("notes", ""),
            data.get("weapons", []),
            data.get("race_abilities", {}),
            data.get("class_abilities", {}),
            data.get("spells", [])
        )

    def display_info(self):
        weapon_info = ""
        for weapon_name in self.weapons:
            weapon = next((w for w in weapons if w.name.lower() == weapon_name.lower()), None)
            if weapon:
                weapon_info += weapon.display_info() + "\n"

        race_abilities_info = "\n".join([f"  {name} ({details['time']}): {details['description']}" for name, details in self.race_abilities.items()])
        class_abilities_info = "\n".join([f"  {name} ({details['time']}): {details['description']}" for name, details in self.class_abilities.items()])

        info = f"""
========================================
Character Information
========================================
Name:                {self.name}
Race:                {self.race}
Sub-Race:            {self.sub_race}
Class:               {self.char_class}
Level:               {self.level}
Subclass:            {self.sub_class}

----------------------------------------
Ability Modifiers
----------------------------------------
  Strength:          {self.ability_modifiers.get("strength", 0)}
  Dexterity:         {self.ability_modifiers.get("dexterity", 0)}
  Constitution:      {self.ability_modifiers.get("constitution", 0)}
  Intelligence:      {self.ability_modifiers.get("intelligence", 0)}
  Wisdom:            {self.ability_modifiers.get("wisdom", 0)}
  Charisma:          {self.ability_modifiers.get("charisma", 0)}

----------------------------------------
Proficiencies:       {', '.join(self.proficiencies)}
Saving Throws:       {', '.join(self.saving_throws)}

----------------------------------------
Weapons
----------------------------------------
{weapon_info}
----------------------------------------
Race Abilities
----------------------------------------
{race_abilities_info}

----------------------------------------
Class Abilities
----------------------------------------
{class_abilities_info}

----------------------------------------
God:                 {self.god}
Proficiency Bonus:   {self.proficiency_bonus}

----------------------------------------
Notes
----------------------------------------
{self.notes}
========================================
        """
        return info.strip()


class Spell:
    def __init__(self, spell_class, spell_save, spell_save_dc, level, spell_name, description, casting_time, range, components, duration, damage_dice=None, spell_type="Other"):
        self.spell_class = spell_class
        self.spell_save = spell_save
        self.spell_save_dc = spell_save_dc
        self.level = level
        self.spell_name = spell_name
        self.description = self.clean_input(description)
        self.casting_time = casting_time
        self.range = range
        self.components = components
        self.duration = duration
        self.damage_dice = damage_dice
        self.spell_type = spell_type

    def clean_input(self, text):
        return ' '.join(text.split())

    def to_dict(self):
        return {
            "spell_class": self.spell_class,
            "spell_save": self.spell_save,
            "spell_save_dc": self.spell_save_dc,
            "level": self.level,
            "spell_name": self.spell_name,
            "description": self.description,
            "casting_time": self.casting_time,
            "range": self.range,
            "components": self.components,
            "duration": self.duration,
            "damage_dice": self.damage_dice,
            "spell_type": self.spell_type
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["spell_class"],
            data.get("spell_save"),
            data.get("spell_save_dc"),
            data["level"],
            data["spell_name"],
            data["description"],
            data["casting_time"],
            data["range"],
            data["components"],
            data["duration"],
            data.get("damage_dice"),
            data.get("spell_type", "Other")
        )

    def display_info(self):
        info = f"""
------------------------
Class: {self.spell_class}
Spell Save: {self.spell_save if self.spell_save else "N/A"}
Spell Save DC: {self.spell_save_dc if self.spell_save_dc else "N/A"}
Level: {self.level}
Spell Name: {self.spell_name}
Description: {self.description}
Casting Time: {self.casting_time}
Range: {self.range}
Components: {self.components}
Duration: {self.duration}
Damage Dice: {self.damage_dice if self.damage_dice else "N/A"}
Spell Type: {self.spell_type}
------------------------
        """
        return info.strip()


class Weapon:
    def __init__(self, name, attack_bonus, damage, damage_type, notes):
        self.name = name
        self.attack_bonus = attack_bonus
        self.damage = damage
        self.damage_type = damage_type
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "attack_bonus": self.attack_bonus,
            "damage": self.damage,
            "damage_type": self.damage_type,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["attack_bonus"],
            data["damage"],
            data["damage_type"],
            data["notes"]
        )

    def display_info(self):
        info = f"""
------------------------
Name: {self.name}
Attack Bonus: {self.attack_bonus}
Damage: {self.damage}
Damage Type: {self.damage_type}
Notes: {self.notes}
------------------------
        """
        return info.strip()

class BagOfHolding:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        return "\n".join(self.items)

    def to_dict(self):
        return {
            "items": self.items
        }

    @classmethod
    def from_dict(cls, data):
        bag = cls()
        bag.items = data["items"]
        return bag

    def display_info(self):
        items_list = "\n".join(self.items)
        info = f"""
------------------------
Bag of Holding Items:
{items_list}
------------------------
        """
        return info.strip()

def save_to_file(data, filename):
    with open(resource_path(filename), "w") as f:
        json.dump([item.to_dict() for item in data], f, indent=4)

def load_from_file(filename, cls):
    try:
        with open(resource_path(filename), "r") as f:
            data = json.load(f)
            return [cls.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

def load_characters():
    return load_from_file("characters.json", Character)

def save_characters(characters):
    save_to_file(characters, "characters.json")

def load_spells():
    return load_from_file("spells.json", Spell)

def save_spells(spells):
    save_to_file(spells, "spells.json")

def load_weapons():
    return load_from_file("weapons.json", Weapon)

def save_weapons(weapons):
    save_to_file(weapons, "weapons.json")

def load_bag_of_holding():
    default_items = ["Potion of Healing", "Rope (50 feet)", "Torch", "Rations (5 days)", "Dagger"]
    file_path = resource_path("bag_of_holding.json")
    
    try:
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 0:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    return BagOfHolding.from_dict(data)
            else:
                raise json.JSONDecodeError("File is empty", file_path, 0)
        else:
            raise FileNotFoundError
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize with default items and save to file
        bag_of_holding = BagOfHolding()
        for item in default_items:
            bag_of_holding.add_item(item)
        save_bag_of_holding(bag_of_holding)
        return bag_of_holding

def save_bag_of_holding(bag_of_holding):
    with open(resource_path("bag_of_holding.json"), "w") as f:
        json.dump(bag_of_holding.to_dict(), f, indent=4)

class BagOfHolding:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        return "\n".join(self.items)

    def to_dict(self):
        return {
            "items": self.items
        }

    @classmethod
    def from_dict(cls, data):
        bag = cls()
        bag.items = data["items"]
        return bag

    def display_info(self):
        items_list = "\n".join(self.items)
        info = f"""
------------------------
Bag of Holding Items:
{items_list}
------------------------
        """
        return info.strip()



characters = load_characters()
spells = load_spells()
weapons = load_weapons()
bag_of_holding = load_bag_of_holding()

def handle_add_note_command():
    name = input("Enter character's name: ")
    character = find_character_by_name(name)
    if character:
        note = input("Enter the note: ")
        character.notes += "\n" + note
        save_characters(characters)
        print(f"Note added to {name} successfully.")
    else:
        print(f"No character named {name} found.")

def handle_add_spell_command():
    try:
        spell_class = input("Enter the spell's class: ")
        spell_save_dc = int(input("Enter the spell's save DC: "))
        level = int(input("Enter the spell's level: "))
        spell_name = input("Enter the spell's name: ")
        description = input("Enter the spell's description: ")
        casting_time = input("Enter the casting time: ")
        range = input("Enter the range: ")
        components = input("Enter the components: ")
        duration = input("Enter the duration: ")

        new_spell = Spell(spell_class, spell_save_dc, level, spell_name, description, casting_time, range, components, duration)
        spells.append(new_spell)
        save_spells(spells)
        print(f"Spell {spell_name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_add_weapon_command():
    try:
        name = input("Enter weapon's name: ")
        attack_bonus = int(input("Enter the weapon's attack bonus: "))
        damage = input("Enter the weapon's damage: ")
        damage_type = input("Enter the weapon's damage type: ")
        notes = input("Enter any additional notes: ")

        new_weapon = Weapon(name, attack_bonus, damage, damage_type, notes)
        weapons.append(new_weapon)
        save_weapons(weapons)
        print(f"Weapon {name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_weapon_info_command(parts):
    weapon_name = " ".join(parts[:-1])
    weapon = next((w for w in weapons if w.name.lower() == weapon_name.lower()), None)
    if weapon:
        print(weapon.display_info())
    else:
        print(f"No weapon named {weapon_name} found.")

def handle_add_item_to_bag_command():
    item = input("Enter the item to add to the Bag of Holding: ")
    bag_of_holding.add_item(item)
    save_bag_of_holding(bag_of_holding)
    print(f"Item '{item}' added to the Bag of Holding successfully.")

def handle_remove_item_from_bag_command():
    item = input("Enter the item to remove from the Bag of Holding: ")
    bag_of_holding.remove_item(item)
    save_bag_of_holding(bag_of_holding)
    print(f"Item '{item}' removed from the Bag of Holding successfully.")

def handle_list_bag_items_command():
    print("Items in the Bag of Holding:")
    print(bag_of_holding.list_items())

def get_best_character_for_stat(skill):
    best_character = None
    highest_stat = -1
    for character in characters:
        char_stat = character.get_stat(skill)
        if char_stat is not None and char_stat > highest_stat:
            highest_stat = char_stat
            best_character = character
    return best_character

def find_character_by_name(name):
    return next((char for char in characters if char.name.lower() == name.lower()), None)

def handle_check_command(parts):
    if len(parts) >= 2:
        skill_to_check = " ".join(parts[:-1])
        best_character = get_best_character_for_stat(skill_to_check)
        if best_character:
            print(f"The best character for {skill_to_check} is {best_character.name} with a {skill_to_check} modifier of {best_character.get_stat(skill_to_check)}.")
        else:
            print(f"No character has a stat for {skill_to_check}.")
    else:
        print("Please specify the skill to check (e.g., perception check).")

def handle_add_character_command():
    try:
        name = input("Enter character's name: ")
        race = input("Enter character's race: ")
        sub_race = input("Enter character's sub-race (if any): ")
        char_class = input("Enter character's class: ")
        level = int(input("Enter character's level: "))
        sub_class = input("Enter character's subclass: ")
        abilities = {}
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            abilities[ability] = int(input(f"Enter {name}'s {ability} modifier: "))
        proficiencies = input(f"Enter {name}'s proficiencies (comma separated): ").lower().split(", ")
        saving_throws = input(f"Enter {name}'s saving throw proficiencies (comma separated): ").lower().split(", ")
        god = input(f"Enter the god {name} worships: ")
        proficiency_bonus = int(input(f"Enter the proficiency bonus for {name}: "))
        notes = input(f"Enter any additional notes for {name}: ")

        weapons = input(f"Enter {name}'s weapons (comma separated): ").lower().split(", ")
        race_abilities = {}
        while True:
            add_race_ability = input("Add a race ability? (y/n): ").lower()
            if add_race_ability == 'n':
                break
            ability_name = input("Enter race ability name: ")
            ability_time = input("Enter the time it takes to complete (action, bonus action, reaction): ")
            ability_description = input("Enter the ability description: ")
            race_abilities[ability_name] = {"time": ability_time, "description": ability_description}

        class_abilities = {}
        while True:
            add_class_ability = input("Add a class ability? (y/n): ").lower()
            if add_class_ability == 'n':
                break
            ability_name = input("Enter class ability name: ")
            ability_time = input("Enter the time it takes to complete (action, bonus action, reaction): ")
            ability_description = input("Enter the ability description: ")
            class_abilities[ability_name] = {"time": ability_time, "description": ability_description}

        spells = []
        while True:
            add_spell = input("Add a spell? (y/n): ").lower()
            if add_spell == 'n':
                break
            level = int(input("Enter spell level: "))
            name = input("Enter spell name: ")
            casting_time = input("Enter casting time: ")
            description = input("Enter spell description: ")
            range = input("Enter spell range: ")
            components = input("Enter spell components: ")
            duration = input("Enter spell duration: ")
            spells.append({"level": level, "name": name, "casting_time": casting_time, "description": description, "range": range, "components": components, "duration": duration})

        new_character = Character(
            name, race, sub_race, char_class, level, sub_class, abilities, proficiencies, god, proficiency_bonus,
            saving_throws, notes, weapons, race_abilities, class_abilities, spells)
        characters.append(new_character)
        save_characters(characters)
        print(f"{name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_player_turn_command(parts):
    character_name = " ".join(parts[:-1])
    character = find_character_by_name(character_name)
    if not character:
        print(f"No character named {character_name} found.")
        return

    # Collect weapon attacks
    weapon_attacks = []
    for weapon_name in character.weapons:
        weapon = next((w for w in weapons if w.name.lower() == weapon_name.lower()), None)
        if weapon:
            attack_string = f"\033[3m{weapon.name}\033[0m (Attack Bonus: {weapon.attack_bonus}, Damage: {weapon.damage} {weapon.damage_type})"
            weapon_attacks.append(attack_string)

    # Collect racial abilities
    racial_abilities = []
    for name, details in character.race_abilities.items():
        if details.get('time', '').lower() == 'action':
            racial_abilities.append(f"\033[3m{name}\033[0m: {details['description']}")

    # Collect class abilities
    class_abilities = []
    class_bonus_abilities = []
    for name, details in character.class_abilities.items():
        if details.get('time', '').lower() == 'action':
            class_abilities.append(f"\033[3m{name}\033[0m: {details['description']}")
        elif details.get('time', '').lower() == 'bonus action':
            class_bonus_abilities.append(f"\033[3m{name}\033[0m: {details['description']}")

    # Collect spells for actions and bonus actions
    spells_action = []
    spells_bonus_action = []
    for spell in character.spells:
        if 'casting_time' in spell and spell['casting_time']:
            casting_time = spell['casting_time'].lower()
            spell_obj = next((s for s in spells if s.spell_name.lower() == spell['name'].lower()), None)
            if spell_obj:
                spell_info = (
                    f"\033[3m{spell['name']}\033[0m (Level {spell['level']}): {spell_obj.description}\n"
                    f"Casting Time: {spell_obj.casting_time}\n"
                    f"Range: {spell_obj.range}\n"
                    f"Damage Dice: {spell_obj.damage_dice if spell_obj.damage_dice else 'N/A'}\n"
                    f"Spell Type: {spell_obj.spell_type}\n"
                    f"Spell Save: {spell_obj.spell_save if spell_obj.spell_save else 'N/A'}\n"
                    f"Spell Save DC: {spell_obj.spell_save_dc if spell_obj.spell_save_dc else 'N/A'}"
                )
                if "bonus action" in casting_time:
                    spells_bonus_action.append(spell_info)
                else:
                    spells_action.append(spell_info)

    # Collect non-spell bonus actions based on character class and abilities
    non_spell_bonus_actions = []

    if character.char_class.lower() == "fighter":
        non_spell_bonus_actions.append("\033[3mSecond Wind\033[0m: Regain hit points equal to 1d10 + your fighter level as a bonus action.")
    if character.char_class.lower() == "rogue":
        non_spell_bonus_actions.append("\033[3mCunning Action\033[0m: Dash, Disengage, or Hide as a bonus action.")
    if "two-weapon fighting" in character.proficiencies:
        non_spell_bonus_actions.append("\033[3mTwo-Weapon Fighting\033[0m: Use a bonus action to attack with a different light melee weapon that you're holding in the other hand.")

    # Formatting the output
    actions_info = "\n\n".join(filter(None, [
        "\033[4mAttack\033[0m:\n" + "\n\n".join(weapon_attacks) if weapon_attacks else "",
        "\033[4mSpells\033[0m:\n" + "\n\n".join(spells_action) if spells_action else "",
        "\033[4mClass Abilities\033[0m:\n" + "\n\n".join(class_abilities) if class_abilities else "",
        "\033[4mRacial Abilities\033[0m:\n" + "\n\n".join(racial_abilities) if racial_abilities else ""
    ]))

    bonus_actions_info = "\n\n".join(filter(None, [
        "\033[1mBonus Actions\033[0m:\n" + "\n\n".join(non_spell_bonus_actions + class_bonus_abilities + spells_bonus_action) if spells_bonus_action or non_spell_bonus_actions or class_bonus_abilities else "",
    ]))

    turn_info = f"""
========================================
{character_name}'s Turn
What can {character_name} do on their turn?

- Use their movement speed to move
- Do an action
- Do a bonus action

========================================
\033[1mActions\033[0m:

 \033[3mDash\033[0m: Gain extra movement for your current turn

 \033[3mHelp\033[0m: You can lend your aid to another creature in the completion of a task. They gain advantage on their next roll.

 \033[3mHide\033[0m: Make a Dexterity (Stealth) check in an attempt to hide. 

{actions_info}

\033[1mBonus Actions\033[0m:
{bonus_actions_info}
========================================
    """
    print(turn_info.strip())



def display_help():
    help_text = """
  Available commands:
    - <skill> check: Check the best character for a given skill (e.g., perception check).
    - add note: Add a note to a character.
    - add spell: Add a new spell.
    - add weapon: Add a new weapon.
    - add npc: Add a new NPC.
    - add guild: Add a new guild.
    - edit character: Edit an existing character.
    - edit npc: Edit an existing NPC.
    - [guild] info: Shows info about a specific guild.
    - [weapon name] info: Display information about a specific weapon.
    - add item to bag: Add an item to the Bag of Holding.
    - remove item from bag: Remove an item from the Bag of Holding.
    - list bag items: List all items in the Bag of Holding.
    - add character: Add a new character to the list.
    - [character name] turn: Display the character's actions and bonus actions for the turn.
    - [character name] info: Display information about a specific character.
    - [NPC name] info: Display information about a specific NPC.
    - [character name] wild: Trigger a wild magic surge for a character.
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)
def handle_character_info_command(parts):
    character_name = " ".join(parts[:-1])
    character = find_character_by_name(character_name)
    if character:
        print(character.display_info())
    else:
        print(f"No character named {character_name} found.")
        
import textwrap
class NPC:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def to_dict(self):
        return {
            "name": self.name,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["notes"]
        )

    def display_info(self):
        info = f"""
------------------------
NPC Information
------------------------
Name: {self.name}
Notes: {self.notes}
------------------------
        """
        return info.strip()


def load_npcs():
    return load_from_file("npcs.json", NPC)

def save_npcs(npcs):
    save_to_file(npcs, "npcs.json")

npcs = load_npcs()

def handle_add_npc_command():
    name = input("Enter NPC's name: ")
    notes = input("Enter any notes for the NPC: ")
    new_npc = NPC(name, notes)
    npcs.append(new_npc)
    save_npcs(npcs)
    print(f"{name} has been added successfully.")

def handle_edit_npc_command():
    name = input("Enter the NPC's name to edit: ")
    npc = find_npc_by_name(name)
    if npc:
        new_name = input("Enter new name (leave blank to keep current): ")
        new_notes = input("Enter new notes (leave blank to keep current): ")
        if new_name:
            npc.name = new_name
        if new_notes:
            npc.notes = new_notes
        save_npcs(npcs)
        print(f"{name}'s information has been updated successfully.")
    else:
        print(f"No NPC named {name} found.")

def handle_npc_info_command(parts):
    npc_name = " ".join(parts[:-1])
    npc = find_npc_by_name(npc_name)
    if npc:
        print(npc.display_info())
    else:
        print(f"No NPC named {npc_name} found.")

def find_npc_by_name(name):
    return next((npc for npc in npcs if npc.name.lower() == name.lower()), None)
def handle_player_spells_command(parts):
    character_name = " ".join(parts[:-1])
    character = find_character_by_name(character_name)
    if not character:
        print(f"No character named {character_name} found.")
        return
    
    # Retrieve the character's spell list and sort by level
    spells = sorted(character.spells, key=lambda x: x['level'])
    
    # Format the character's spell list
    formatted_spells = {}
    for spell in spells:
        level = spell['level']
        if level not in formatted_spells:
            formatted_spells[level] = []
        
        spell_info = f"{spell['name']}:\n{spell['description']}"
        if spell.get('damage_dice'):
            spell_info += f"\nDamage Dice: {spell['damage_dice']}"
        
        wrapped_spell_info = textwrap.fill(spell_info, width=70)
        formatted_spells[level].append(wrapped_spell_info)
    
    # Display the formatted spell list
    for level, spells in formatted_spells.items():
        print(f"\nLevel {level} Spells:\n" + "="*15)
        for spell in spells:
            print(spell)
            print("\n" + "-"*70 + "\n")
class Guild:
    def __init__(self, name, town, headquarters, leader, members, symbols, colors, allies, enemies):
        self.name = name
        self.town = town
        self.headquarters = headquarters
        self.leader = leader
        self.members = members
        self.symbols = symbols
        self.colors = colors
        self.allies = allies
        self.enemies = enemies

    def to_dict(self):
        return {
            "name": self.name,
            "town": self.town,
            "headquarters": self.headquarters,
            "leader": self.leader,
            "members": self.members,
            "symbols": self.symbols,
            "colors": self.colors,
            "allies": self.allies,
            "enemies": self.enemies
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["town"],
            data["headquarters"],
            data["leader"],
            data["members"],
            data["symbols"],
            data["colors"],
            data["allies"],
            data["enemies"]
        )

    def display_info(self):
        members_list = ", ".join(self.members)
        allies_list = ", ".join(self.allies)
        enemies_list = ", ".join(self.enemies)
        info = f"""
------------------------
Name: {self.name}
Town: {self.town}
Headquarters: {self.headquarters}
Leader: {self.leader}
Members: {members_list}
Symbols: {self.symbols}
Colors: {self.colors}
Allies: {allies_list}
Enemies: {enemies_list}
------------------------
        """
        return info.strip()

def save_guilds(guilds):
    with open("guilds.json", "w") as f:
        json.dump([guild.to_dict() for guild in guilds], f, indent=4)

def load_guilds():
    try:
        with open("guilds.json", "r") as f:
            data = json.load(f)
            return [Guild.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

guilds = load_guilds()

def handle_edit_character_command():
    name = input("Enter the character's name to edit: ")
    character = find_character_by_name(name)
    if not character:
        print(f"No character named {name} found.")
        return

    print("Leave the field blank to keep the current value.")
    new_name = input(f"Enter new name (current: {character.name}): ").strip() or character.name
    new_race = input(f"Enter new race (current: {character.race}): ").strip() or character.race
    new_sub_race = input(f"Enter new sub-race (current: {character.sub_race}): ").strip() or character.sub_race
    new_char_class = input(f"Enter new class (current: {character.char_class}): ").strip() or character.char_class
    new_level = input(f"Enter new level (current: {character.level}): ").strip()
    new_sub_class = input(f"Enter new subclass (current: {character.sub_class}): ").strip() or character.sub_class

    abilities = {}
    for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
        abilities[ability] = input(f"Enter new {ability} modifier (current: {character.ability_modifiers.get(ability, 0)}): ").strip()
        abilities[ability] = int(abilities[ability]) if abilities[ability] else character.ability_modifiers.get(ability, 0)

    new_proficiencies = input(f"Enter new proficiencies (comma separated, current: {', '.join(character.proficiencies)}): ").strip()
    new_proficiencies = new_proficiencies.lower().split(", ") if new_proficiencies else character.proficiencies

    new_saving_throws = input(f"Enter new saving throws (comma separated, current: {', '.join(character.saving_throws)}): ").strip()
    new_saving_throws = new_saving_throws.lower().split(", ") if new_saving_throws else character.saving_throws

    new_god = input(f"Enter new god (current: {character.god}): ").strip() or character.god
    new_proficiency_bonus = input(f"Enter new proficiency bonus (current: {character.proficiency_bonus}): ").strip()
    new_proficiency_bonus = int(new_proficiency_bonus) if new_proficiency_bonus else character.proficiency_bonus

    new_notes = input(f"Enter new notes (current: {character.notes}): ").strip() or character.notes

    character.name = new_name
    character.race = new_race
    character.sub_race = new_sub_race
    character.char_class = new_char_class
    character.level = int(new_level) if new_level else character.level
    character.sub_class = new_sub_class
    character.ability_modifiers = abilities
    character.proficiencies = new_proficiencies
    character.saving_throws = new_saving_throws
    character.god = new_god
    character.proficiency_bonus = new_proficiency_bonus
    character.notes = new_notes

    save_characters(characters)
    print(f"{name} has been updated successfully.")


def handle_add_guild_command():
    try:
        name = input("Enter guild name: ")
        town = input("Enter the town where the guild is located: ")
        headquarters = input("Enter the headquarters of the guild: ")
        leader = input("Enter the leader of the guild: ")
        members = input("Enter members (comma separated): ").split(", ")
        symbols = input("Enter symbols of the guild: ")
        colors = input("Enter colors of the guild: ")
        allies = input("Enter allies (comma separated): ").split(", ")
        enemies = input("Enter enemies (comma separated): ").split(", ")

        new_guild = Guild(name, town, headquarters, leader, members, symbols, colors, allies, enemies)
        guilds.append(new_guild)
        save_guilds(guilds)
        print(f"Guild {name} has been added successfully.")
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

def handle_town_guilds_command(parts):
    town_name = " ".join(parts[:-1])
    town_guilds = [guild for guild in guilds if guild.town.lower() == town_name.lower()]
    if town_guilds:
        for guild in town_guilds:
            print(guild.display_info())
    else:
        print(f"No guilds found in {town_name}.")

def handle_guild_info_command(parts):
    guild_name = " ".join(parts[:-1])
    guild = next((g for g in guilds if g.name.lower() == guild_name.lower()), None)
    if guild:
        print(guild.display_info())
    else:
        print(f"No guild named {guild_name} found.")
def handle_wild_magic_command(parts):
    character_name = " ".join(parts[:-1])
    character = find_character_by_name(character_name)
    if not character:
        print(f"No character named {character_name} found.")
        return
    
    roll = random.randint(1, len(wild_magic_table))
    result = wild_magic_table[str(roll)]
    print(f"\n{character_name} triggers a wild magic surge!\nRoll: {roll}\nResult: {result}\n")

def handle_command(user_input):
    parts = user_input.split()

    if user_input == "quit":
        return False
    elif user_input == "help":
        display_help()
    elif "check" in user_input:
        handle_check_command(parts)
    elif user_input == "add note":
        handle_add_note_command()
    elif user_input == "add spell":
        handle_add_spell_command()
    elif user_input == "add weapon":
        handle_add_weapon_command()
    elif user_input == "add guild":
        handle_add_guild_command()
    elif user_input == "edit character":
        handle_edit_character_command()
    elif user_input == "edit npc":
        handle_edit_npc_command()
    elif len(parts) > 1 and parts[-1].lower() == "guilds":
        handle_town_guilds_command(parts)
    elif user_input == "add item to bag":
        handle_add_item_to_bag_command()
    elif user_input == "remove item from bag":
        handle_remove_item_from_bag_command()
    elif user_input == "list bag items":
        handle_list_bag_items_command()
    elif user_input == "add character":
        handle_add_character_command()
    elif user_input == "add npc":
        handle_add_npc_command()
    elif len(parts) > 1 and parts[-1].lower() == "spells":
        handle_player_spells_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "turn":
        handle_player_turn_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "wild":
        handle_wild_magic_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "info":
        command_subject = " ".join(parts[:-1])
        handle_info_command(command_subject)
    else:
        print("Unknown command. Please try again.")

    return True


def handle_info_command(command_subject):
    weapon = next((w for w in weapons if w.name.lower() == command_subject.lower()), None)
    character = find_character_by_name(command_subject)
    npc = find_npc_by_name(command_subject)
    guild = next((g for g in guilds if g.name.lower() == command_subject.lower()), None)

    if weapon:
        print(weapon.display_info())
    elif character:
        print(character.display_info())
    elif npc:
        print(npc.display_info())
    elif guild:
        print(guild.display_info())
    else:
        print(f"No weapon, character, NPC, or guild named {command_subject} found.")

def handle_character_info_command(parts):
    character_name = " ".join(parts[:-1])
    character = find_character_by_name(character_name)
    if character:
        print(character.display_info())
    else:
        print(f"No character named {character_name} found.")

def find_character_by_name(name):
    """
    Find a character by name.

    Args:
    name (str): The name of the character.

    Returns:
    Character: The character object if found, None otherwise.
    """
    return next((char for char in characters if char.name.lower() == name.lower()), None)

def find_npc_by_name(name):
    """
    Find an NPC by name.

    Args:
    name (str): The name of the NPC.

    Returns:
    NPC: The NPC object if found, None otherwise.
    """
    return next((npc for npc in npcs if npc.name.lower() == name.lower()), None)


def main():
    print("Welcome to the D&D CLI. Type 'help' for a list of commands.")
    running = True
    while running:
        user_input = input("> ")
        running = handle_command(user_input)

if __name__ == "__main__":
    main()
