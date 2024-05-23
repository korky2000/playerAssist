import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

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

Ability Modifiers:
  Strength:          {self.ability_modifiers.get("strength", 0)}
  Dexterity:         {self.ability_modifiers.get("dexterity", 0)}
  Constitution:      {self.ability_modifiers.get("constitution", 0)}
  Intelligence:      {self.ability_modifiers.get("intelligence", 0)}
  Wisdom:            {self.ability_modifiers.get("wisdom", 0)}
  Charisma:          {self.ability_modifiers.get("charisma", 0)}

Proficiencies:       {', '.join(self.proficiencies)}
Saving Throws:       {', '.join(self.saving_throws)}

Weapons:             {', '.join(self.weapons)}

Race Abilities:      {json.dumps(self.race_abilities, indent=2)}
Class Abilities:     {json.dumps(self.class_abilities, indent=2)}

God:                 {self.god}
Proficiency Bonus:   {self.proficiency_bonus}

Notes:               {self.notes}
========================================
        """
        return info.strip()

    def display_turn_info(self):
        action_abilities = [name for name, details in self.class_abilities.items() if details['time'] == 'action']
        bonus_action_abilities = [name for name, details in self.class_abilities.items() if details['time'] == 'bonus action']
        reaction_abilities = [name for name, details in self.class_abilities.items() if details['time'] == 'reaction']

        info = f"""
========================================
{self.name}'s Turn
========================================
Actions:
Attack:
{', '.join(self.weapons)}

Class Abilities:
{', '.join(action_abilities)}

Bonus Actions:
{', '.join(bonus_action_abilities)}

Reactions:
{', '.join(reaction_abilities)}

Spells:
Action:
{', '.join([spell['name'] for spell in self.spells if 'action' in spell['casting_time']])}
Bonus Action:
{', '.join([spell['name'] for spell in self.spells if 'bonus action' in spell['casting_time']])}
========================================
        """
        return info.strip()

class DnDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Character Manager")

        self.characters = []

        # Load existing characters from file
        self.load_characters()

        # Setup GUI elements
        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Add character button
        self.add_char_button = tk.Button(frame, text="Add Character", command=self.add_character)
        self.add_char_button.pack(pady=5)

        # Listbox for displaying characters
        self.char_listbox = tk.Listbox(frame)
        self.char_listbox.pack(pady=5)
        self.char_listbox.bind('<<ListboxSelect>>', self.display_character)

        # Text box for displaying character details
        self.char_details = tk.Text(frame, width=60, height=20, wrap=tk.WORD)
        self.char_details.pack(pady=5)

        # Command entry
        self.command_entry = tk.Entry(frame)
        self.command_entry.pack(pady=5)
        self.command_entry.bind('<Return>', self.handle_command)

        # Populate the listbox with character names
        self.update_char_listbox()

    def add_character(self):
        char_name = simpledialog.askstring("Input", "Enter character's name:")
        if not char_name:
            return
        char_race = simpledialog.askstring("Input", "Enter character's race:")
        if not char_race:
            return
        char_sub_race = simpledialog.askstring("Input", "Enter character's sub-race (if any):")
        char_class = simpledialog.askstring("Input", "Enter character's class:")
        if not char_class:
            return
        char_level = simpledialog.askinteger("Input", "Enter character's level:")
        if char_level is None:
            return
        char_sub_class = simpledialog.askstring("Input", "Enter character's subclass:")

        ability_modifiers = {}
        for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            mod = simpledialog.askinteger("Input", f"Enter {char_name}'s {ability} modifier:")
            if mod is None:
                return
            ability_modifiers[ability] = mod

        proficiencies = simpledialog.askstring("Input", f"Enter {char_name}'s proficiencies (comma separated):")
        if not proficiencies:
            return
        proficiencies = proficiencies.lower().split(", ")
        saving_throws = simpledialog.askstring("Input", f"Enter {char_name}'s saving throw proficiencies (comma separated):")
        if not saving_throws:
            return
        saving_throws = saving_throws.lower().split(", ")
        god = simpledialog.askstring("Input", f"Enter the god {char_name} worships:")
        proficiency_bonus = simpledialog.askinteger("Input", f"Enter the proficiency bonus for {char_name}:")
        if proficiency_bonus is None:
            return
        notes = simpledialog.askstring("Input", f"Enter any additional notes for {char_name}:")
        weapons = simpledialog.askstring("Input", f"Enter {char_name}'s weapons (comma separated):")
        if not weapons:
            return
        weapons = weapons.lower().split(", ")

        race_abilities = {}
        while True:
            add_race_ability = simpledialog.askstring("Input", "Add a race ability? (y/n):").lower()
            if add_race_ability == 'n':
                break
            if add_race_ability == 'y':
                ability_name = simpledialog.askstring("Input", "Enter race ability name:")
                if not ability_name:
                    break
                ability_time = simpledialog.askstring("Input", "Enter the time it takes to complete (action, bonus action, reaction):")
                if not ability_time:
                    break
                ability_description = simpledialog.askstring("Input", "Enter the ability description:")
                if not ability_description:
                    break
                race_abilities[ability_name] = {"time": ability_time, "description": ability_description}

        class_abilities = {}
        while True:
            add_class_ability = simpledialog.askstring("Input", "Add a class ability? (y/n):").lower()
            if add_class_ability == 'n':
                break
            if add_class_ability == 'y':
                ability_name = simpledialog.askstring("Input", "Enter class ability name:")
                if not ability_name:
                    break
                ability_time = simpledialog.askstring("Input", "Enter the time it takes to complete (action, bonus action, reaction):")
                if not ability_time:
                    break
                ability_description = simpledialog.askstring("Input", "Enter the ability description:")
                if not ability_description:
                    break
                class_abilities[ability_name] = {"time": ability_time, "description": ability_description}

        spells = []
        while True:
            add_spell = simpledialog.askstring("Input", "Add a spell? (y/n):").lower()
            if add_spell == 'n':
                break
            if add_spell == 'y':
                level = simpledialog.askinteger("Input", "Enter spell level:")
                if level is None:
                    continue
                name = simpledialog.askstring("Input", "Enter spell name:")
                if not name:
                    continue
                casting_time = simpledialog.askstring("Input", "Enter casting time:")
                description = simpledialog.askstring("Input", "Enter spell description:")
                range = simpledialog.askstring("Input", "Enter spell range:")
                components = simpledialog.askstring("Input", "Enter spell components:")
                duration = simpledialog.askstring("Input", "Enter spell duration:")
                spell = {
                    "level": level,
                    "name": name,
                    "casting_time": casting_time,
                    "description": description,
                    "range": range,
                    "components": components,
                    "duration": duration
                }
                spells.append(spell)

        new_character = Character(
            char_name, char_race, char_sub_race, char_class, char_level, char_sub_class, ability_modifiers,
            proficiencies, god, proficiency_bonus, saving_throws, notes, weapons, race_abilities, class_abilities, spells
        )
        self.characters.append(new_character)
        self.save_characters()
        self.update_char_listbox()

    def display_character(self, event):
        selected_index = self.char_listbox.curselection()
        if selected_index:
            selected_character = self.characters[selected_index[0]]
            self.char_details.delete(1.0, tk.END)
            self.char_details.insert(tk.END, selected_character.display_info())

    def handle_command(self, event):
        command = self.command_entry.get()
        if command:
            self.execute_command(command)
            self.command_entry.delete(0, tk.END)

    def execute_command(self, command):
        parts = command.split()
        if len(parts) < 2:
            messagebox.showinfo("Error", "Invalid command")
            return

        if parts[1] == "turn":
            self.handle_player_turn_command(parts[0])
        elif parts[1] == "info":
            char_name = parts[0]
            character = self.find_character_by_name(char_name)
            if character:
                self.char_details.delete(1.0, tk.END)
                self.char_details.insert(tk.END, character.display_info())
            else:
                messagebox.showinfo("Error", f"No character named {char_name} found.")
        else:
            messagebox.showinfo("Error", "Unknown command")

    def handle_player_turn_command(self, char_name):
        character = self.find_character_by_name(char_name)
        if character:
            self.char_details.delete(1.0, tk.END)
            self.char_details.insert(tk.END, character.display_turn_info())
        else:
            messagebox.showinfo("Error", f"No character named {char_name} found.")

    def find_character_by_name(self, name):
        for char in self.characters:
            if char.name.lower() == name.lower():
                return char
        return None

    def load_characters(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "characterTequila.json"), "r") as file:
                data = json.load(file)
                self.characters = [Character.from_dict(char) for char in data]
        except FileNotFoundError:
            self.characters = []

    def save_characters(self):
        with open(os.path.join(os.path.dirname(__file__), "characterTequila.json"), "w") as file:
            json.dump([char.to_dict() for char in self.characters], file, indent=4)

    def update_char_listbox(self):
        self.char_listbox.delete(0, tk.END)
        for char in self.characters:
            self.char_listbox.insert(tk.END, char.name)

if __name__ == "__main__":
    root = tk.Tk()
    app = DnDApp(root)
    root.mainloop()
