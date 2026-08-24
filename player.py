"""This module holds the player class, the player's status displays, and a few functions used by the player,
such as the leveling function. Note that player_character is the generated player object."""

import utils
import items

# Player Core Stats. Be warned that hp and stamina are methods rather
# than integers, so they need parentheses when called in the future.
# Some of the attributes also start out as empty lists/dicts that get
# filled as the player acquires items.
# Later on we also added the player's consumables here and whether or
# not they have invulnerability on from using a spellcard.
class Player:
    def __init__(self):
        self.level = 12
        self.strength = 10
        self.precision = 10
        self.agility = 10
        self.endurance = 10
        self.demon_bonus_applied = 0
        self.eye_of_omens_counter = 0
        self.demon_counter = 0
        self.invulnerable = False
        self.player_turn = True
        self.exp = 0
        self.money = 80
        self.sardine_inventory = 3
        self.spellcard_inventory = 1
        self.owned_items = []
        self.effects = {}
        self.hp = self.max_hp()
        self.stamina = self.max_stamina()

    # Player Derived Stats. These are functions so they can be easily 
    # recalculated as the player levels up and increases stats.
    def max_hp(self) -> int:
        return 10 + (self.level * 2) + (self.endurance * 3)
    def max_stamina(self) -> int:
        return 10 + (self.level * 2) + (self.endurance // 2)
    def hp_regen(self) -> int:
        return (self.endurance // 10)
    def stamina_regen(self) -> int:
        return (self.endurance // 4)

    # I am turning the demon mode bonus into a function so we can make it
    # Scale with the player's level throughout the game, making it weaker
    # early but stronger later on.
    # The demon mode bonus is equal to half the player's level, starting at
    # +6 to all stats except endurance, and ending up around +50.
    def demon_bonus_result(player_character):
        return player_character.level // 2

# This function is meant to display the player's level, exp, HP, and stamina.
def stats_display(player_character):
    # We use the make_bar function above to display player values as bars.
    # Note that since max HP and max Stamina are methods we need to call them
    # with () so that the program will always recalculate the maximums.
    exp_bar = utils.make_bar(player_character.exp, 100, width=20)
    hp_bar = utils.make_bar(player_character.hp, player_character.max_hp(), width=20)
    stamina_bar = utils.make_bar(player_character.stamina, player_character.max_stamina(), width=20)
    print(f"\nLevel: {player_character.level} | {player_character.exp} / 100 {exp_bar}")
    print(f"HP: {player_character.hp} / {player_character.max_hp()} {hp_bar}") 
    print(f"Stamina: {player_character.stamina} / {player_character.max_stamina()} {stamina_bar}")

# This expanded status display shows the four player attributes.
def full_stats_display(player_character):
    print(f"\nStrength: {player_character.strength} | Precision: {player_character.precision} | Agility: {player_character.agility} | Endurance: {player_character.endurance} | Money: ${player_character.money}")
    # If the player picked up items with effects we display those too.
    if player_character.effects:
        print("---Active Effects ---")
        # This for loop runs for every distinct effect that has been added to
        # the player's inventory (pulls items from the player_character.effects dictionary).
        # plus their total potencies. The loop essentially unpacks the dictionary.
        for effect_name, potency in player_character.effects.items():
            # We then check if the effect listed is in the list of effects that
            # are percentage-based. If so we add a % at the end.
            if effect_name in items.percentage_effects:
                print(f"{effect_name}: {potency}%")
            else:
                print(f"{effect_name}: {potency}")
    else:
        print("No Active Effects")

# This dictionary holds the three attacks available to the player and
# their damage multipliers.
# Meteor shot does a considerable amount of extra damage while
# Helios Dive is an even more substantial finisher but costs a lot of
# stamina to compensate. I also considered adding a cooldown to it
# but at least for now decided not to.
attack_multipliers = {
    "Standard": 1.0,
    "Meteor": 1.5,
    "Helios": 2.5
}

# This function holds stamina costs so they can be more future-proofed.
# It now also adjusts the stamina if the player has any Graceful items.
# The way we're doing it like this rather than hardcoding them where they
# are used is to make it so they can be neatly modified in one location
# if we ever decide to modify or expand on them.
def stamina_costs(player_character, attack_key): 
    base_costs = {
    "1": 8,
    "2": 12,
    "3": 10,
    "4": 24
    }

    # We make a base_cost variable and call the adjusted_stamina_cost function
    # so that the Graceful item effect can give the player a stamina discount
    # if they have that.
    base_cost = base_costs[attack_key]
    return adjusted_stamina_cost(player_character, base_cost)

# This other function checks to see if the player actually has enough
# stamina to perform an action and it performs the action and deducts
# the cost. For this function we are going to be using another
# function as one of its arguments (effect) through the use of lambda.
# details on that further below.
def stamina_checker(player_character, cost, flavor_text, effect):
    # The checker first measures if the player has enough stamina,
    # then prints flavor text and performs an effect.
    # Then it deducts the stamina cost.
    if player_character.stamina >= cost:
        print(flavor_text)
        effect()
        player_character.stamina = player_character.stamina - cost
        return True
    else:
        print("Not enough stamina!")
        return False

# This function uses the graceful item effect to reduce stamina costs.
# Abilities that cost stamina will always have a minimum cost of 1.
# It takes the base_cost variable from stamina_costs for this operation.
# We use the .get() function to see if the player has the "graceful"
# effect and default its value to 0, but if they do have it then it will
# not be 0.
def adjusted_stamina_cost(player_character, base_cost):
    graceful_total = player_character.effects.get("graceful", 0)
    adjusted_cost = base_cost - graceful_total
    return max(1, adjusted_cost)

# Function that is called when the player levels up.
# They can choose one of their attributes to increase by 2.
# It uses the same kind of options display logic as the previous
# function but rather than executing effects the chosen option
# instead increases a player stat.
def level_up(player_character):
    options = {
        "1": "Strength. Throw harder!",
        "2": "Precision. Hit more, crit more!",
        "3": "Agility. Avoid damage!",
        "4": "Endurance. More health and stamina!"
        }
    for num, text in options.items():
        print(f"{num}) {text}")
    while True:
        level_up_increase = input("Increase a score by 2!")
        if level_up_increase in options:
            if level_up_increase == "1":
                player_character.strength = player_character.strength + 2
            elif level_up_increase == "2":
                player_character.precision = player_character.precision + 2
            elif level_up_increase == "3":
                player_character.agility = player_character.agility + 2
            elif level_up_increase == "4":
                player_character.endurance = player_character.endurance + 2
            break
        else:
            utils.slow_print("Your options range between 1 and 4!")