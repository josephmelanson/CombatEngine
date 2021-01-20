# Combat Engine

Combat Engine functions as a simple strategy game, but is actually intended as a learning tool. This version is written in Python, and uses basic to intermediate level code and concepts. The goal of this project is create a program that is simple enough in scope to be recreated in different programming languages as the author learns them. As such, Combat Engine is meant to be a learning tool that makes learning new programming languages, and their structures, more relatable to someone with interest in game design and mechanics.

The rules that govern combat in Combat Engine are based on the Wizards of the Coast Dungeons & Dragons 5.1 Open Gaming License (https://dnd.wizards.com/articles/features/systems-reference-document-srd), but have been modified and streamlined to create a simplier game experience, and facilitate ease of coding.

## Version

This is version 1.4 (Python). Version 2.0 will be in Java.

## Installation

Python will need to be installed on the user's system for Combat Engine to run.

## Usage

Combat Engine should be executable from a CLI (Command Line, GitBash, Terminal) or through a Python IDE.

Please note that upon saving a score, Combat Engine will create a file name score_file.csv in the same directory as the combatengine.py file.

```python
python combatengine.py
```

## Game Flow
I'm considering creating a flowchart to represent game flow. Suggestions on this subject are welcomed. Players do not take part in combat per se, but instead name a character which is then assigned randomly generated statistics. A monster is then generated with random statistics, and combat takes place automatically. If the player survives the encounter, they are presented with their remaining Hit Points, and asked if they would like to retire. Retiring ends the game, and saves the players score. If the player does not retire, a new monster is generated and another combat session takes place. This flow continues until the player retires, or is defeated.

Start Game > Load Scores > Prompt for Character Name > Generate Character > Generate Monster > Run Combat

IF Player survives combat > Game rolls for loot (potion) > Show player remaining HP > Prompt for retire

ELSE Player defeated, game over.

IF Player retires > Save score IF higher than previous high score

ELSE IF Player has potion > Prompt player to use potion

THEN Generate Monster > Run Combat > LOOP to IF Player survives combat

## Contributing
Feedback is very welcome. I'm primarly concerned with bugs and logical and syntaxual errors in the code, but suggestions regarding game flow and design are encouraged as well.

## License
I need to learn more about licenses, and which one would be most appropriate for a project of this scope. Feedback welcomed.