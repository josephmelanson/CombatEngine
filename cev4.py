import random
from math import floor
import pandas as pd
import os

# constants
VERSION = "0.4"
VOWEL = ['a', 'e', 'i', 'o', 'u', 'y']
ALPHABET = {
    1: "a",
    2: "b",
    3: "c",
    4: "d",
    5: "e",
    6: "f",
    7: "g",
    8: "h",
    9: "i",
    10: "j",
    11: "k",
    12: "l",
    13: "m",
    14: "n",
    15: "o",
    16: "p",
    17: "q",
    18: "r",
    19: "s",
    20: "t",
    21: "u",
    22: "v",
    23: "w",
    24: "x",
    25: "y",
    26: "z"
}

# scoring
score_file = "score_file.csv"
top_ten = pd.DataFrame(columns=["name", "score"])

# difficulty options
player_base_hp = 20  # higher = more player hp = easier
mob_base_hp = 10  # higher = more monster hp = harder
potion_potency = 2  # potion_potency = x, where potions heal 1 to x hp
potion_rate = 4  # potion_rate = x, where there is 1 in x chance to get a potion

# character and monster data
# Strength = str = bonus to dmg
# Dexterity = dex = bonus to hit
# Constitution = con = bonus to hp
player_stats = {
    "name": "",
    "armor_class": 10,
    "current_hp": 0,
    "total_hp": 0,
    "str": 0,
    "dex": 0,
    "con": 0,
    "str_bns": 0,
    "dex_bns": 0,
    "con_bns": 0,
    "initiative": 0,
    "dmg_type": 6,
    "potions": 0,
    "score": 0
}

mob_stats = {
    "name": "mob",
    "armor_class": 10,
    "current_hp": 0,
    "total_hp": 0,
    "str": 0,
    "dex": 0,
    "con": 0,
    "str_bns": 0,
    "dex_bns": 0,
    "con_bns": 0,
    "initiative": 0,
    "dmg_type": 6,
    "potions": 0
}


def main():
    print(f"Welcome to Combat Engine, version {VERSION}.\n\n")
    read_score()
    raw_player_name = input("Name your character: ")
    player_stats["name"] = raw_player_name.capitalize()
    # roll character:
    player_stats["str"], player_stats["dex"], player_stats["con"], player_stats["str_bns"], player_stats["dex_bns"], player_stats["con_bns"], player_stats["total_hp"] = character_creation(player_base_hp)
    player_stats["current_hp"] = player_stats["total_hp"]
    # display character:
    print(f"\n-----{player_stats['name']}-----\nHP: {player_stats['total_hp']}\nAC: {player_stats['armor_class']}\n-----Attributes-----\nStrength: {player_stats['str']}\nDexterity: {player_stats['dex']}\nConstitution: {player_stats['con']}\n-----Bonuses-----\nStrength Bonus: {player_stats['str_bns']}\nDexterity Bonus: {player_stats['dex_bns']}\nConstitution Bonus: {player_stats['con_bns']}\n----------\n")
    # initialize encounter with monster
    post_tf = True
    while post_tf:
        # monster loop generation and monster stats generation
        play_again = mob_loop()
        while play_again == 1:  # the monster and the player have hp
            # run combat
            play_again = combat_round(player_stats['initiative'], mob_stats['initiative'])
        if play_again == 2:  # player hp, not monster
            post_tf = post_combat()
        elif play_again == 3:  # monster has hp, not player
            post_tf = False
            print(f"\nYou died. Game over.\nYour score was: {player_stats['score']}\n")
    print("Game over. Press any key to quit.")
    input()


# start character creation functions
def roll_stats():  # roll stats
    stat_final = random.randrange(3, 19)
    return stat_final


def stat_to_bonus(stat_score): # translate stats to bonus
    return floor((stat_score-10)/2)


def character_creation(cc_hp_base): # roll stats, bonuses, hp
    cc_str = roll_stats()
    cc_dex = roll_stats()
    cc_con = roll_stats()
    cc_str_bonus = stat_to_bonus(cc_str)
    cc_dex_bonus = stat_to_bonus(cc_dex)
    cc_con_bonus = stat_to_bonus(cc_con)
    cc_hp = cc_hp_base + cc_con_bonus
    return cc_str, cc_dex, cc_con, cc_str_bonus, cc_dex_bonus, cc_con_bonus, cc_hp


def mob_name(player_name, length_mod):
    name_list = []
    name_num = len(player_name)
    name_length = name_num + length_mod
    for i in range(0, name_length):
        number = random.randrange(1, 26)
        letter = ALPHABET.get(number)
        name_list.append(letter)
    vowel_present = False
    for i in VOWEL:
        if i in name_list:
            vowel_present = True
            break
    if not vowel_present:
        # i think this works, but the first time it runs length_mod is 0, so no vowels get added...
        for i in range(name_length):
            random_vowel = random.randint(0, 5)
            new_vowel = VOWEL[random_vowel]
            name_list.append(new_vowel)
    final_name = ''.join(map(str, name_list))
    final_name = final_name.capitalize()
    return final_name


def mob_creation(mob_hp_base, rounds):
    mc_str = roll_stats()
    mc_dex = roll_stats()
    mc_con = roll_stats()
    mc_str_bonus = stat_to_bonus(mc_str)
    mc_dex_bonus = stat_to_bonus(mc_dex)
    mc_con_bonus = stat_to_bonus(mc_con)
    mc_hp = mob_hp_base + mc_con_bonus + rounds
    mc_name = mob_name(player_stats['name'], player_stats['score'])
    mc_name.capitalize()
    return mc_str, mc_dex, mc_con, mc_str_bonus, mc_dex_bonus, mc_con_bonus, mc_hp, mc_name
# end character creation functions


# start combat functions
def initiative(init_pdb, init_mdb):  # init_pdb=player dex bonus, init_mdb=mob dex bonus
    player_init_roll = random.randrange(1,21) + init_pdb
    mob_init_roll = random.randrange(1,21) + init_mdb
    while player_init_roll == mob_init_roll:
        player_init_roll = random.randrange(1,21) + init_pdb
        mob_init_roll = random.randrange(1,21) + init_mdb
    return player_init_roll, mob_init_roll


def mob_loop():
    # create monster
    mob_stats["str"], mob_stats["dex"], mob_stats["con"], mob_stats["str_bns"], mob_stats["dex_bns"], mob_stats["con_bns"], mob_stats["total_hp"], mob_stats["name"] = mob_creation(mob_base_hp, player_stats['score'])
    mob_stats["current_hp"] = mob_stats["total_hp"]
    print(f"\n----------\nA {mob_stats['name']} appeared!\nHP: {mob_stats['total_hp']}\nStrength: {mob_stats['str']}\nDexterity: {mob_stats['dex']}\nConstitution: {mob_stats['con']}\n----------\nStrength Bonus: {mob_stats['str_bns']}\nDexterity Bonus: {mob_stats['dex_bns']}\nConstitution Bonus: {mob_stats['con_bns']}\n----------\n")
    # roll initiative
    player_stats["initiative"], mob_stats["initiative"] = initiative(player_stats["dex_bns"], mob_stats["dex_bns"])
    print(f"{player_stats['name']} rolled {player_stats['initiative']} for initiative.\nThe {mob_stats['name']} rolled {mob_stats['initiative']}.")
    return 1


def roll_for_dmg(dmg_type, dmg_bonus):
    dmg_final = random.randrange(1,dmg_type) + dmg_bonus
    if dmg_final < 1:
        dmg_final = 1
    return dmg_final


def roll_to_hit(attacker_hit_bonus, defender_ac):
    attacker_to_hit = random.randrange(1,21) + attacker_hit_bonus
    if attacker_to_hit >= defender_ac:
        return True, attacker_to_hit
    elif attacker_to_hit < defender_ac:
        return False, attacker_to_hit


def combat_round(player_data, mob_data):
    dmg_to_player = 0
    dmg_to_mob = 0
    # check if player goes first
    if player_data >= mob_data:
        hit_tf, att_to_hit = roll_to_hit(player_stats['dex_bns'], mob_stats['armor_class'])  # check if player hit mob
        if hit_tf:
            print(f"{player_stats['name']} hits with a {att_to_hit}!")
            dmg_to_mob = roll_for_dmg(player_stats['dmg_type'], player_stats['str_bns'])
            print(f"{player_stats['name']} does {dmg_to_mob} damage.")
        elif not hit_tf:
            print(f"{player_stats['name']} missed with a {att_to_hit}.")
        # check if mob hit player
        hit_tf, att_to_hit = roll_to_hit(mob_stats['dex_bns'], player_stats['armor_class'])
        if hit_tf:
            print(f"{mob_stats['name']} hits with a {att_to_hit}!")
            dmg_to_player = roll_for_dmg(mob_stats['dmg_type'], mob_stats['str_bns'])
            print(f"{mob_stats['name']} does {dmg_to_player} damage.")
        elif not hit_tf:
            print(f"{mob_stats['name']} missed with a {att_to_hit}.")
    # check if mob goes first
    elif player_data < mob_data:
        hit_tf, att_to_hit = roll_to_hit(mob_stats['dex_bns'], player_stats['armor_class']) # check if mob hit player
        if hit_tf:
            print(f"{mob_stats['name']} hits with a {att_to_hit}!")
            dmg_to_player = roll_for_dmg(mob_stats['dmg_type'], mob_stats['str_bns'])
            print(f"{mob_stats['name']} does {dmg_to_player} damage.")
        elif not hit_tf:
            print(f"{mob_stats['name']} missed with a {att_to_hit}.")
        # check if player hit mob
        hit_tf, att_to_hit = roll_to_hit(player_stats['dex_bns'], mob_stats['armor_class'])
        if hit_tf:
            print(f"{player_stats['name']} hits with a {att_to_hit}!")
            dmg_to_mob = roll_for_dmg(player_stats['dmg_type'], player_stats['str_bns'])
            print(f"{player_stats['name']} does {dmg_to_mob} damage.")
        elif not hit_tf:
            print(f"{player_stats['name']} missed with a {att_to_hit}.")
    # update health
    player_stats['current_hp'] = player_stats['current_hp'] - dmg_to_player
    mob_stats['current_hp'] = mob_stats['current_hp'] - dmg_to_mob
    # return combat round outcome. 1 = both alive (draw), 2 = player alive (win), 3 = mob alive (lose)
    if player_stats['current_hp'] > 0 and mob_stats['current_hp'] > 0:
        combat_result = 1
        return combat_result
    if player_stats['current_hp'] > 0 and mob_stats['current_hp'] < 1:
        combat_result = 2
        return combat_result
    elif player_stats['current_hp'] < 1:
        combat_result = 3
        return combat_result


def post_combat():
    print("\nYou win.\n")
    player_stats['score'] = player_stats['score'] + 1
    potion_tf = roll_for_item(potion_rate)
    if potion_tf:
        print("You find a potion on the monster.\n")
    elif not potion_tf:
        print("You found no items on the monster.\n")
    print(f"\nYou have {player_stats['potions']} potions and have {player_stats['current_hp']} HP remaining.\n")
    print(f"\nYou have defeated {player_stats['score']} monster(s).\n")
    retire_yn = input("Retire? (y/n)")
    retire_yn = retire_yn.lower()
    if retire_yn == 'y':
        print(f"\n{player_stats['name']} retired with a record of {player_stats['score']} monsters slain.\n\n")
        add_score(player_stats['name'], player_stats['score'])  # update high score list
        write_score()
        display_score()
        return False
    elif retire_yn == 'n':
        if player_stats['potions'] >= 1:
            potion_input = input("Use a potion? (y/n)")
            potion_input = potion_input.lower()
            if potion_input == 'y':
                use_potion(potion_potency)
                return True
            elif potion_input == 'n':
                return True
        elif player_stats['potions'] <= 0:
            return True
# end combat functions


# start item functions
def roll_for_item(item_chance):
    item_value = random.randrange(1,item_chance)
    if item_value == 1:
        player_stats['potions'] = player_stats['potions'] + 1
        return True
    elif item_value != 1:
        return False


def use_potion(potion_min):
    potion_cap = (potion_min * 4)
    hp_healed = random.randrange(potion_min, potion_cap + 1) + potion_min # plus 1 is for python counting
    player_stats['potions'] = player_stats['potions'] - 1
    player_stats['current_hp'] = player_stats['current_hp'] + hp_healed
    print(f"You used a potion and regained {hp_healed} HP.\nYou have {player_stats['potions']} potion(s) left.\n")
    if player_stats['current_hp'] > player_stats['total_hp']:
        player_stats['current_hp'] = player_stats['total_hp']
        print(f"{hp_healed} was more than your max. HP set to {player_stats['total_hp']}.\n")
# end item functions


# start scoring functions
def add_score(score_name, new_score):
    global top_ten
    if score_name in top_ten["name"].values:
        old_score = top_ten[top_ten["name"] == score_name["score"].iloc[0]]
        if new_score > old_score:
            top_ten = top_ten[top_ten["name"] != score_name]
        else:
            return
    top_ten = top_ten.append({"name": score_name, "score": new_score}, ignore_index=True)
    top_ten = top_ten.sort_values(by="score", ascending=False).head(10)


def write_score():
    top_ten.to_csv(score_file, header=False, index=False)
    print("Scores written.\n")


def read_score():
    global top_ten
    if os.path.exists(score_file):
        top_ten = pd.read_csv(score_file, names=["name", "score"])
        print("Scores loaded.\n")
        display_score()
    else:
        print("No previous scores available.\n")


def display_score():
    print("\nThe top ten scores are:\n")
    for i, row in top_ten.sort_values(by="score", ascending=False).iterrows():
        print(f"{i+1}. {row['name']} - {row['score']}")
    print("\n")
# end scoring functions


if __name__ == "__main__":
    main()
