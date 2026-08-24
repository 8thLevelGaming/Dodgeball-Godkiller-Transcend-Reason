"""This module handles the player options, the combat calculations, and the all-important
fight() function."""

import player
import items
import utils
import enemies
import random

# Function to take player input when making decisions.
def player_options(player_character):
    # The options variable is a dictionary keying numbers to the options
    # available in a fight.
    options = {
        "1": f"Basic Shot ({player.stamina_costs('1')}). A simple throw.",
        "2": f"Meteor Shot ({player.stamina_costs('2')}). Jump and throw from above!",
        "3": f"Eye of Omens ({player.stamina_costs('3')}). Use your cursed eye to predict enemy movements!",
        "4": f"Helios Dive ({player.stamina_costs('4')}). Unleash the power of the sun!",
        "5": "Demonic Art ~ Transcend Reason (1 Soul). Have faith in your evil.",
        "6": "Rest. Catch your breath and recover extra stamina.",
        "7": f"Eat sardines to recover your energy and maintain your physical form. You have {player_character.sardine_inventory}.",
        "8": f"Use a spellcard ({player_character.spellcard_inventory} available). 1 round of invulnerability plus deal guaranteed damage.",
        "9": "View your attributes."
        }
    # The dictionary is unpacked. The options are printed in full.
    for num, text in options.items():
        print(f"{num}) {text}")
    # Until the player picks a valid option, this loop keeps them available.
    # The chosen variable compares player input to the list of keys.
    while True:
        chosen = input("""Choose a move! """)
        if chosen in options:
            return chosen
        else:
            utils.slow_print("Your options range between 1 and 9!")

# Functions that calculate damage for normal hits, critical hits, and grazes.
# Critical hits do double damage, grazes deal half damage.
def damage_calc(attack_type, player_character, current_enemy):
    # Attack type can multiply damage.
    multiplier = player.attack_multipliers[attack_type]
    # Damage takes both strength and level into account.
    # So even players with low strength will have a slightly higher max hit
    # as they level up.
    total_damage = (player_character.strength + random.randint(1,player_character.level)) * multiplier
    # Total Damage is affected by the Heroic Resolve item effect now.
    heroic_multiplier = heroic_resolve_calculator(player_character)
    total_damage = total_damage * heroic_multiplier
    # Total damage is rounded before it is applied to prevent floats.
    total_damage = round(total_damage)
    
    # This is also where we now check if the dodgeball god's shield is active.
    # if so, the player's damage is reflected onto them on all three hit tiers.
    if getattr(current_enemy, "shield_active", False):
        reflected_damage = total_damage
        player_character.hp = player_character.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    # If there is no shield, total damage is deducted from enemy HP and
    # on-hit effects like lifedrain are applied.
    # We return the damage for display.
    else:
        current_enemy.hp = current_enemy.hp - total_damage
        effects_on_hit(player_character, current_enemy, total_damage, attack_type, is_critical=False)
        return total_damage

# This is the same calculation, but for critical hits, meaning
# damage is doubled. Due to the way attack multiplies work
# Special attacks can be multiplied even more than that.
def crit_calc(attack_type, player_character, current_enemy):
    multiplier = player.attack_multipliers[attack_type]
    total_damage = ((player_character.strength + random.randint(1,player_character.level)) * 2) * multiplier
    heroic_multiplier = heroic_resolve_calculator(player_character)
    total_damage = total_damage * heroic_multiplier
    total_damage = round(total_damage)

    if getattr(current_enemy, "shield_active", False):
        reflected_damage = total_damage
        player_character.hp = player_character.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    else:
        current_enemy.hp = current_enemy.hp - total_damage
        # Note that unlike in the previous branches, is_critical is True in
        # this function. This enables Obliterate to trigger.
        effects_on_hit(player_character, current_enemy, total_damage, attack_type, is_critical=True)
        return total_damage

# Graze is the same but damage is halved.
# Grazes do not apply on-hit effects either.
def graze_calc(attack_type, player_character, current_enemy):
    multiplier = player.attack_multipliers[attack_type]
    total_damage = ((player_character.strength + random.randint(1,player_character.level)) // 2) * multiplier
    heroic_multiplier = heroic_resolve_calculator(player_character)
    total_damage = total_damage * heroic_multiplier
    total_damage = round(total_damage)

    if getattr(current_enemy, "shield_active", False):
        reflected_damage = total_damage
        player_character.hp = player_character.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    else:
        current_enemy.hp = current_enemy.hp - total_damage
        return total_damage

# Function to calculate if an attack hits, crits, grazes, or misses.
# The player hits if their attack roll exceeds enemy AC by 30.
# And grazes if they fail to hit the AC by less than 30.
# With the starting precision value of 10 and no boosts, a player would have to
# roll 50 or higher to hit a hypothetical enemy with 10 agility.
# If the enemy has 15 agility this required roll would change to 100.
# Each point of precision translates to a 5% chance to upgrade an attack to
# the next tier of hit.
def hit_calc(attack_type, player_character, current_enemy, eye_of_omens_counter):
    # The Eye of Omens grants a considerable flat boost to attack rolls
    # if active, equivalent to about 8 precision points.
    eye_of_omens_bonus = 0
    if eye_of_omens_counter > 0:
        eye_of_omens_bonus = 40
    attack_roll = (player_character.precision * 5) + random.randint(0,100) + eye_of_omens_bonus
    # The Helios Dive attack has +25 on attack rolls also.
    # Equivalent to 5 precision points.
    if attack_type == "Helios":
        attack_roll = attack_roll + 25
        
    armor_class = (current_enemy.agility * 10)
    hit_result = "miss"

    print(f"\nYour Attack Roll = {attack_roll}. Enemy Armor Class = {armor_class}.")
    
    if attack_roll >= 30 + armor_class:
        hit_result = "crit"
    elif attack_roll >= armor_class:
        hit_result = "hit"
    elif attack_roll >= armor_class - 30:
        hit_result = "graze"
    else:
        hit_result = "miss"

    # This calculator was later rewritten to accommodate the Accurate item effect.
    # The player's total Accurate effect is grabbed and the game uses a d100 
    # to potentially upgrade miss and graze results to the next tier of hit.
    # Meaning that Accurate can be a crutch for low-precision runs but
    # is pretty useless if you can reliably crit everything.
    accurate_total = player_character.effects.get("accurate", 0)
    if accurate_total > 0:
        if hit_result == "miss":
            if random.randint(0, 100) <= accurate_total:
                hit_result = "graze"
                print("Your accuracy turns a miss into a graze!")
        elif hit_result == "graze":
            # Half the chance to upgrade a graze to a hit
            if random.randint(0, 100) <= (accurate_total // 2):
                hit_result = "hit"
                print("Your accuracy upgrades your graze into a hit!")

    # Depending on how the player's attack roll went the function
    # determines which damage calculator to use and collects their
    # output for display.
    # Note that meteor strikes have a chance to stun the enemy
    # and this chance increases for critical hits.
    if hit_result == "crit":
        damage_report = crit_calc(attack_type, player_character, current_enemy)
        utils.slow_print(f"Critical Hit! You hit for {damage_report}!")
        if attack_type == "Meteor":
            stun_check(current_enemy, chance=33)
    elif hit_result == "hit":
        damage_report = damage_calc(attack_type, player_character, current_enemy)
        utils.slow_print(f"Hit! You hit for {damage_report}!")
        if attack_type == "Meteor":
            stun_check(current_enemy, chance=25)
    elif hit_result == "graze":
        damage_report = graze_calc(attack_type, player_character, current_enemy)
        utils.slow_print(f"Graze! You hit for {damage_report}!")

    # If the player misses, they can get a special message if their
    # enemy was a kaiju. After all, how do you miss such a large
    # target?
    elif hit_result == "miss":
        if current_enemy.type == "Kaiju":
            print("Your throw was too weak to harm the kaiju!")
        else:
            utils.slow_print("Miss!")

# We add some functions for other special effects from items.
# We start with a function that will handle effects that apply
# after an enemy takes damage.
def effects_on_hit(player_character, current_enemy, total_damage, attack_type, is_critical=False):
    lifesteal_total = player_character.effects.get("lifesteal", 0)
    echo_hit_total = player_character.effects.get("echo hit", 0)
    obliterate_total = player_character.effects.get("obliterate", 0)

        # Lifesteal heals the player for a percentage of the damage taken.
    # So the function adds the total potency from the player's items together.
    # Then if the player has any lifesteal it calculates the amount of hp healed.
    # by first dividing the lifesteal total by 100 and multiplying the damage
    # dealt by the result. There is anti-overheal protection here too.
    if lifesteal_total > 0:
        heal_amount = int(total_damage * (lifesteal_total / 100))
        player_character.hp = min((player_character.hp + heal_amount), player_character.max_hp())
        print(f"You drain health from the enemy and healed for {heal_amount} hp!")

    # Echo hits roll additional attacks on hit if the player succeeds at a % roll.
    # It is possible to chain echo hits.
    if echo_hit_total > 0:
        if random.randint(0,100) <= echo_hit_total:
            print("You hit again!")
            echo_hit_damage = damage_calc("Standard", player_character, current_enemy)
            print(f"The echo hit deals {echo_hit_damage} additional damage!")

    # Obliterate has a % chance of instantly slaying the enemy. It ends with return
    # to stop further processes. It only triggers on critical hits, which we now
    # check for.
    if is_critical and obliterate_total > 0:
        if random.randint(0,100) <= obliterate_total:
            if current_enemy.type == "Dodgeball God":
                print("Even god cannot withstand your power and is obliterated.")
            else:
                print("OBLITERATED!")
            current_enemy.hp = 0
            return

# This is one of the mathier functions, which calculates the bonus damage
# from Heroic Resolve. While the player has Heroic Resolve among their item
# effects they deal more damage as their HP is lower, up to a maximum of
# around double damage with all relevant items equipped.
# The formula is similar to the one for the iconic OSRS Dharok set, but
# modified for a game where HP can go well above 99.
def heroic_resolve_calculator(player_character):
    resolve_total = player_character.effects.get("heroic resolve", 0)
    max_hp = player_character.max_hp()
    missing_percentage = (max_hp - player_character.hp) / max_hp
    heroic_bonus = 1 + missing_percentage * (resolve_total / 100)
    return heroic_bonus

# This one applies effects when the player is hit. Note we grab
# damage_report in the arguments to use for retribution.
def effects_on_damage_taken(player_character, current_enemy, damage_report):
    retribution = player_character.effects.get("retribution", 0)
    resilient = player_character.effects.get("resilient", 0)

    # The retribution effect deals a percentage of damage taken
    # back to attackers.
    if retribution > 0:
        ret_damage = int(damage_report * (retribution / 100))
        current_enemy.hp = current_enemy.hp - ret_damage
        print(f"The enemy takes {ret_damage} damage from Retribution!")

    # Resilient gives the player a chance to survive lethal damage
    # with 1 HP remaining.
    if resilient > 0:
        if player_character.hp - damage_report <= 0:
            if random.randint(0,100) <= resilient:
                player_character.hp = 1
                print("You are still standing!")

# These functions mirror the player calculation ones, but roll enemy damage.
# They use the minimum and maximum damage variables stored in the enemy classes
# as the arguments in randint, giving each enemy a custom damage range.
def enemy_damage_calc(player_character, current_enemy):
    total_damage = random.randint(current_enemy.damage_min, current_enemy.damage_max)
    player_character.hp = player_character.hp - total_damage
    return total_damage

def enemy_graze_calc(player_character, current_enemy):
    total_damage = (random.randint(current_enemy.damage_min, current_enemy.damage_max) // 2)
    player_character.hp = player_character.hp - total_damage
    return total_damage

# This small function rolls a stun chance percentage used by hit_calc()
# to give Meteor Shot a chance to stun enemies it successfully hits.
# Their stun status is then checked 
# The default stun chance is 25% but crits are given an argument
# boosting that to 33%.
def stun_check(current_enemy, chance=25):
    if random.randint(1, 100) <= chance:
        current_enemy.stunned = True
        utils.slow_print(f"{current_enemy.type} is stunned by the attack!")
        
# Function to calculate if the player is hit.
# It works the same for enemies as it does for players.
# Except the Eye of Omens bonus also applies defensively here and
# The enemies are unable to score critical hits.
def dodge_calc(player_character, current_enemy, eye_of_omens_counter):
    attack_roll = (current_enemy.precision * 5) + random.randint(0,100)
    eye_of_omens_bonus = 0
    
    if eye_of_omens_counter > 0:
        eye_of_omens_bonus = 40
        
    armor_class = (player_character.agility * 10) + eye_of_omens_bonus

    print(f"\nThe enemy's Attack Roll = {attack_roll}. Your Armor Class = {armor_class}.")

    # If the player has used a spellcard to gain invulnerability
    # that is checked first and damage is not rolled even on a hit.
    if player_character.invulnerable is True:
        print("The spellcard negates all damage!")
    elif attack_roll >= armor_class:
        damage_report = enemy_damage_calc(player_character, current_enemy)
        utils.slow_print(f"The dodgeball hits you! You take {damage_report} damage!")
        effects_on_damage_taken(player_character, current_enemy, damage_report)
    elif attack_roll >= armor_class - 30:
        damage_report = enemy_graze_calc(player_character, current_enemy)
        utils.slow_print(f"The dodgeball grazes you! You take {damage_report} damage!")
        effects_on_damage_taken(player_character, current_enemy, damage_report)
    else:
        utils.slow_print("You catch the dodgeball!")

# Function to initiate a fight with the enemy that was rolled.
def fight(player_character, current_enemy, player_turn, next_overlord, next_shop, fight_god, eye_of_omens_counter, demon_counter, god_charged, god_turn_counter):
    # it starts a loop to have both player and enemy stats on display every turn.
    # The player's turn always happens first.
    while True:
        enemies.enemy_stats_display(current_enemy)
        player.stats_display(player_character)
        player_character.invulnerable = False

        # The loop is set to immediately break if the player hits 0 HP.
        # If the enemy reaches 0 HP instead the player gets experience,
        # the overlord counter decreases, and the player potentially levels up.
        if player_character.hp < 1:
            defeat_message = enemies.get_defeat_message(current_enemy.type)
            utils.slow_print(defeat_message)
            break
        elif current_enemy.hp < 1:
            # If the enemy was god, the game is won.
            if current_enemy.type == "Dodgeball God":
                utils.slow_print(current_enemy.defeat)
                utils.slow_print("The Dodgeball God has fallen...")
                utils.slow_print("You have created a new age of Dodgeball Demons and are now the supreme overlord!")
                return "GOD_DEFEATED"
                
            utils.slow_print("\n" + current_enemy.defeat)
            utils.slow_print("Victory!")
            crow_total = player_character.effects.get("crow", 0)
            player_character.exp = player_character.exp + current_enemy.exp_reward

            # If the player has the crow effect, rewards are increased
            # and a sardine may be received as a random drop.
            if crow_total > 0:
                base_money_reward = current_enemy.money_reward
                crow_bonus_money = int(base_money_reward * (crow_total / 100))
                total_money_reward = base_money_reward + crow_bonus_money
                player_character.money = player_character.money + total_money_reward
                print(f"You found ${total_money_reward}! Your crow-like nature contributed ${crow_bonus_money}.")
    
                if random.randint(0,100) <= (crow_total):
                    player_character.sardine_inventory += 1
                    print(f"Your fellow crows bring you a sardine! You now have {player_character.sardine_inventory}.")
            else:
                player_character.money = player_character.money + current_enemy.money_reward

            # If it was an overlord, spellcards are awareded.
            if current_enemy.type in ["Dodgeball Overlord", "Badass Freakin' Overlord"]:
                player_character.spellcard_inventory += 1
                utils.slow_print(f"You have earned a Spellcard! You now have {player_character.spellcard_inventory}.")
            
            next_overlord = next_overlord - 1
            next_shop = next_shop - 1
            fight_god = fight_god - 1
            utils.slow_print(f"\nThe next Dodgeball Overlord is {next_overlord} battles away!")
            utils.slow_print(f"The next shop is {next_shop} battles away!")
            if player_character.exp >= 100:
                player.level = player.level + 1
                player.exp = player.exp - 100
                player.full_stats_display(player_character)
                player.level_up(player_character)

            # current_enemy returns to 0, rolling another enemy.
            current_enemy = 0
            return current_enemy

        # This loop is active while it is the player's turn.
        # Their buff counters decrease at the start of the turn if not at 0,
        # and the player is then free to use their actions.
        while player_turn and current_enemy.hp > 0:
            print("")
            player_move = player_options()
            
            # Each attack is keyed to a dictionary above that matches its stamina cost and
            # runs the attack roll through lambda.
            if player_move == "1":
                if player.stamina_checker(player_character, player.stamina_costs('1'), "You throw the dodgeball!", lambda: hit_calc("Standard", player_character, current_enemy, eye_of_omens_counter)):
                    player_turn = False
                    
            elif player_move == "2":
                if player.stamina_checker(player_character, player.stamina_costs('2'), "You jump and slam the dodgeball into the enemy!", lambda: hit_calc("Meteor", player_character, current_enemy, eye_of_omens_counter)):
                    player_turn = False
                    
            elif player_move == "3":
                if player_character.stamina >= player.stamina_costs('3'):
                    utils.slow_print("\nYour magical eye grants you precognition!")
                    base_duration = 3
                    time_control_bonus = player_character.effects.get("time control", 0)
                    total_duration = base_duration + time_control_bonus
                    eye_of_omens_counter = total_duration
                    if time_control_bonus > 0:
                        print("Your mastery over time extends the effect!")
                    player_character.stamina = player_character.stamina - player.stamina_costs('3')
                    player_turn = False
                else:
                    print("Not enough stamina!")
                    
            elif player_move == "4":
                if player.stamina_checker(player_character, player.stamina_costs('4'), "You throw a ball imbued with the power and malevolence of the sun!", lambda: hit_calc("Helios", player_character, current_enemy, eye_of_omens_counter)):
                    player_turn = False

            # Moves 3 and 5 boost the player's stats temporarily instead, and move 5 is
            # a free action that does not end the player's turn, but does reduce their
            # HP to 1. The player can also rest if out of stamina for other actions,
            # or view their attributes for free.
            elif player_move == "5":
                if demon_counter == 0:
                    player_character.hp = 1
                    base_duration = 3
                    time_control_bonus = player_character.effects.get("time control", 0)
                    total_duration = base_duration + time_control_bonus
                    demon_counter = total_duration
                    utils.slow_print(f"\nThe darkness takes you! Your enhanced state will last for {demon_counter} turns!")
                    if time_control_bonus > 0:
                        print("Your mastery over time extends the effect!")
                    player_character.demon_bonus_applied = player.demon_bonus_result(player_character)
                    player_character.strength = player_character.strength + player_character.demon_bonus_applied
                    player_character.precision = player_character.precision + player_character.demon_bonus_applied
                    player_character.agility = player_character.agility + player_character.demon_bonus_applied
                else:
                    print("You are already transformed!")
                    
            elif player_move == "6":
                player_character.stamina = player_character.stamina + (player_character.stamina_regen() * 3)
                player_turn = False
                
            elif player_move == "7":
                if player_character.sardine_inventory > 0:
                    player_character.sardine_inventory = player_character.sardine_inventory - 1
                    player_character.hp = player_character.max_hp()
                    player_character.stamina = player_character.max_stamina()
                    utils.slow_print("You eat the sardines. They taste like victory.")
                    if player_character.effects.get("hungry beast", 0) == 0:
                        player_turn = False
                    elif player_character.effects.get("hungry beast", 0) > 0:
                        print("You devour the sardines quickly!")
                else:
                    print("You are out of sardines!")

            elif player_move == "8":
                if player_character.spellcard_inventory > 0:
                    player_character.spellcard_inventory = player_character.spellcard_inventory - 1
                    current_enemy.hp = current_enemy.hp - (player_character.level * 2)
                    player_character.invulnerable = True
                    utils.slow_print("You become invulnerable for a brief time and unleash a powerful attack!")
                    player_turn = False
                else:
                    print("You are out of spellcards!")
                    
            elif player_move == "9":
                player.full_stats_display(player_character)

            # The following code uses min() to regenerate the player's HP and stamina
            # up to but not exceeding their maximum values. This prevents overheal.
            # We want this regen to happen after the player's turn but before the enemy
            # attacks as a mercy to the player.
            hp_regen_bonus = 0
            stamina_regen_bonus = 0
            if demon_counter > 0:
                hp_regen_bonus = 5
                stamina_regen_bonus = 10
            player_character.hp = min(player_character.hp + player_character.hp_regen() + hp_regen_bonus, player_character.max_hp())
            player_character.stamina = min(player_character.stamina + player_character.stamina_regen() + stamina_regen_bonus, player_character.max_stamina())

        # Once the player's turn ends, the enemy performs a simple attack and
        # The player can move again. If the enemy is stunned
        # then their turn is skipped, and if they enemy is
        # god then it uses a different set of actions instead of
        # only basic attacks.
        if player_turn is False and current_enemy.hp > 0:
            if getattr(current_enemy, "stunned", False):
                print("The enemy is stunned and cannot attack!")
                current_enemy.stunned = False
            elif current_enemy.type == "Dodgeball God":
                god_actions(player_character, current_enemy, god_charged, god_turn_counter, eye_of_omens_counter)
            
            else:
                utils.slow_print(f"{current_enemy.type} throws a dodgeball at you!")
                dodge_calc(player_character, current_enemy, eye_of_omens_counter)
            player_turn = True

        # The buff duration decrements were moved here so they'll run
        # correctly even if the player checks their stats.
        if eye_of_omens_counter > 0:
            eye_of_omens_counter = eye_of_omens_counter - 1
            if eye_of_omens_counter == 0:
                utils.slow_print("Your precognition ends.")
        if demon_counter > 0:
            demon_counter = demon_counter - 1
            if demon_counter == 0:
                player_character.strength = player_character.strength - player_character.demon_bonus_applied
                player_character.precision = player_character.precision - player_character.demon_bonus_applied
                player_character.agility = player_character.agility - player_character.demon_bonus_applied
                player_character.demon_bonus_applied = 0
                utils.slow_print("The darkness releases you!")
        print("-" * 40)

# This function handles the Dodgeball God's behavior.
# This is intended to be a two-phase fight against an opponent who
# becomes stronger over time and sometimes uses very damaging moves
# that call for the use of defensive buffs or the coming spellcard item.
# We use global variables for the boss states so they won't reset on their own.
def god_actions(player_character, current_enemy, god_charged, god_turn_counter, eye_of_omens_counter):

    # The enemy's shield special turns off at the start of its next turn if it was active.
    current_enemy.shield_active = False

    # The god turn counter increases by 1 each turn.
    god_turn_counter = god_turn_counter + 1

    # Every 3 turns, the boss powers up permanently, creating a DPS race.
    if god_turn_counter % 3 == 0:
        print("\nThe Dodgeball God removes a power limiter and grows stronger!")
        current_enemy.damage_min = current_enemy.damage_min + 10
        current_enemy.damage_max = current_enemy.damage_max + 10
        current_enemy.precision = current_enemy.precision + 10
    
    god_move = random.randint(0,100)

    # Boss becomes stronger below half health but does not gain new moves.
    if current_enemy.hp < (current_enemy.max_hp // 2) and current_enemy.phase_2 is False:
        print("\n'You dare?! We are as different as Heaven and Earth!'")
        current_enemy.phase_2 = True
        current_enemy.damage_min = current_enemy.damage_min + 30
        current_enemy.damage_max = current_enemy.damage_max + 30
        current_enemy.precision = current_enemy.precision + 50

    # If the boss charged an attack last turn, we want that to
    # fire on this turn, dealing heavy damage.
    # This attack will have a randomized name chosen from the list.
    if god_charged is True:
        chosen_move_name = god_name_randomizer()
        utils.slow_print("\nThe Dodgeball God unleashes their special move!")
        utils.slow_print(f'{chosen_move_name}')

        # We store the boss' current damage range to reset later.
        original_damage_min = current_enemy.damage_min
        original_damage_max = current_enemy.damage_max

        # We then double its current values.
        current_enemy.damage_min = current_enemy.damage_min * 2
        current_enemy.damage_max = current_enemy.damage_max * 2

        # We roll an attack. Because its damage range on its class
        # is boosted the damage in this calculation will also be.
        dodge_calc(player_character, current_enemy, eye_of_omens_counter)

        # Original damage range restored for subsequent turns.
        current_enemy.damage_min = original_damage_min
        current_enemy.damage_max = original_damage_max

        # Charged attack wears off.
        god_charged = False

    # If a move is not charged the boss performs a normal turn.
    else:
        # Result of 30 or less on the move roll means a charged attack
        # that will execute next turn, warning the player to defend.
        if god_move <= 30:
            print("\nThe Dodgeball God is gathering energy!")
            god_charged = True

        # A result between 31 and 40 causes the boss to activate a shield.
        # This shield reflects damage taken for 1 round.
        elif god_move <= 40:
            print("\nThe Dodgeball God creates a reflective shield! A barrier this powerful should only last for the next few moments!")
            current_enemy.shield_active = True

        # On a result of 41-100 the boss performs a normal attack.
        else:
            dodge_calc(player_character, current_enemy, eye_of_omens_counter)

    return god_charged, god_turn_counter

# random.choice is used to return a random move from the list.
def god_name_randomizer():
    return random.choice(god_move_names)

# God has some very intense moves, chosen randomly from this list.
god_move_names = [
    "Heavenly Dragon Buster, First Form!",
    "Ten Hands of Divine Punishment!",
    "Everlasting Flame of Creation!",
    "Black Python of the First Night!",
    "Stardust Genesis Burst!",
    "Ultimate Move of the Nuclear Sect: Sunsplitter Throw!",
    "Immortal's Whirlwind Sphere!",
    "Ten Thousand Golden Blades!",
    "Silver Hurricane of the Sea Dragon!",
    "Radiant Judgment of the Celestials!",
    "Red Crane's Final Flight!",
    "Infinity Rains From the Sky!",
    "Final Dream of the Scarlet Prince!"
]