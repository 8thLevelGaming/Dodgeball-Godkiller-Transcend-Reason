# This is where the list of enemy classes starts.
# Note that we are giving them both minimum and maximum damage values.
# This is so we can use them as the randint range later.
# They have semi-randomized money and experience rewards.
# I have also given each enemy a short message that plays on defeat.
# As a reminder, a player's starting stats give them 100 AC and
# +50 on attack rolls.

# This is an agile enemy with 140 AC and +75 on attack rolls.
class AgileFoe:
    def __init__(self):
        self.type = "Agile Foe"
        self.hp = 15 + random.randint(5,15)
        self.damage_min = 4
        self.damage_max = 12
        self.precision = 15
        self.agility = 14
        self.exp_reward = 25 + random.randint(5, 10)
        self.money_reward = random.randint(15, 25)
        self.defeat = "'Unforgivably slow...'"

# Function to make the current enemy strong but clumsy.
# It has 90 AC and +70 on attack rolls but deals more damage
# and has more health compared to the agile enemy.
class MightyFoe:
    def __init__(self):
        self.type = "Mighty Foe"
        self.hp = 20 + random.randint(10,25)
        self.damage_min = 6
        self.damage_max = 18
        self.precision = 14
        self.agility = 9
        self.exp_reward = 25 + random.randint(5, 10)
        self.money_reward = random.randint(15, 25)
        self.defeat = "'Nani?!'"

# Function to generate a more balanced current enemy.
# It is a sort of middle ground between the previous two.
# With 130 AC and +80 on attack rolls while also being tough.
class BalancedFoe:
    def __init__(self):
        self.type = "Balanced Enemy"
        self.hp = 20 + random.randint(5,20)
        self.damage_min = 6
        self.damage_max = 15
        self.precision = 16
        self.agility = 13
        self.exp_reward = 25 + random.randint(5, 10)
        self.money_reward = random.randint(20, 25)
        self.defeat = "'Augh!!!'"

# Function to generate a weak mook.
# This is the weakest enemy in the game and not very threatening.
# Has only 70 AC and +45 on attacks, meaning that even at the start
# of the game they will be easy to hit and dodge.
class Weakling:
    def __init__(self):
        self.type = "Weakling"
        self.hp = random.randint(5,15)
        self.damage_min = 4
        self.damage_max = 8
        self.precision = 9
        self.agility = 7
        self.exp_reward = 10 + random.randint(5, 10)
        self.money_reward = random.randint(5, 15)
        self.defeat = "'Weh!'"

# Function to generate a tough elite enemy.
# This is the strongest random option in the early enemy table.
# Has 150 AC (nearly impossible to hit without buffs or Helios Dive
# before upgrading precision) and +90 on attacks, meaning it
# will almost always hit the player with 10 agility.
# A starting player may need to use a sardine and go all out with
# Eye of Omens, Demon Mode, and/or Helios Dive to win.
class Elite:
    def __init__(self):
        self.type = "Elite"
        self.hp = 45 + random.randint(10,20)
        self.damage_min = 12
        self.damage_max = 24
        self.precision = 18
        self.agility = 15
        self.exp_reward = 50
        self.money_reward = random.randint(30, 50)
        self.defeat = "'No! It can't be!'"

# Function to make stats for a Dodgeball Overlord.
# This is a sort of mini-boss that appears periodically and
# drops spellcards. Replaced by a stronger variant past mid-game.
# It has 180 AC and +110 to attack rolls, making it very deadly
# early on.
class Overlord:
    def __init__(self):
        self.type = "Dodgeball Overlord"
        self.hp = 100
        self.damage_min = 15
        self.damage_max = 30
        self.precision = 22
        self.agility = 18
        self.exp_reward = 100
        self.money_reward = 80
        self.defeat = "'How is this possible?!'"

# Tier 2 enemy sheets. These ones show up only on the second
# enemy table.

# Catgirls are agile but also tougher than most previous foes.
# With 180 AC and +115 on attacks they are comparable to overlords.
# But deal less damage and have less health.
class Catgirl:
    def __init__(self):
        self.type = "Catgirl"
        self.hp = 50 + random.randint(20,35)
        self.damage_min = 10
        self.damage_max = 20
        self.precision = 23
        self.agility = 18
        self.exp_reward = 45 + random.randint(5, 10)
        self.money_reward = random.randint(25, 50)
        self.defeat = "'N-nyaaa...'"

# Psychics are more frail than catgirls but their powers let them
# control the ball in ways that make them hard to hit and dodge
# compared to tier 1 enemies.
# They have 170 AC and +125 on attacks but don't hit too hard.
class Psychic:
    def __init__(self):
        self.type = "Psychic"
        self.hp = 30 + random.randint(10,20)
        self.damage_min = 10
        self.damage_max = 16
        self.precision = 25
        self.agility = 17
        self.exp_reward = 45 + random.randint(5, 10)
        self.money_reward = random.randint(30, 50)
        self.defeat = "'I have foreseen your every move... and concluded I can't win! See ya!'"

# Musha are armored warriors with good stats all around.
# 190 AC and +150 on attacks.
class Musha:
    def __init__(self):
        self.type = "Musha"
        self.hp = 85 + random.randint(15,100)
        self.damage_min = 20
        self.damage_max = 30
        self.precision = 30
        self.agility = 19
        self.exp_reward = 75 + random.randint(15, 25)
        self.money_reward = random.randint(25, 60)
        self.defeat = "'It was you!!!'"

# Abominations have very wide HP and damage ranges, meaning
# they are unpredictable but potentially run-ending threats.
# Must be taken seriously if encountered early.
# 210 AC and +200 on attack rolls means they will hit consistently
# until the player has at least 20 agility.
class Abomination:
    def __init__(self):
        self.type = "Abomination"
        self.hp = 100 + random.randint(100,350)
        self.damage_min = 15
        self.damage_max = 55
        self.precision = 40
        self.agility = 21
        self.exp_reward = 80 + random.randint(15, 20)
        self.money_reward = random.randint(60, 85)
        self.defeat = "'...'"

# Dragons don't start appearing until halfway through the game.
# They are always very durable and have 260 AC and +250 on attacks.
class Dragon:
    def __init__(self):
        self.type = "Dragon"
        self.hp = 500
        self.damage_min = 30
        self.damage_max = 50
        self.precision = 50
        self.agility = 26
        self.exp_reward = 100
        self.money_reward = random.randint(60, 95)
        self.defeat = "'A mere human cannot surpass me! I am perfection! Who are you?!'"

# Kaiju are endgame enemies with 300 AC and +300 on attacks,
# a huge step up from even dragons.
class Kaiju:
    def __init__(self):
        self.type = "Kaiju"
        self.hp = 1200
        self.damage_min = 50
        self.damage_max = 75
        self.precision = 60
        self.agility = 30
        self.exp_reward = 100
        self.money_reward = random.randint(75, 100)
        self.defeat = "'SKREOOONK'"

# Upgraded overlord that starts appearing starting in the mid-game.
# With 350 AC and +325 on attacks they are in some ways stronger than
# kaijus, in ways that can more than make up for thier lower damage
# and health. They may be the strongest non-unique enemies in the game.
class BadassOverlord:
    def __init__(self):
        self.type = "Badass Freakin' Overlord"
        self.hp = 1000
        self.damage_min = 50
        self.damage_max = 60
        self.precision = 65
        self.agility = 35
        self.exp_reward = 100
        self.money_reward = 100
        self.defeat = "'I found a worthy opponent right at the end... I can move on with a smile.'"

# Function to create the Dodgeball God. This is a final boss
# that has a couple of additional values for its shield and
# phase 2 activation.
# Additionally with 350 AC the player will reach 100% chance
# to hit it with 70 precision but less than that would be
# a struggle. It also has +500 on attack rolls, meaning 60
# agility is needed to ensure it won't hit, and even then
# it grows stronger periodically and when going under 50%
# HP, so high agility is only a temporary shield.
class God:
    def __init__(self):
        self.type = "Dodgeball God"
        self.hp = 10000
        self.max_hp = 10000
        self.damage_min = 60
        self.damage_max = 120
        self.precision = 100
        self.agility = 35
        self.shield_active = False
        self.phase_2 = False
        self.defeat = "'Is this... what you wanted...?'"


def get_defeat_message(enemy_type):
    """This function stores a dictionary with defeat messages for all enemy types, and plays the one
    that matches the type of enemy that defeated the player, or a generic one if the type is outside
    the dictionary."""
    defeat_messages = {
        "Agile Foe": "You were outmaneuvered by the agile foe...",
        "Mighty Foe": "You were overpowered by the mighty foe...",
        "Balanced Foe": "You could not keep up with the balanced foe...",
        "Weakling": "You lost to a weakling... the shame is haunting.",
        "Elite": "The elite strikes a cute victory pose over your body.",
        "Dodgeball Overlord": "You have been overmastered by the overlord...",
        "Catgirl": "The catgirl sits nearby and licks her paw.",
        "Psychic": "Your mind is shattered by the psychic. Hope this does not awaken anything in you.",
        "Musha": "Defeated... You will never be able to beat Ginseigo at this rate.",
        "Abomination": "The abomination's power has left you in despair.",
        "Dragon": "The dragon's flames were too hot for you.",
        "Kaiju": "The kaiju's red atomic breath overcame even your best throws.",
        "Badass Freakin' Overlord": "The overlord's merciless throws leave you in a crater on the ground.",
        "Dodgeball God": "You tried, but the world refused to change..."
    }

    return defeat_messages.get(enemy_type, "You have been defeated!")

# Function that creates an enemy of a random type.
# It rolls a random number between 0 and 100 and
# uses if/elif branches to divide the options into
# ranges kind of like a TTRPG random encounter table.
def create_random_enemy():
    enemy_roll = random.randint(0,100)
    if enemy_roll <= 25:
        new_enemy = AgileFoe()
    elif enemy_roll <= 50:
        new_enemy = MightyFoe()
    elif enemy_roll <= 75:
        new_enemy = BalancedFoe()
    elif enemy_roll <= 95:
        new_enemy = Weakling()
    elif enemy_roll <= 100:
        new_enemy = Elite()
    slow_print("\nA new adversary approaches!")
    # We return the result of the roll.
    return new_enemy

# We make a very similar function that will be used to roll mid and
# late-game enemies once the next_god counter puts the player out of
# the early game. This other function will roll different ranges
# depending on the stage of the game.
def create_greater_enemy():
    if fight_god > game_midpoint:
        enemy_roll = random.randint(0, 100)
    elif fight_god > starting_late_game:
        enemy_roll = random.randint(25, 125)
    else:
        enemy_roll = random.randint(50, 150)

    if enemy_roll <= 10:
        new_enemy = Elite()
    elif enemy_roll <= 30:
        new_enemy = Catgirl()
    elif enemy_roll <= 50:
        new_enemy = Psychic()
    elif enemy_roll <= 80:
        new_enemy = Musha()
    elif enemy_roll <= 100:
        new_enemy = Abomination()
    elif enemy_roll <= 125:
        new_enemy = Dragon()
    elif enemy_roll <= 150:
        new_enemy = Kaiju()
    slow_print("\nA new adversary approaches!")
    return new_enemy

# These functions just make overlord enemies and the final boss.
# These are not in the random tables so instead they are used
# after enough battles have happened.
def create_overlord():
    new_overlord = Overlord()
    return new_overlord

def create_greater_overlord():
    new_overlord = BadassOverlord()
    return new_overlord

def create_god():
    dodgeball_god = God()
    return dodgeball_god
    
# Simple function that displays enemy type and HP.
def enemy_stats_display():
    print(f"\nCurrent Enemy: {current_enemy.type} | Enemy HP: {current_enemy.hp}")