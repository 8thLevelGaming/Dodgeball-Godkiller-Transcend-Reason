"""This module contains the code for the shop and gym."""

import items
import random
import player
import utils

def item_roll(player_character):
    """This is the function that rolls random items on each separate shop visit.
    Available items are those in the item pool but not in the player's inventory.
    It runs a for loop for every name in the pool."""
    available = [name for name in items.item_pool if name not in player_character.owned_items]
    # There is a bit of protection against rolling less than 3 available items but
    # I made so many that it is impossible to deplete the list in full playthrough.
    count = min(3, len(available))
    return random.sample(available, count)
    
def gym(player_character):
    """This is the gym function for the shop below.
    It calculates how much exp the player needs to level up.
    And if the player has money equal to that amount it purchases the exp
    at a ratio of $2 per experience point to level up."""
    training_cost = gym_price(player_character)
    exp_to_buy = training_cost // 2
    if player_character.money >= training_cost:
        player_character.money = player_character.money - training_cost
        player_character.exp = player_character.exp + exp_to_buy
        # The flavor text for the gym is randomized.
        gym_flavor_text = random_gym_text()
        print(f"\n{gym_flavor_text}")
        if player_character.exp >= 100:
            player_character.level = player_character.level + 1
            player_character.exp = player_character.exp - 100
            player_character.full_stats_display(player_character)
            player.level_up(player_character)
    else:
        print("You can't afford to go to the gym...")

def gym_price(player_character):
    """Function calculates and returns the cost of using the gym."""
    gym_price = (100 - player_character.exp) * 2
    return gym_price

def random_gym_text():
    """Lists and rolls randomized flavor text you can get when going to the gym."""
    gym_flavors = [
        "You lift heavy weights and run around for a while!",
        "You obliterate several target dummies with your throws!",
        "You do 100 push-ups, 100 sit-ups, 100 squats, and a 10 km run!"
    ]
    
    chosen_text = random.choice(gym_flavors)
    return chosen_text

def visit_shop(player_character):
    """Function that creates a shop the player periodically visits.
    At this shop, the player can buy a meal to fully restore HP and stamina.
    The player can also find three randomized items. Only one of them can be bought on each shop visit.
    This function uses getattr and setattr. These help with saving object attributes into strings.
    For example, setattr(player, "strength", 15) is the same as player.strength = 15. 
    There are cases where this is preferable, such as when an attribute is decided at runtime."""
    available_items = item_roll()
    # We make it so every shop visit the player enters as not having
    # already bought an item, enabling them to buy a new one.
    player_already_bought = False

    # The prices and rarities of the 3 items rolled are collected.
    # Note that we are using list positions for the items, meaning that
    # the first item is at position 0.
    item1_price = items.item_price(available_items[0])
    item1_rarity = items.item_pool[available_items[0]]['rarity']
    item2_price = items.item_price(available_items[1])
    item2_rarity = items.item_pool[available_items[1]]['rarity']
    item3_price = items.item_price(available_items[2])
    item3_rarity = items.item_pool[available_items[2]]['rarity']

    # This is the loop where the player can actually interact with the shop.
    while True:
        utils.slow_print("\nA strange old man offers you mapo tofu and a relic. You can buy only one of the three.")
        player.stats_display(player_character)
        utils.slow_print(f"You currently have ${player.money}")
        print("-" * 40)
        gym_price_display = gym_price()
        
        options = {
        "1": f"Buy {available_items[0]} ({item1_rarity}) for ${item1_price}\n ---> {items.item_effects_display(available_items[0])}",
        "2": f"Buy {available_items[1]} ({item2_rarity}) for ${item2_price}\n ---> {items.item_effects_display(available_items[1])}",
        "3": f"Buy {available_items[2]} ({item3_rarity}) for ${item3_price}\n ---> {items.item_effects_display(available_items[2])}",
        "4": "Eat some extra-spicy mapo tofu for $20.",
        "5": f"Buy a big can of sardines to eat later for $20. You currently have {player.sardine_inventory}.",
        "6": f"Hit the gym and train. It will cost ${gym_price_display}.",
        "7": "View your stats.",
        "8": "Leave the shop."
        }
        for num, text in options.items():
            print(f"{num}) {text}")

        player_buy = input("What will you get? ")
        
        if player_buy in options:
            if player_buy == "1":
                item_name = available_items[0]
                # We can call the apply_item_effects function to handle adding those
                if player_character.money >= item1_price:
                    # In addition to checking the player can afford the item we also
                    # confirm that the player has not bought an item yet.
                    if player_already_bought is False:
                        player_character.money = player_character.money - item1_price
                        items.apply_item_effects(item_name, player_character)
                        print(f"You bought {item_name}! ({items.item_effects_display(item_name)})")
                        # After sale, we mark that the player bought an item,
                        # which blocks the other options for this visit.
                        player_already_bought = True
                    else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that.")
                    
            elif player_buy == "2":
                item_name = available_items[1]
                if player.money >= item2_price:
                    if player_already_bought is False:
                        player.money = player.money - item2_price
                        items.apply_item_effects(item_name, player_character)
                        print(f"You bought {item_name}! ({items.item_effects_display(item_name)})")
                        player_already_bought = True
                    else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that.")
                    
            elif player_buy == "3":
                item_name = available_items[2]
                if player_character.money >= item3_price:
                     if player_already_bought is False:
                        player_character.money = player_character.money - item3_price
                        items.apply_item_effects(item_name, player_character)
                        print(f"You bought {item_name}! ({items.item_effects_display(item_name)})")
                        player_already_bought = True
                     else:
                        print("The strange old man only had one relic for sale. Try again next visit.")
                else:
                    print("You can't afford that")

            # The remaining options are very simple, restoring the player,
            # increasing their sardine_inventory attribute, calling the
            # gym function, or displaying their stats.
            elif player_buy == "4":
                if player_character.money >= 20:
                    player_character.money = player_character.money - 20
                    utils.slow_print("\nYou greedily devour the mapo tofu! It tastes sinful.")
                    player_character.hp = player_character.max_hp()
                    player_character.stamina = player_character.max_stamina()
                else:
                    print("You can't even afford that delicious mapo tofu... your martyrdom is truly endless.")
                    
            elif player_buy == "5":
                if player_character.money >= 20:
                    player_character.money = player_character.money - 20
                    player_character.sardine_inventory = player_character.sardine_inventory + 1
                    print(f"\nYou buy some sardines. You now have {player_character.sardine_inventory}")
                else:
                    print("The poor must make do without sardines. How cruel.")
                    
            elif player_buy == "6":
                gym(player_character)
                
            elif player_buy == "7":
                player.full_stats_display(player_character)

            # We break the loop only when the player leaves the shop.
            elif player_buy == "8":
                utils.slow_print("You leave the tofu shop.")
                break
        else:
            print("Your options range between 1 and 8!")