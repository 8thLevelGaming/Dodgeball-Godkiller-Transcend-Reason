# Claude (later replaced by Deepseek) helped me debug the code and explained several concepts to me,
# such as why I'd want to use a dictionary to handle different attack types
# and what the dictionary should look like.
# But it did not write or plan the program.
# It was my idea to make a dodgeball combat RPG and I was the one in charge of
# all of the design decisions, mechanics, and so on (and it shows).
# I used the LLMs more as a (kind of clueless) teacher than as a substitute on this.
# Because I seek the knowledge that will let me make much more complex games in the future.

import player
import enemies
import combat
import shop
import utils

start_game = 0


class GameState:
    """This class keeps track of various progression counters and the current difficulty.
    Current_enemy makes it so there is no initial enemy so the game rolls a random one.
    The next_shop and next_overlord variables count down to the next shop or boss fight.
    The total_battles variable is basically our counter for how long the game will be."""
    def __init__(self):
        self.easy_mode = False
        self.next_shop = 9
        self.next_overlord = 9
        self.total_battles = 108
        self.fight_god = self.total_battles
        self.current_enemy = 0

        # Game Stage variables record if the game is in its early, mid, or
        # late stages based on how close the fight with god is.
        # The game is 108 battles divided into 4 quarters of 27.
        #Goes from city to dojos to the moon and finally the Dodgeball Dimension.
        self.game_quarter = self.total_battles // 4
        self.early_game_over = self.game_quarter * 3
        self.game_midpoint = self.game_quarter * 2
        self.starting_late_game = self.game_quarter

# GameState variable is initialized.
game_state = GameState()

# Tutorial. Game starts only when the player presses 1.
# I decided to not just start the game right away to give the player time
# to read and absorb all of this information first.
print("""This is a simple Python game played entirely through 
        the number keys. Your main attributes are:
        1. Strength: Determines attack damage.
        2. Precision: Determines chance to hit and score critical hits.
        3. Agility: Determines chance to graze or dodge incoming hits.
        4. Endurance: Determines maximum health and HP/stamina regen.
        
        You gain experience and money as you defeat your opponents.
        You level up each time you reach 100 experience.
        Money can be spent to buy equipment to empower yourself or
        food to heal yourself.
        
        Sardines fully restore HP and Stamina. 
        Spellcards negate damage taken for a round and deal some damage.
        
        Items acquired through play can have a variety of effects:
        Lifesteal drains some of the enemy's health to recover your own.
        Retribution deals automatic damage to enemies that hit you.
        Echo Hit gives attacks a chance to trigger a bonus basic attack on target.
        Graceful reduces all stamina costs by a listed flat amount.
        Obliterate has a percentage chance to end an enemy on a critical hit.
        Resilient gives you a % chance to survive a lethal attack with 1 hp.
        Time Control increases the duration of temporary buffs by a flat amount.
        Heroic Resolve increases damage dealt as your hp decreases.
        Accurate has a % chance to upgrade miss into graze, and half that chance to upgrade graze into hit.
        Hungry Beast enables the player to eat food without ending their turn.
        Crow makes you more crow-like, increasing money gained and giving a chance for free sardines.""")

while True:
    try:
        start_game = int(input("""You can perform various dodgeball moves to fight.
        Press 1 to start the game on normal difficulty.
        Press 2 to start the game on easy difficulty."""))
        if start_game == 1:
            break
        elif start_game == 2:
            easy_mode = True
            break
        else:
            print("\nPlease press 1 or 2!")
    except ValueError:
        print("\nPlease press 1 or 2!")

# Introduction text. This is just lore and backstory.
print("""\nYou abandoned being a princess and trained all your life for this.
You learned the most lethal dodgeball techniques the ancient masters knew.
You trained your body to the limit and paired that with optimal nutrition.
You studied the history of the sport and sought to master its principles.
It was all building up to this day. You now hold the ultimate cursed dodgeball.
In your hands there can be no greater weapon.

It is time to create an international incident or two!""")

# This just makes a line for readability.
# We do this after each turn too.
print("-" * 40)

# This runs the Player class, instantiating its values into a variable 
# called player. This variable gets refreshed if the player is defeated
# and starts over (see bottom of program), wiping progress.
# Because the game will always refer to this variable rather than the
# class itself we use player in all lowercase to search for items in the
# attached player class.
player_character = player.Player()

# Immediately after we create the player, we check if easy mode
# was selected, and if so we increase the player's level,
# plus a couple of stats and their starting money.
if game_state.easy_mode is True:
    player_character.level = 15
    player_character.strength = 12
    player_character.precision = 12
    player_character.agility = 11
    player_character.endurance = 12
    player_character.money = 120
    # HP and stamina are recalculated after the endurance buff
    # to ensure the player still starts at full.
    player_character.hp = player_character.max_hp()
    player_character.stamina = player_character.max_stamina()
        
# This is the loop that actually runs the game. The outer loop checks that
# the player is still alive and restarts the game if not.
# It now displays what stage of the game the player is in.
# The inner loop rolls random enemies, switching to an overlord enemy periodically.
while True:
    while game_state.current_enemy == 0:
        # This if/elif branch tells the player in which quarter of the
        # game they are.
        if game_state.fight_god > game_state.early_game_over:
            print("You hunt your prey at local city gyms!")
        elif game_state.fight_god > game_state.game_midpoint:
            print("You visit ancient dodgeball dojos to meet stronger enemies.")
        elif game_state.fight_god > game_state.starting_late_game:
            print("You invade the Moon in the name of dodgeball mastery.")
        elif game_state.fight_god <= game_state.starting_late_game:
            print("You seek the ultimate challenge in the Dodgeball Dimension!")

        # This triggers a shop visit if the next_shop counter hits 0.
        # The placement at the top of the loop ensures it always happens before either the overlord or god fights.
        if game_state.next_shop <= 0:
            utils.slow_print("\nYou visit the Spice King Mapo Tofu Shop!")
            shop.visit_shop(player_character)
            game_state.next_shop = 9
            continue
        elif game_state.fight_god <= 0:
            game_state.current_enemy = enemies.create_god()
            print("-" * 40)
            utils.slow_print("The Dodgeball God has descended to stop your reign of terror!")
            utils.slow_print("'You believe you have mastered Dodgeball?! You are but a frog in a well gazing up at the sky!'")
        
        # If there is no periodic or final fight scheduled, the game instead rolls a random enemy depending on
        # which stage of the game the player is in.
        elif game_state.next_overlord > 0 and game_state.fight_god > game_state.early_game_over:
            game_state.current_enemy = enemies.create_random_enemy()
            utils.slow_print(f"Prepare to face {game_state.current_enemy.type}!")

        elif game_state.next_overlord > 0 and game_state.fight_god <= game_state.early_game_over:
            game_state.current_enemy = enemies.create_greater_enemy(game_state)
            if game_state.current_enemy.type == "Catgirl":
                print("Nyaaa~!")
            elif game_state.current_enemy.type == "Abomination":
                print("A formless horror wants to play dodgeball with you!")
            else:
                print(f"A {game_state.current_enemy.type} approaches!")
        elif game_state.next_overlord <= 0 and game_state.fight_god > 54:
            game_state.current_enemy = enemies.create_overlord()
            utils.slow_print("A Dodgeball Overlord challenges you!")
            game_state.next_overlord = 9
        elif game_state.next_overlord <= 0 and game_state.fight_god <= 54:
            game_state.current_enemy = enemies.create_greater_overlord()
            utils.slow_print("A Badass Freakin' Overlord has appeared!")
            game_state.next_overlord = 9

        # Initiates combat between the player and current enemy.
        combat_state = combat.CombatState(player_character, game_state.current_enemy)
        # Retrieves the fight results.
        game_state.result = combat.fight(game_state, combat_state)

        # Game ends and displays the player's stats if god is defeated.
        if game_state.result == "GOD_DEFEATED":
            print("YOU WIN!")
            print("Your final attributes were:")
            player.full_stats_display(player_character)
            break

        # If the player is defeated they can choose a difficulty and
        # start again. This will refresh player attributes and reset global variables.
        if game_state.result == "PLAYER_DEFEATED":
            utils.slow_print("You have been defeated! But the demon demands more dodgeball...")
            print("-" * 40)
            difficulty_selection = 0
            game_state = GameState()

        while difficulty_selection not in ["1", "2"]:
            print("Will you try again?")
            print("1) Try again on normal difficulty.")
            print("2) Try again on easy difficulty.")
            difficulty_selection = input("Choose: ")
    
            if difficulty_selection == "2":
                game_state.easy_mode = True
            elif difficulty_selection == "1":
                game_state.easy_mode = False
            else:
                print("Choose 1 or 2.")
                
        player_character = player.Player()

        if easy_mode is True:
            player_character.level = 15
            player_character.strength = 12
            player_character.precision = 12
            player_character.agility = 11
            player_character.endurance = 12
            player_character.money = 120
            player_character.hp = player_character.max_hp()
            player_character.stamina = player_character.max_stamina()

    else:
        break
                
# To Do List (not necessarily in order):
# Continue testing balance. 

# Print attack rolls and enemy AC for clarity.
# Polish the % sign issue in effect displays.

# It should be possible to split the components of the fight
# function into at least 3 separate ones.

# Ideas I'm saving for the sequel (TBA):
# 1- Items with multiple special effects.
# 2- Enemies with different mechanics and behaviors.
# 3- A "pupusa shop" visited 5 times throughout the game (one per stage plus once
# at the very start of the game).
# In this shop the player can eat pupusas to gain 2 points they can spend on
# improving one of 3 combat masteries (Throwing, Dodging, and Mystery).
# Each of which would be a bar with 6 skills to buy.
# Meaning only one bar can be maxed.
