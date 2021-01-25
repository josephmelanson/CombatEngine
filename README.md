# Combat Engine
Combat Engine functions as a simple strategy game, but is actually intended as a learning tool. This version is written in Python, and uses basic to intermediate level code and concepts. The goal of this project is create a program that is simple enough in scope to be recreated in different programming languages as the author learns them. As such, Combat Engine is meant to be a learning tool that makes learning new programming languages, and their structures, more relatable to someone with interest in game design and mechanics.

The rules that govern combat in Combat Engine are based on the Wizards of the Coast Dungeons & Dragons 5.1 Open Gaming License (https://dnd.wizards.com/articles/features/systems-reference-document-srd), but have been modified and streamlined to create a simplier game experience, and facilitate ease of coding.

## Version
This is version 1.4 (Python). Version 2.0 will be in Java.

## Installation
Python and Pandas will need to be installed on the user's system for Combat Engine to run.

To install Pandas on Linux:

sudo apt install python3-pip

pip3 install pandas

## Usage
Combat Engine should be executable from a CLI (Command Line, GitBash, Terminal) or through a Python IDE.

Please note that upon saving a score, Combat Engine will create a file name score_file.csv in the same directory as the combatengine.py file.

```python
python combatengine.py
```

## Gameplay
Players are prompted to name a character, whereupon combat takes place automatically. If the play wins, there is a chance the defeated monster will drop a potion. Players then have the option to use the potion, which will restore a small amount of health. Next, the retire prompt gives players a chance to end their game and save their score. Scores are only saved if a player retires.

## Updates/Improvements
Version 2 will have a potion loop so that players will have the option of using multiple potions (if they have them) before resuming combat. Version 2 will also have a "Play again?" option after a character is defeated.

## Contributing
Feedback is very welcome. I'm primarly concerned with bugs and logical and syntaxual errors in the code, but suggestions regarding game flow and design are encouraged as well.

## License
I need to learn more about licenses, and which one would be most appropriate for a project of this scope. Feedback welcomed.
