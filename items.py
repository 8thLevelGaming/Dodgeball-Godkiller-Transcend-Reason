# Item Pool Dictionary.
# This dictionary stores values that are themselves dictionaries.
# The simpler ones follow the format:
# str:"Item Name": { "boosts": [{"stat": "stat_name", "amount": int}], "rarity": "rarity_tier"
# By using "boosts" like this we can assign multiple different {stat/amount} values within
# the square brackets and create items that boost multiple stats.
# We are doing it like this so we can uset setattr() and getattr()
# In addition to "boosts" and "rarity" we also have "special" to record a special
# effect the item has beyond just increasing stats.
item_pool = {
# Common Items. Current count: 21
    "Fingerless Gloves": {
        "boosts": [
            {"stat":"strength", "amount": 4,}],
        "rarity": "common"},
    
    "Black Eyepatch": {
        "boosts": [
            {"stat": "precision", "amount": 4}], 
        "rarity": "common"},
    
    "Heroic Red Scarf": {
        "boosts": [
            {"stat": "agility", "amount": 2}], 
        "special": {"name": "heroic resolve", "potency": 10},
        "rarity": "common"},

    "Princely Cape": {
        "boosts": [
            {"stat": "precision", "amount": 2}], 
        "special": {"name": "heroic resolve", "potency": 10},
        "rarity": "common"},
    
    "Tough Tank Top": {
        "boosts": [
            {"stat": "endurance", "amount": 4}], 
        "rarity": "common"},
    
    "Mysterious Face Mask": {
        "boosts": [
            {"stat": "agility", "amount": 1},
            {"stat": "endurance", "amount": 1}], 
        "special": {"name": "crow", "potency": 5},
        "rarity": "common"},

    "Cute Glasses": {
        "boosts": [
            {"stat": "precision", "amount": 2}],
        "special": {"name": "accurate", "potency": 5},
        "rarity": "common"},

    "Sporty Shorts": {
        "boosts": [
            {"stat": "strength", "amount": 2},
            {"stat": "endurance", "amount": 2}], 
        "rarity": "common"},

    "Fursona": {
        "boosts": [
            {"stat": "strength", "amount": 1},
            {"stat": "precision", "amount": 1},
            {"stat": "agility", "amount": 1},
            {"stat": "endurance", "amount": 1}], 
        "rarity": "common"},

    "Cool Bandana": {
        "boosts": [
            {"stat": "strength", "amount": 1}],
        "special": {"name": "echo hit", "potency": 5}, 
        "rarity": "common"},

    "Running Shoes": {
        "boosts": [
            {"stat": "agility", "amount": 1}], 
        "special": {"name": "graceful", "potency": 2},
        "rarity": "common"},

    "Curl Cream": {
        "boosts": [
            {"stat": "precision", "amount": 1},
            {"stat": "agility", "amount": 1},
            {"stat": "endurance", "amount": 2}],
        "rarity": "common"},

    "Crab Claw": {
        "boosts": [
            {"stat": "strength", "amount": 1},
            {"stat": "endurance", "amount": 3}],
        "rarity": "common"},

    "Cute Mandibles": {
        "boosts": [
            {"stat": "strength", "amount": 3},
            {"stat": "precision", "amount": 1}],
        "rarity": "common"},

    "Tentacle": {
        "boosts": [
            {"stat": "strength", "amount": 1},
            {"stat": "precision", "amount": 3}],
        "rarity": "common"},

    "Bat Familiar": {
        "boosts": [
            {"stat": "precision", "amount": 1}], 
        "special": {"name": "lifesteal", "potency": 5},
        "rarity": "common"},

    "Crow Familiar": {
        "boosts": [
            {"stat": "precision", "amount": 2}], 
        "special": {"name": "crow", "potency": 5},
        "rarity": "common"},

    "Hedgehog Buddy": {
        "boosts": [
            {"stat": "endurance", "amount": 1}], 
        "special": {"name": "retribution", "potency": 10},
        "rarity": "common"},

    "Shielding Parasol": {
        "boosts": [
            {"stat": "endurance", "amount": 1}], 
        "special": {"name": "resilient", "potency": 3},
        "rarity": "common"},

    "Physical Full Burst": {
        "boosts": [
            {"stat": "agility", "amount": 1}], 
        "special": {"name": "time control", "potency": 1},
        "rarity": "common"},

    "Autism Diagnosis": {
        "boosts": [
            {"stat": "precision", "amount": 1}],
        "special": {"name": "echo hit", "potency": 3},
        "rarity": "common"},

# Uncommon Items. Current count: 22
    "Dog Paw Gloves": {
        "boosts": [
            {"stat": "strength", "amount": 4},
            {"stat": "agility", "amount": 4}],
        "rarity": "uncommon"},

    "T-34 Tank": {
        "boosts": [
            {"stat": "strength", "amount": 4},
            {"stat": "endurance", "amount": 4}],
        "rarity": "uncommon"},

    "Amulet of Fury": {
        "boosts": [
            {"stat": "strength", "amount": 3},
            {"stat": "precision", "amount": 3},
            {"stat": "endurance", "amount": 2}],
        "rarity": "uncommon"},

    "Cloak of Shadows": {
        "boosts": [
            {"stat": "agility", "amount": 4},
            {"stat": "endurance", "amount": 2}],
        "special": {"name": "crow", "potency": 5},
        "rarity": "uncommon"},

    "Tornado Hand": {
        "boosts": [
            {"stat": "strength", "amount": 4},
            {"stat": "precision", "amount": 4}], 
        "rarity": "uncommon"},

    "Valkyrie Helm": {
        "boosts": [
            {"stat": "strength", "amount": 8}],
        "rarity": "uncommon"},

    "Cat Eyes": {
        "boosts": [
            {"stat": "precision", "amount": 4}],
        "special": {"name": "accurate", "potency": 10},
        "rarity": "uncommon"},

    "Rabbit Ears of Agility": {
        "boosts": [
            {"stat": "agility", "amount": 8}],
        "rarity": "uncommon"},

    "Graceful Outfit": {
        "boosts": [
            {"stat": "agility", "amount": 4}],
        "special": {"name": "graceful", "potency": 4},
        "rarity": "uncommon"},
    
    "Rune Platebody": {
        "boosts": [
            {"stat": "endurance", "amount": 8}],
        "rarity": "uncommon"},

    "Estus Flask": {
        "boosts": [
            {"stat": "agility", "amount": 2},
            {"stat": "endurance", "amount": 6}],
        "rarity": "uncommon"},

    "Vampire Fang": {
        "boosts": [
            {"stat": "strength", "amount": 3}],
        "special": {"name": "lifesteal", "potency": 10},
        "rarity": "uncommon"},

    "Bulwark of Thorns": {
        "boosts": [
            {"stat": "endurance", "amount": 3}],
        "special": {"name": "retribution", "potency": 25},
        "rarity": "uncommon"},

    "Void Wing Nouliths": {
        "boosts": [
            {"stat": "precision", "amount": 5}],
        "special": {"name": "echo hit", "potency": 5},
        "rarity": "uncommon"},

    "Cursed War Dolls": {
        "boosts": [
            {"stat": "precision", "amount": 3}],
        "special": {"name": "echo hit", "potency": 10},
        "rarity": "uncommon"},

    "Dark Aura": {
        "boosts": [
            {"stat": "strength", "amount": 3},
            {"stat": "agility", "amount": 2},
            {"stat": "endurance", "amount": 3}],
        "rarity": "uncommon"},

    "Badass Scythe": {
        "special": {"name": "obliterate", "potency": 4},
        "rarity": "uncommon"},

    "Yokai Dowsing Rod": {
        "special": {"name": "crow", "potency": 20},
        "rarity": "uncommon"},

    "Mini-Hakkero": {
        "boosts": [
            {"stat": "strength", "amount": 4}],
        "special": {"name": "obliterate", "potency": 2},
        "rarity": "uncommon"},

    "Occult Medicine Box": {
        "boosts": [
            {"stat": "endurance", "amount": 3}], 
        "special": {"name": "resilient", "potency": 6},
        "rarity": "uncommon"},

    "Perfect Maid's Pocket Watch": {
        "boosts": [
            {"stat": "precision", "amount": 2},
            {"stat": "agility", "amount": 2}],
        "special": {"name": "time control", "potency": 2},
        "rarity": "uncommon"},

    "Dharok's Armor": {
        "boosts": [
            {"stat": "strength", "amount": 2},
            {"stat": "endurance", "amount": 2}],
        "special": {"name": "heroic resolve", "potency": 30},
        "rarity": "uncommon"},

# Rare Items. Current count: 17
    "Cursed Armor: Muramasa": {
        "boosts": [
            {"stat": "strength", "amount": 8},
            {"stat": "precision", "amount": 4},
            {"stat": "agility", "amount": 4},
            {"stat": "endurance", "amount": 8}],
        "rarity": "rare"},

    "Blessed Armor: Masamune": {
        "boosts": [
            {"stat": "strength", "amount": 4},
            {"stat": "precision", "amount": 2},
            {"stat": "agility", "amount": 4},
            {"stat": "endurance", "amount": 6}],
        "special": {"name": "heroic resolve", "potency": 50},
        "rarity": "rare"},

    "Devourlord's Arm": {
        "boosts": [
            {"stat": "strength", "amount": 10}],
        "special": {"name": "lifesteal", "potency": 25},
        "rarity": "rare"},

    "Gate of Babylon": {
        "boosts": [
            {"stat": "strength", "amount": 5}],
        "special": {"name": "echo hit", "potency": 25},
        "rarity": "rare"},

    "Fragarach: The Answerer": {
        "boosts": [
            {"stat": "strength", "amount": 10}],
        "special": {"name": "retribution", "potency": 100},
        "rarity": "rare"},

    "Overlord Cape": {
        "boosts": [
            {"stat": "strength", "amount": 4},
            {"stat": "precision", "amount": 8},
            {"stat": "agility", "amount": 8},
            {"stat": "endurance", "amount": 4}],
        "rarity": "rare"},

    "Moonlight Greatsword": {
        "boosts": [
            {"stat": "strength", "amount": 10},
            {"stat": "precision", "amount": 4}],
        "rarity": "rare"},

    "Legendary Ninja Uniform": {
        "boosts": [
            {"stat": "precision", "amount": 6},
            {"stat": "agility", "amount": 8}],
        "special": {"name": "crow", "potency": 15},
        "rarity": "rare"},

    "Sealed Arm of the Fallen Hero": {
        "boosts": [
            {"stat": "strength", "amount": 6},
            {"stat": "precision", "amount": 6},
            {"stat": "agility", "amount": 6},
            {"stat": "endurance", "amount": 6}],
        "rarity": "rare"},

    "Mystic Eyes of Death Perception": {
        "boosts": [
            {"stat": "precision", "amount": 10}],
        "special": {"name": "obliterate", "potency": 10},
        "rarity": "rare"},

    "Brahmashirastra": {
        "boosts": [
            {"stat": "strength", "amount": 10}],
        "special": {"name": "obliterate", "potency": 10},
        "rarity": "rare"},

    "Corrupted Shark": {
        "boosts": [
            {"stat": "endurance", "amount": 10}],
        "special": {"name": "hungry beast", "potency": 1},
        "rarity": "rare"},

    "Skull of Mondain": {
        "boosts": [
            {"stat": "strength", "amount": 14}],
        "rarity": "rare"},

    "Amulet of Bloodfury": {
        "boosts": [
            {"stat": "strength", "amount": 3},
            {"stat": "precision", "amount": 3},
            {"stat": "endurance", "amount": 3}],
        "special": {"name": "lifesteal", "potency": 15},
        "rarity": "rare"},

    "Hourai Elixir": {
        "boosts": [
            {"stat": "endurance", "amount": 10}], 
        "special": {"name": "resilient", "potency": 12},
        "rarity": "rare"},

    "Chrono Trigger": {
        "boosts": [
            {"stat": "endurance", "amount": 5}], 
        "special": {"name": "time control", "potency": 3},
        "rarity": "rare"},

    "Nemesis Eye": {
        "boosts": [
            {"stat": "precision", "amount": 5}], 
        "special": {"name": "accurate", "potency": 20},
        "rarity": "rare"},
}

# The item's price is based on its rarity. These values are stored below.
rarity_prices = {
    "common": 100,
    "uncommon": 150,
    "rare": 200
}

# A list of item special effects that are percentage-based.
# We are making a record of these because in some displays
# we want to display a % sign after the item's potency.
# But only if it is a percentage effect rather than a
# flat value like the Graceful effect.
percentage_effects = [
    "lifesteal",
    "retribution",
    "echo hit",
    "obliterate",
    "resilient",
    "heroic resolve",
    "accurate",
    "crow"
]

# The fourth and fifth lines grab the stat's name (capitalized) and the boost amount.
# Then there is an if/else loop. If the item provides a bonus it will be added to the
# empty list as a string made up of the name and value, with a + sign.
# The else: branch is mostly meant for future-proofing in case I want to add items that
# reduce a stat in favor of another in the future, or modify existing items to do that.
#After that we add another if statement that will check for fancier effects later
# versions of the program hope to implement.
# The final line uses .join() to combine the strings in the effects list into one, 
# separated by commas.
# This function is used to display the effects of items in the shop.
def item_effects_display (item_name):
    
    # The first lines within the function grabs an item's data 
    # from the item_pool dictionary and make an effects list.
    details = item_pool[item_name]
    effects = []
    # The loop populates the effects list with the item's boosts, if any.
    # It pretty much unpacks them from the item and if it finds boosts
    # it shows the capitalized stat name and amount.
    if "boosts" in details:
        for boost in details["boosts"]:
            stat_name = boost["stat"].capitalize()
            amount = boost["amount"]
            if amount > 0:
                effects.append(f"{stat_name} +{amount}")
            else:
                effects.append(f"{stat_name} {amount}")

    # If the item has special effects it displays that too.
    # In the same way, but with a % symbol only if the item
    # is in our list of % effects.
    if "special" in details:
        special_name = details["special"]["name"].capitalize()
        special_potency = details["special"]["potency"]
        if details["special"]["name"] in percentage_effects:
            effects.append(f"{special_name} {special_potency}%")
        else:
            effects.append(f"{special_name} {special_potency}")

    # We separate the effects with a comma and space.
    return ", ".join(effects)

# This function collects an item's price based on its rarity.
# It is given the item_name argument and then it looks up its
# rarity in the item pool, using that to determine its price.
def item_price(item_name):
    return rarity_prices[item_pool[item_name]["rarity"]]

# I have moved the application of item effects to the player into its own
# function to keep the code DRY and neat.
def apply_item_effects(item_name):
    details = item_pool[item_name]

    # It collects the data from items in the pool and uses
    # setattr and getattr to update the player's stats by the correct amount.
    # These functions can be used to neatly update object attributes.
    # In this case the object argument (player) is updated by the attribute
    # parameter (item_effect["stat"]) and the amount is obtained through
    # getattr to get the item's "amount".
    if "boosts" in details:
        for item_effect in details["boosts"]:
            setattr(player, item_effect["stat"], getattr(player, item_effect["stat"]) + item_effect["amount"])
    # There is also a condition where if the item has special effects,
    # those will be added to the player's active effects and two effects of
    # the same type will stack their potency additively.
    if "special" in details:
        effect_name = details["special"]["name"]
        effect_potency = details["special"]["potency"]

        player.effects[effect_name] = player.effects.get(effect_name, 0) + effect_potency
    player.owned_items.append(item_name)