import json
import os

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
    def __init__(self, spell_class, spell_save_dc, level, spell_name, description, casting_time, range, components, duration):
        self.spell_class = spell_class
        self.spell_save_dc = spell_save_dc
        self.level = level
        self.spell_name = spell_name
        self.description = self.clean_input(description)
        self.casting_time = casting_time
        self.range = range
        self.components = components
        self.duration = duration

    def clean_input(self, text):
        return ' '.join(text.split())

    def to_dict(self):
        return {
            "spell_class": self.spell_class,
            "spell_save_dc": self.spell_save_dc,
            "level": self.level,
            "spell_name": self.spell_name,
            "description": self.description,
            "casting_time": self.casting_time,
            "range": self.range,
            "components": self.components,
            "duration": self.duration
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["spell_class"],
            data["spell_save_dc"],
            data["level"],
            data["spell_name"],
            data["description"],
            data["casting_time"],
            data["range"],
            data["components"],
            data["duration"]
        )

    def display_info(self):
        info = f"""
------------------------
Class: {self.spell_class}
Spell Save DC: {self.spell_save_dc}
Level: {self.level}
Spell Name: {self.spell_name}
Description: {self.description}
Casting Time: {self.casting_time}
Range: {self.range}
Components: {self.components}
Duration: {self.duration}
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
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in data], f, indent=4)

def load_from_file(filename, cls):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [cls.from_dict(item) for item in data]
    except FileNotFoundError:
        return []

def load_characters():
    return load_from_file(os.path.join(os.path.dirname(__file__), "characters.json"), Character)

def save_characters(characters):
    save_to_file(characters, os.path.join(os.path.dirname(__file__), "characters.json"))

def load_spells():
    return load_from_file(os.path.join(os.path.dirname(__file__), "spells.json"), Spell)

def save_spells(spells):
    save_to_file(spells, os.path.join(os.path.dirname(__file__), "spells.json"))

def load_weapons():
    return load_from_file(os.path.join(os.path.dirname(__file__), "weapons.json"), Weapon)

def save_weapons(weapons):
    save_to_file(weapons, os.path.join(os.path.dirname(__file__), "weapons.json"))

def load_bag_of_holding():
    try:
        with open(os.path.join(os.path.dirname(__file__), "bag_of_holding.json"), "r") as f:
            data = json.load(f)
            return BagOfHolding.from_dict(data)
    except FileNotFoundError:
        return BagOfHolding()

def save_bag_of_holding(bag_of_holding):
    with open(os.path.join(os.path.dirname(__file__), "bag_of_holding.json"), "w") as f:
        json.dump(bag_of_holding.to_dict(), f, indent=4)

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
    for name, details in character.class_abilities.items():
        if details.get('time', '').lower() == 'action':
            class_abilities.append(f"\033[3m{name}\033[0m: {details['description']}")

    # Collect spells for actions and bonus actions
    spells_action = []
    spells_bonus_action = []
    for spell in character.spells:
        if 'casting_time' in spell and spell['casting_time']:
            casting_time = spell['casting_time'].lower()
            if "action" in casting_time and "bonus" not in casting_time:
                spells_action.append(f"\033[3m{spell['name']}\033[0m (Level {spell['level']})")
            elif "bonus action" in casting_time:
                spells_bonus_action.append(f"\033[3m{spell['name']}\033[0m (Level {spell['level']})")

    # Debug statements
    print(f"DEBUG: Character Spells - {character.spells}")
    print(f"DEBUG: Spells for Actions - {spells_action}")
    print(f"DEBUG: Spells for Bonus Actions - {spells_bonus_action}")

    # Collect bonus actions
    bonus_actions = []
    for name, details in character.race_abilities.items():
        if details.get('time', '').lower() == 'bonus action':
            bonus_actions.append(f"\033[3m{name}\033[0m: {details['description']}")
    for name, details in character.class_abilities.items():
        if details.get('time', '').lower() == 'bonus action':
            bonus_actions.append(f"\033[3m{name}\033[0m: {details['description']}")

    # Formatting the output
    actions_info = "\n\n".join(filter(None, [
        "\033[4mAttack\033[0m:\n" + "\n\n".join(weapon_attacks) if weapon_attacks else "",
        "\033[4mSpells\033[0m:\n" + "\n\n".join(spells_action) if spells_action else "",
        "\033[4mClass Abilities\033[0m:\n" + "\n\n".join(class_abilities) if class_abilities else "",
        "\033[4mRacial Abilities\033[0m:\n" + "\n\n".join(racial_abilities) if racial_abilities else ""
    ]))

    bonus_actions_info = "\n\n".join(filter(None, [
        "\033[1mBonus Actions\033[0m:\n" + "\n\n".join(bonus_actions) if bonus_actions else "",
        "\033[1mBonus Action Spells\033[0m:\n" + "\n\n".join(spells_bonus_action) if spells_bonus_action else ""
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
    - [weapon name] info: Display information about a specific weapon.
    - add item to bag: Add an item to the Bag of Holding.
    - remove item from bag: Remove an item from the Bag of Holding.
    - list bag items: List all items in the Bag of Holding.
    - add character: Add a new character to the list.
    - [character name] turn: Display the character's actions and bonus actions for the turn.
    - [character name] info: Display information about a specific character.
    - help: Display this help message.
    - quit: Exit the program.
    """
    print(help_text)

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
    elif user_input == "add item to bag":
        handle_add_item_to_bag_command()
    elif user_input == "remove item from bag":
        handle_remove_item_from_bag_command()
    elif user_input == "list bag items":
        handle_list_bag_items_command()
    elif user_input == "add character":
        handle_add_character_command()
    elif len(parts) > 1 and parts[-1].lower() == "turn":
        handle_player_turn_command(parts)
    elif len(parts) > 1 and parts[-1].lower() == "info":
        command_subject = " ".join(parts[:-1])
        weapon = next((w for w in weapons if w.name.lower() == command_subject.lower()), None)
        character = find_character_by_name(command_subject)
        if weapon:
            handle_weapon_info_command(parts)
        elif character:
            handle_character_info_command(parts)
        else:
            print(f"No weapon or character named {command_subject} found.")
    else:
        print("Unknown command. Please try again.")

    return True

def main():
    print("Welcome to the D&D CLI. Type 'help' for a list of commands.")
    running = True
    while running:
        user_input = input("> ")
        running = handle_command(user_input)

if __name__ == "__main__":
    main()
