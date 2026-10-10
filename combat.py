"""This module handles the player options, the combat calculations, and the all-important
fight() function."""

import player
import utils
import enemies
import random

def player_options(combat_state):
    """This function presents the player with options and takes their input, then returns it.
    The options variable is a dictionary keying numbers to the options."""

    options = {
        "1": f"Basic Shot ({combat_state.player.stamina_costs('1')}). A simple throw.",
        "2": f"Meteor Shot ({combat_state.player.stamina_costs('2')}). Jump and throw from above!",
        "3": f"Eye of Omens ({combat_state.player.stamina_costs('3')}). Use your cursed eye to predict enemy movements!",
        "4": f"Helios Dive ({combat_state.player.stamina_costs('4')}). Unleash the power of the sun!",
        "5": "Demonic Art ~ Transcend Reason (1 Soul). Have faith in your evil.",
        "6": "Rest. Catch your breath and recover extra stamina.",
        "7": f"Eat sardines to recover your energy and maintain your physical form. You have {combat_state.player.sardine_inventory}.",
        "8": f"Use a spellcard ({combat_state.player.spellcard_inventory} available). 1 round of invulnerability plus deal guaranteed damage.",
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
def damage_calc(attack_type, combat_state):
    """This function calculates how much damage the player does with a solid hit."""
    # Attack type can multiply damage.
    multiplier = player.attack_multipliers[attack_type]
    # Damage takes both strength and level into account.
    # So even players with low strength will have a slightly higher max hit
    # as they level up.
    total_damage = (combat_state.player.strength + random.randint(1,combat_state.player.level)) * multiplier
    # Total Damage is affected by the Heroic Resolve item effect now.
    heroic_multiplier = heroic_resolve_calculator(combat_state)
    total_damage = total_damage * heroic_multiplier
    # Total damage is rounded before it is applied to prevent floats.
    total_damage = round(total_damage)
    
    # This is also where we now check if the dodgeball god's shield is active.
    # if so, the player's damage is reflected onto them on all three hit tiers.
    if getattr(combat_state.enemy, "shield_active", False):
        reflected_damage = total_damage
        combat_state.player.hp = combat_state.player.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    # If there is no shield, total damage is deducted from enemy HP and
    # on-hit effects like lifedrain are applied.
    # We return the damage for display.
    else:
        combat_state.enemy.hp = combat_state.enemy.hp - total_damage
        effects_on_hit(combat_state, total_damage, is_critical=False)
        return total_damage

def crit_calc(attack_type, combat_state):
    """This function uses the same damage calculation, but the result is doubled.
    It is called on critical strikes. Due to the way attack multiplies work
    Special attacks can be multiplied even more than that."""
    multiplier = player.attack_multipliers[attack_type]
    total_damage = ((combat_state.player.strength + random.randint(1,combat_state.player.level)) * 2) * multiplier
    heroic_multiplier = heroic_resolve_calculator(combat_state)
    total_damage = total_damage * heroic_multiplier
    total_damage = round(total_damage)

    if getattr(combat_state.enemy, "shield_active", False):
        reflected_damage = total_damage
        combat_state.player.hp = combat_state.player.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    else:
        combat_state.enemy.hp = combat_state.enemy.hp - total_damage
        # Note that unlike in the previous branches, is_critical is True in
        # this function. This enables Obliterate to trigger.
        effects_on_hit(combat_state, total_damage, is_critical=True)
        return total_damage

def graze_calc(attack_type, combat_state):
    """If the player came slightly short of a hit, they graze the enemy instead.
    This deals half damage and does not apply on-hit effects, unlike hits and crits."""
    multiplier = player.attack_multipliers[attack_type]
    total_damage = ((combat_state.player.strength + random.randint(1,combat_state.player.level)) // 2) * multiplier
    heroic_multiplier = heroic_resolve_calculator(combat_state)
    total_damage = total_damage * heroic_multiplier
    total_damage = round(total_damage)

    if getattr(combat_state.enemy, "shield_active", False):
        reflected_damage = total_damage
        combat_state.player.hp = combat_state.player.hp - reflected_damage
        print(f"The Dodgeball God's shield reflects your throw, dealing {reflected_damage} damage back at you!")
        return 0

    else:
        combat_state.enemy.hp = combat_state.enemy.hp - total_damage
        return total_damage

def hit_calc(attack_type, combat_state):
    """This is the function that calculates attack rolls.
    It determines if the player hits the enemy, and what quality of hit
    they accomplish (possibilities are crit, hit, graze, miss).
    With the starting precision value of 10 and no boosts, a player would have to
    roll 50 or higher to hit a hypothetical enemy with 10 agility.
    If the enemy has 15 agility this required roll would change to 100.
    Each point of precision translates to a 5% chance to upgrade an attack to
    the next tier of hit."""
    # The Eye of Omens grants a considerable flat boost to attack rolls
    # if active, equivalent to about 8 precision points.
    eye_of_omens_bonus = 0
    if combat_state.player.eye_of_omens_counter > 0:
        eye_of_omens_bonus = 40
    attack_roll = (combat_state.player.precision * 5) + random.randint(0,100) + eye_of_omens_bonus
    # The Helios Dive attack has +25 on attack rolls also.
    # Equivalent to 5 precision points.
    if attack_type == "Helios":
        attack_roll = attack_roll + 25
        
    armor_class = (combat_state.enemy.agility * 10)
    hit_result = "miss"

    print(f"\nYour Attack Roll = {attack_roll}. Enemy Armor Class = {armor_class}.")

    # The player crits if their attack roll exceeds enemy AC by at least 30.
    # They graze if they miss by less than 30.
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
    accurate_total = combat_state.player.effects.get("accurate", 0)
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
        damage_report = crit_calc(attack_type, combat_state)
        utils.slow_print(f"Critical Hit! You hit for {damage_report}!")
        if attack_type == "Meteor":
            stun_check(combat_state.enemy, chance=33)
    elif hit_result == "hit":
        damage_report = damage_calc(attack_type, combat_state)
        utils.slow_print(f"Hit! You hit for {damage_report}!")
        if attack_type == "Meteor":
            stun_check(combat_state.enemy, chance=25)
    elif hit_result == "graze":
        damage_report = graze_calc(attack_type, combat_state)
        utils.slow_print(f"Graze! You hit for {damage_report}!")

    # If the player misses, they can get a special message if their
    # enemy was a kaiju. After all, how do you miss such a large target?
    elif hit_result == "miss":
        if combat_state.enemy.type == "Kaiju":
            print("Your throw was too weak to harm the kaiju!")
        else:
            utils.slow_print("Miss!")

def effects_on_hit(combat_state, total_damage, is_critical=False):
    """This function handles effects that apply after the player deals damage to
    an enemy with their attacks, such as lifesteal and obliterate."""
    lifesteal_total = combat_state.player.effects.get("lifesteal", 0)
    echo_hit_total = combat_state.player.effects.get("echo hit", 0)
    obliterate_total = combat_state.player.effects.get("obliterate", 0)

    # Lifesteal heals the player for a percentage of the damage taken.
    # So the function adds the total potency from the player's items together.
    # Then if the player has any lifesteal it calculates the amount of hp healed.
    # by first dividing the lifesteal total by 100 and multiplying the damage
    # dealt by the result. There is anti-overheal protection here too.
    if lifesteal_total > 0:
        heal_amount = int(total_damage * (lifesteal_total / 100))
        combat_state.player.hp = min((combat_state.player.hp + heal_amount), combat_state.player.max_hp())
        print(f"You drain health from the enemy and healed for {heal_amount} hp!")

    # Echo hits roll additional attacks on hit if the player succeeds at a % roll.
    # It is possible to chain echo hits.
    if echo_hit_total > 0:
        if random.randint(0,100) <= echo_hit_total:
            print("You hit again!")
            echo_hit_damage = damage_calc("Standard", combat_state)
            print(f"The echo hit deals {echo_hit_damage} additional damage!")

    # Obliterate has a % chance of instantly slaying the enemy. It ends with return
    # to stop further processes. It only triggers on critical hits, which we now
    # check for.
    if is_critical and obliterate_total > 0:
        if random.randint(0,100) <= obliterate_total:
            if combat_state.enemy.type == "Dodgeball God":
                print("Even god cannot withstand your power and is obliterated.")
            else:
                print("OBLITERATED!")
            combat_state.enemy.hp = 0
            return

def heroic_resolve_calculator(combat_state):
    """This is one of the mathier functions, which calculates the bonus damage
    from Heroic Resolve. While the player has Heroic Resolve among their item
    effects they deal more damage as their HP is lower, up to a maximum of
    around double damage with all relevant items equipped.
    The formula is similar to the one for the iconic OSRS Dharok set, but
    modified for a game where HP can go well above 99."""
    resolve_total = combat_state.player.effects.get("heroic resolve", 0)
    max_hp = combat_state.player.max_hp()
    missing_percentage = (max_hp - combat_state.player.hp) / max_hp
    heroic_bonus = 1 + missing_percentage * (resolve_total / 100)
    return heroic_bonus

def effects_on_damage_taken(combat_state, damage_report):
    """This one applies effects when the player is hit.
    We take damage_report in the arguments to use for retribution."""
    retribution = combat_state.player.effects.get("retribution", 0)
    resilient = combat_state.player.effects.get("resilient", 0)

    # The retribution effect deals a percentage of damage taken
    # back to attackers.
    if retribution > 0:
        ret_damage = int(damage_report * (retribution / 100))
        combat_state.enemy.hp = combat_state.enemy.hp - ret_damage
        print(f"The enemy takes {ret_damage} damage from Retribution!")

    # Resilient gives the player a chance to survive lethal damage
    # with 1 HP remaining.
    if resilient > 0:
        if combat_state.player.hp - damage_report <= 0:
            if random.randint(0,100) <= resilient:
                combat_state.player.hp = 1
                print("You are still standing!")

# These functions mirror the player calculation ones, but roll enemy damage.
def enemy_damage_calc(combat_state):
    """Uses the minimum and maximum damage values in an enemy class to
    roll damage dealt to the player on hit."""
    total_damage = random.randint(combat_state.enemy.damage_min, combat_state.enemy.damage_max)
    combat_state.player.hp = combat_state.player.hp - total_damage
    return total_damage

def enemy_graze_calc(combat_state):
    """Rolls damage dealt to the player when the enemy grazes them."""
    total_damage = (random.randint(combat_state.enemy.damage_min, combat_state.enemy.damage_max) // 2)
    combat_state.player.hp = combat_state.player.hp - total_damage
    return total_damage

def stun_check(current_enemy, chance=25):
    """This small function rolls a stun chance percentage used by hit_calc().
    It gives Meteor Shot a chance to stun enemies it successfully hits.
    Their stun status is then checked. The default stun chance is 25% but 
    crits are given an argument boosting that to 33%."""
    if random.randint(1, 100) <= chance:
        current_enemy.stunned = True
        utils.slow_print(f"{current_enemy.type} is stunned by the attack!")
        
def dodge_calc(combat_state):
    """This is partially a mirrored hit_calc().
    Except it rolls the chance for the player to be hit by the enemy.
    The Eye of Omens bonus applies defensively here.
    And enemies are unable to score critical hits."""
    attack_roll = (combat_state.enemy.precision * 5) + random.randint(0,100)
    eye_of_omens_bonus = 0
    
    if combat_state.player.eye_of_omens_counter > 0:
        eye_of_omens_bonus = 40
        
    armor_class = (combat_state.player.agility * 10) + eye_of_omens_bonus

    print(f"\nThe enemy's Attack Roll = {attack_roll}. Your Armor Class = {armor_class}.")

    # If the player has used a spellcard to gain invulnerability
    # that is checked first and damage is not rolled even on a hit.
    if combat_state.player.invulnerable is True:
        print("The spellcard negates all damage!")
    elif attack_roll >= armor_class:
        damage_report = enemy_damage_calc(combat_state)
        utils.slow_print(f"The dodgeball hits you! You take {damage_report} damage!")
        effects_on_damage_taken(combat_state, damage_report)
    elif attack_roll >= armor_class - 30:
        damage_report = enemy_graze_calc(combat_state)
        utils.slow_print(f"The dodgeball grazes you! You take {damage_report} damage!")
        effects_on_damage_taken(combat_state, damage_report)
    else:
        utils.slow_print("You catch the dodgeball!")

def activate_eye_of_omens(combat_state):
    base_duration = 3
    time_control_bonus = combat_state.player.effects.get("time control", 0)
    total_duration = base_duration + time_control_bonus
    combat_state.player.eye_of_omens_counter = total_duration
    if time_control_bonus > 0:
        print("Your mastery over time extends the effect!")

class CombatState:
    """This class tracks the variables used in combat.
    It refers to the player and current enemy so those objects are updated.
    And then it also keeps track of whether the dodgeball god has charged
    an attack and whether it is due for a power boost.
    It also logs the result variable to track if the player has won or lost."""
    def __init__(self, player_character, current_enemy):
        self.player = player_character
        self.enemy = current_enemy
        self.god_charged = False
        self.god_turn_counter = 0
        self.result = None

def fight(game_state, combat_state):
    """Core function that initiates and handles combat with the rolled enemy."""
    # it starts a loop to have both player and enemy stats on display every turn.
    # The player's turn always happens first.
    while True:
        enemies.enemy_stats_display(combat_state.enemy)
        player.stats_display(combat_state.player)
        combat_state.player.invulnerable = False

        # The loop is set to immediately break if the player hits 0 HP.
        # If the enemy reaches 0 HP instead the player gets experience,
        # the overlord counter decreases, and the player potentially levels up.
        if combat_state.player.hp < 1:
            defeat_message = enemies.get_defeat_message(combat_state.enemy.type)
            utils.slow_print(defeat_message)
            break
        elif combat_state.enemy.hp < 1:
            # If the enemy was god, the game is won.
            if combat_state.enemy.type == "Dodgeball God":
                utils.slow_print(combat_state.enemy.defeat)
                utils.slow_print("The Dodgeball God has fallen...")
                utils.slow_print("You have created a new age of Dodgeball Demons and are now the supreme overlord!")
                return "GOD_DEFEATED"
                
            utils.slow_print("\n" + combat_state.enemy.defeat)
            utils.slow_print("Victory!")
            crow_total = combat_state.player.effects.get("crow", 0)
            combat_state.player.exp = combat_state.player.exp + combat_state.enemy.exp_reward

            # If the player has the crow effect, rewards are increased
            # and a sardine may be received as a random drop.
            if crow_total > 0:
                base_money_reward = combat_state.enemy.money_reward
                crow_bonus_money = int(base_money_reward * (crow_total / 100))
                total_money_reward = base_money_reward + crow_bonus_money
                combat_state.player.money = combat_state.player.money + total_money_reward
                print(f"You found ${total_money_reward}! Your crow-like nature contributed ${crow_bonus_money}.")
    
                if random.randint(0,100) <= (crow_total):
                    combat_state.player.sardine_inventory += 1
                    print(f"Your fellow crows bring you a sardine! You now have {combat_state.player.sardine_inventory}.")
            else:
                combat_state.player.money = combat_state.player.money + combat_state.enemy.money_reward

            # If it was an overlord, spellcards are awareded.
            if combat_state.enemy.type in ["Dodgeball Overlord", "Badass Freakin' Overlord"]:
                combat_state.player.spellcard_inventory += 1
                utils.slow_print(f"You have earned a Spellcard! You now have {combat_state.player.spellcard_inventory}.")
            
            game_state.next_overlord = game_state.next_overlord - 1
            game_state.next_shop = game_state.next_shop - 1
            game_state.fight_god = game_state.fight_god - 1
            utils.slow_print(f"\nThe next Dodgeball Overlord is {game_state.next_overlord} battles away!")
            utils.slow_print(f"The next shop is {game_state.next_shop} battles away!")
            if combat_state.player.exp >= 100:
                combat_state.player.level = combat_state.player.level + 1
                combat_state.player.exp = combat_state.player.exp - 100
                player.full_stats_display(combat_state.player)
                player.level_up(combat_state.player)

            # current_enemy returns to 0, rolling another enemy.
            result = 0
            game_state.current_enemy = 0
            return result

        # This loop is active while it is the player's turn.
        # Their buff counters decrease at the start of the turn if not at 0,
        # and the player is then free to use their actions.
        while combat_state.player.player_turn and combat_state.enemy.hp > 0:
            print("")
            player_move = player_options(combat_state)
            
            # Each attack is keyed to a dictionary above that matches its stamina cost and
            # runs the attack roll through lambda.
            if player_move == "1":
                if player.stamina_checker(combat_state.player, combat_state.player.stamina_costs('1'), "You throw the dodgeball!", lambda: hit_calc("Standard", combat_state)):
                    combat_state.player.player_turn = False
                    
            elif player_move == "2":
                if player.stamina_checker(combat_state.player, combat_state.player.stamina_costs('2'), "You jump and slam the dodgeball into the enemy!", lambda: hit_calc("Meteor", combat_state)):
                    combat_state.player.player_turn = False
                    
            elif player_move == "3":
                if player.stamina_checker(combat_state.player, combat_state.player.stamina_costs('3'), "Your magical eye grants you precognition!", lambda: activate_eye_of_omens(combat_state)):
                    combat_state.player.player_turn = False
                    
            elif player_move == "4":
                if player.stamina_checker(combat_state.player, combat_state.player.stamina_costs('4'), "You throw a ball imbued with the power and malevolence of the sun!", lambda: hit_calc("Helios", combat_state)):
                    combat_state.player.player_turn = False

            # Moves 3 and 5 boost the player's stats temporarily instead, and move 5 is
            # a free action that does not end the player's turn, but does reduce their
            # HP to 1. The player can also rest if out of stamina for other actions,
            # or view their attributes for free.
            elif player_move == "5":
                if combat_state.player.demon_counter == 0:
                    combat_state.player.hp = 1
                    base_duration = 3
                    time_control_bonus = combat_state.player.effects.get("time control", 0)
                    total_duration = base_duration + time_control_bonus
                    combat_state.player.demon_counter = total_duration
                    utils.slow_print(f"\nThe darkness takes you! Your enhanced state will last for {combat_state.player.demon_counter} turns!")
                    if time_control_bonus > 0:
                        print("Your mastery over time extends the effect!")
                    combat_state.player.demon_bonus_applied = combat_state.player.demon_bonus_result(combat_state.player)
                    combat_state.player.strength = combat_state.player.strength + combat_state.player.demon_bonus_applied
                    combat_state.player.precision = combat_state.player.precision + combat_state.player.demon_bonus_applied
                    combat_state.player.agility = combat_state.player.agility + combat_state.player.demon_bonus_applied
                else:
                    print("You are already transformed!")
                    
            elif player_move == "6":
                combat_state.player.stamina = combat_state.player.stamina + (combat_state.player.stamina_regen() * 3)
                combat_state.player.player_turn = False
                
            elif player_move == "7":
                if combat_state.player.sardine_inventory > 0:
                    combat_state.player.sardine_inventory = combat_state.player.sardine_inventory - 1
                    combat_state.player.hp = combat_state.player.max_hp()
                    combat_state.player.stamina = combat_state.player.max_stamina()
                    utils.slow_print("You eat the sardines. They taste like victory.")
                    if combat_state.player.effects.get("hungry beast", 0) == 0:
                        combat_state.player.player_turn = False
                    elif combat_state.player.effects.get("hungry beast", 0) > 0:
                        print("You devour the sardines quickly!")
                else:
                    print("You are out of sardines!")

            elif player_move == "8":
                if combat_state.player.spellcard_inventory > 0:
                    combat_state.player.spellcard_inventory = combat_state.player.spellcard_inventory - 1
                    combat_state.player.hp = combat_state.player.hp - (combat_state.player.level * 2)
                    combat_state.player.invulnerable = True
                    utils.slow_print("You become invulnerable for a brief time and unleash a powerful attack!")
                    combat_state.player.player_turn = False
                else:
                    print("You are out of spellcards!")
                    
            elif player_move == "9":
                player.full_stats_display(combat_state.player)

            # The following code uses min() to regenerate the player's HP and stamina
            # up to but not exceeding their maximum values. This prevents overheal.
            # We want this regen to happen after the player's turn but before the enemy
            # attacks as a mercy to the player.
            hp_regen_bonus = 0
            stamina_regen_bonus = 0
            if combat_state.player.demon_counter > 0:
                hp_regen_bonus = 5
                stamina_regen_bonus = 10
            combat_state.player.hp = min(combat_state.player.hp + combat_state.player.hp_regen() + hp_regen_bonus, combat_state.player.max_hp())
            combat_state.player.stamina = min(combat_state.player.stamina + combat_state.player.stamina_regen() + stamina_regen_bonus, combat_state.player.max_stamina())

        # Once the player's turn ends, the enemy performs a simple attack and
        # The player can move again. If the enemy is stunned
        # then their turn is skipped, and if they enemy is
        # god then it uses a different set of actions instead of
        # only basic attacks.
        if combat_state.player.player_turn is False and combat_state.enemy.hp > 0:
            if getattr(combat_state.enemy, "stunned", False):
                print("The enemy is stunned and cannot attack!")
                combat_state.enemy.stunned = False
            elif combat_state.enemy.type == "Dodgeball God":
                god_actions(combat_state)
            
            else:
                utils.slow_print(f"{combat_state.enemy.type} throws a dodgeball at you!")
                dodge_calc(combat_state)
            combat_state.player.player_turn = True

        # The buff duration decrements were moved here so they'll run
        # correctly even if the player checks their stats.
        if combat_state.player.eye_of_omens_counter > 0:
            combat_state.player.eye_of_omens_counter = combat_state.player.eye_of_omens_counter - 1
            if combat_state.player.eye_of_omens_counter == 0:
                utils.slow_print("Your precognition ends.")
        if combat_state.player.demon_counter > 0:
            combat_state.player.demon_counter = combat_state.player.demon_counter - 1
            if combat_state.player.demon_counter == 0:
                combat_state.player.strength = combat_state.player.strength - combat_state.player.demon_bonus_applied
                combat_state.player.precision = combat_state.player.precision - combat_state.player.demon_bonus_applied
                combat_state.player.agility = combat_state.player.agility - combat_state.player.demon_bonus_applied
                combat_state.player.demon_bonus_applied = 0
                utils.slow_print("The darkness releases you!")
        print("-" * 40)

    return "PLAYER_DEFEATED"

def god_actions(combat_state):
    """This function handles the dodgeball god's behavior.
    It is intended to be a two-phase fight against an opponent
    who grows stronger over time."""

    # The enemy's shield special turns off at the start of its next turn if it was active.
    combat_state.enemy.shield_active = False

    # The god turn counter increases by 1 each turn.
    combat_state.god_turn_counter = combat_state.god_turn_counter + 1

    # Every 3 turns, the boss powers up permanently, creating a DPS race.
    if combat_state.god_turn_counter % 3 == 0:
        print("\nThe Dodgeball God removes a power limiter and grows stronger!")
        combat_state.enemy.damage_min = combat_state.enemy.damage_min + 10
        combat_state.enemy.damage_max = combat_state.enemy.damage_max + 10
        combat_state.enemy.precision = combat_state.enemy.precision + 10
    
    god_move = random.randint(0,100)

    # Boss becomes stronger below half health but does not gain new moves.
    if combat_state.enemy.hp < (combat_state.enemy.max_hp // 2) and combat_state.enemy.phase_2 is False:
        print("\n'You dare?! We are as different as Heaven and Earth!'")
        combat_state.enemy.phase_2 = True
        combat_state.enemy.damage_min = combat_state.enemy.damage_min + 30
        combat_state.enemy.damage_max = combat_state.enemy.damage_max + 30
        combat_state.enemy.precision = combat_state.enemy.precision + 50

    # If the boss charged an attack last turn, we want that to
    # fire on this turn, dealing heavy damage.
    # This attack will have a randomized name chosen from the list.
    if combat_state.god_charged is True:
        chosen_move_name = god_name_randomizer()
        utils.slow_print("\nThe Dodgeball God unleashes their special move!")
        utils.slow_print(f'{chosen_move_name}')

        # We store the boss' current damage range to reset later.
        original_damage_min = combat_state.enemy.damage_min
        original_damage_max = combat_state.enemy.damage_max

        # We then double its current values.
        combat_state.enemy.damage_min = combat_state.enemy.damage_min * 2
        combat_state.enemy.damage_max = combat_state.enemy.damage_max * 2

        # We roll an attack. Because its damage range on its class
        # is boosted the damage in this calculation will also be.
        dodge_calc(combat_state)

        # Original damage range restored for subsequent turns.
        combat_state.enemy.damage_min = original_damage_min
        combat_state.enemy.damage_max = original_damage_max

        # Charged attack wears off.
        combat_state.god_charged = False

    # If a move is not charged the boss performs a normal turn.
    else:
        # Result of 30 or less on the move roll means a charged attack
        # that will execute next turn, warning the player to defend.
        if god_move <= 30:
            print("\nThe Dodgeball God is gathering energy!")
            combat_state.god_charged = True

        # A result between 31 and 40 causes the boss to activate a shield.
        # This shield reflects damage taken for 1 round.
        elif god_move <= 40:
            print("\nThe Dodgeball God creates a reflective shield! A barrier this powerful should only last for the next few moments!")
            combat_state.enemy.shield_active = True

        # On a result of 41-100 the boss performs a normal attack.
        else:
            dodge_calc(combat_state)

def god_name_randomizer():
    """The random.choice function is used to return a random move from the list."""
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